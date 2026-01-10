from app.models.student import Student
from app.models.scholarship import Scholarship

class ScholarshipRanker:
    """
    AHP-inspired weighted scoring for scholarship ranking.
    Based on Bachtiar et al. (2021) - Multi-criteria decision making in DSS.
    """

    WEIGHTS = {
        'gpa_buffer': 0.25,
        'keyword_match': 0.25,
        'competitiveness': 0.20,
        'time_to_deadline': 0.15,
        'doc_burden': 0.15
    }

    @staticmethod
    def calculate_gpa_score(student, scholarship):
        """
        Score based on how much student's GPA exceeds minimum.
        Higher buffer = better fit.
        """
        gpa_buffer = student.gpa - scholarship.min_gpa
        max_gpa = 4.0
        normalized = min(gpa_buffer / max_gpa, 1.0)
        return max(0.0, normalized)

    @staticmethod
    def calculate_keyword_score(student, scholarship):
        """
        Jaccard similarity between student and scholarship keywords.
        Measures profile-scholarship fit.
        """
        if not student.keywords or not scholarship.keywords:
            return 0.5

        student_kw = set([kw.lower() for kw in student.keywords])
        scholarship_kw = set([kw.lower() for kw in scholarship.keywords])

        intersection = len(student_kw & scholarship_kw)
        union = len(student_kw | scholarship_kw)

        if union == 0:
            return 0.5

        return intersection / union

    @staticmethod
    def calculate_competitiveness_score(scholarship):
        """
        Inverse of competitiveness - easier scholarships score higher.
        Less competitive = higher chance of winning.
        """
        return 1.0 - scholarship.competitiveness

    @staticmethod
    def calculate_deadline_score(scholarship):
        """
        Urgency score based on days to deadline.
        Sooner deadline = higher urgency (but not too soon).
        Optimal range: 30-90 days.
        """
        days = scholarship.days_to_deadline()

        if days <= 0:
            return 0.0
        elif days < 15:
            return 0.3
        elif days < 30:
            return 0.6
        elif days <= 90:
            return 1.0
        elif days <= 180:
            return 0.8
        else:
            return 0.5

    @staticmethod
    def calculate_doc_burden_score(scholarship):
        """
        Score based on number of required documents.
        Fewer documents = easier application.
        """
        num_docs = len(scholarship.required_documents)
        max_docs = 5

        if num_docs == 0:
            return 1.0

        normalized = 1.0 - (num_docs / max_docs)
        return max(0.0, min(1.0, normalized))

    @staticmethod
    def calculate_final_score(student, scholarship):
        """
        Calculate weighted final score using AHP methodology.

        Returns:
            tuple: (final_score: float, breakdown: dict)
        """
        scores = {
            'gpa_buffer': ScholarshipRanker.calculate_gpa_score(student, scholarship),
            'keyword_match': ScholarshipRanker.calculate_keyword_score(student, scholarship),
            'competitiveness': ScholarshipRanker.calculate_competitiveness_score(scholarship),
            'time_to_deadline': ScholarshipRanker.calculate_deadline_score(scholarship),
            'doc_burden': ScholarshipRanker.calculate_doc_burden_score(scholarship)
        }

        final_score = sum(
            ScholarshipRanker.WEIGHTS[factor] * score
            for factor, score in scores.items()
        )

        breakdown = {
            factor: round(ScholarshipRanker.WEIGHTS[factor] * score, 3)
            for factor, score in scores.items()
        }

        return round(final_score, 3), breakdown

    @staticmethod
    def rank_scholarships(eligible_scholarships, student):
        """
        Rank eligible scholarships by final score.

        Args:
            eligible_scholarships: List of dicts with 'scholarship' and criteria
            student: Student object

        Returns:
            list: Ranked scholarships with scores (highest first)
        """
        ranked = []

        for item in eligible_scholarships:
            scholarship = item['scholarship']
            score, breakdown = ScholarshipRanker.calculate_final_score(student, scholarship)

            ranked.append({
                'scholarship': scholarship,
                'score': score,
                'breakdown': breakdown,
                'met_criteria': item['met_criteria'],
                'failed_criteria': item['failed_criteria']
            })

        ranked.sort(key=lambda x: x['score'], reverse=True)

        for i, item in enumerate(ranked, 1):
            item['ranking'] = i

        return ranked
