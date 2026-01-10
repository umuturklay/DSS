from datetime import datetime
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.models.match_result import MatchResult

class Explainer:
    """
    Explanation generator for scholarship matching decisions.
    Based on Fajardo et al. (2024) - Transparency in educational DSS.
    """

    @staticmethod
    def generate_match_explanation(ranked_item, student):
        """
        Generate detailed explanation for a matched scholarship.

        Args:
            ranked_item: Dict with scholarship, score, breakdown, criteria
            student: Student object

        Returns:
            MatchResult object with full explanation
        """
        scholarship = ranked_item['scholarship']
        score = ranked_item['score']

        result = MatchResult(scholarship, student, matched=True, score=score)
        result.ranking = ranked_item.get('ranking', 0)
        result.met_criteria = ranked_item.get('met_criteria', [])
        result.failed_criteria = ranked_item.get('failed_criteria', [])
        result.scoring_breakdown = ranked_item.get('breakdown', {})

        result.recommendation = Explainer._generate_recommendation(
            scholarship, score, result.ranking
        )

        return result

    @staticmethod
    def generate_rejection_explanation(ineligible_item, student):
        """
        Generate explanation for a non-matched scholarship.

        Args:
            ineligible_item: Dict with scholarship and failed_criteria
            student: Student object

        Returns:
            MatchResult object with rejection explanation
        """
        scholarship = ineligible_item['scholarship']

        result = MatchResult(scholarship, student, matched=False, score=0.0)
        result.met_criteria = ineligible_item.get('met_criteria', [])
        result.failed_criteria = ineligible_item.get('failed_criteria', [])

        result.recommendation = Explainer._generate_rejection_recommendation(
            scholarship, result.failed_criteria
        )

        return result

    @staticmethod
    def _generate_recommendation(scholarship, score, ranking):
        """Generate recommendation text based on score and ranking"""
        deadline_str = scholarship.deadline[:10] if scholarship.deadline else "rolling"

        if score >= 0.8:
            strength = "Excellent"
            action = "Highly recommended - Apply as soon as possible"
        elif score >= 0.6:
            strength = "Strong"
            action = "Recommended - Good fit for your profile"
        elif score >= 0.4:
            strength = "Moderate"
            action = "Consider applying if interested"
        else:
            strength = "Weak"
            action = "Low priority - Consider other options first"

        return f"{strength} match (#{ranking}) - {action}. Deadline: {deadline_str}"

    @staticmethod
    def _generate_rejection_recommendation(scholarship, failed_criteria):
        """Generate recommendation for rejected applications"""
        if not failed_criteria:
            return "Not eligible - Technical error in evaluation"

        primary_issue = failed_criteria[0].replace('✗ ', '')

        if 'GPA' in primary_issue:
            return f"Not eligible - {primary_issue}. Consider improving academic performance."
        elif 'Course' in primary_issue or 'major' in primary_issue.lower():
            return f"Not eligible - {primary_issue}. Look for scholarships in your field."
        elif 'Nationality' in primary_issue or 'international' in primary_issue.lower():
            return f"Not eligible - {primary_issue}. Search for scholarships accepting your status."
        elif 'Age' in primary_issue:
            return f"Not eligible - {primary_issue}. Look for scholarships with broader age range."
        elif 'Deadline' in primary_issue:
            return f"Not eligible - {primary_issue}. Scholarship closed."
        else:
            return f"Not eligible - {primary_issue}"

    @staticmethod
    def format_for_json(match_results):
        """
        Format match results for JSON API response.

        Args:
            match_results: List of MatchResult objects

        Returns:
            list: JSON-serializable list of dicts
        """
        return [result.to_dict() for result in match_results]

    @staticmethod
    def generate_summary_stats(matched_results, rejected_results, student):
        """
        Generate summary statistics for student dashboard.

        Returns:
            dict: Summary stats
        """
        total_scholarships = len(matched_results) + len(rejected_results)
        matched_count = len(matched_results)
        match_rate = (matched_count / total_scholarships * 100) if total_scholarships > 0 else 0

        if matched_results:
            avg_score = sum(r.score for r in matched_results) / len(matched_results)
            top_score = max(r.score for r in matched_results)
        else:
            avg_score = 0.0
            top_score = 0.0

        return {
            'student_id': student.student_id,
            'total_scholarships_analyzed': total_scholarships,
            'matched_count': matched_count,
            'rejected_count': len(rejected_results),
            'match_rate_percent': round(match_rate, 1),
            'average_match_score': round(avg_score, 3),
            'top_match_score': round(top_score, 3),
            'recommendation': Explainer._generate_student_recommendation(matched_count, avg_score)
        }

    @staticmethod
    def _generate_student_recommendation(matched_count, avg_score):
        """Generate overall recommendation for student"""
        if matched_count == 0:
            return "No matches found. Consider improving your GPA or broadening your search criteria."
        elif matched_count <= 2:
            return f"Limited options ({matched_count} matches). Consider applying to all matched scholarships."
        elif matched_count <= 5:
            return f"Good options ({matched_count} matches). Focus on top 3 scholarships with highest scores."
        else:
            return f"Excellent options ({matched_count} matches). Apply to top 5 scholarships strategically."
