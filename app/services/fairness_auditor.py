from collections import defaultdict
from app.models.student import Student
from app.models.match_result import MatchResult

class FairnessAuditor:
    """
    Fairness auditing system for detecting bias in scholarship matching.
    Based on Rasooli et al. (2023) - Fairness in Educational Assessment.
    """

    BIAS_THRESHOLD = 0.15

    @staticmethod
    def calculate_match_rate(students_subset, all_matched_results):
        """
        Calculate match rate for a subset of students.

        Args:
            students_subset: List of student IDs
            all_matched_results: Dict mapping student_id -> list of matched scholarships

        Returns:
            float: Match rate (0-1)
        """
        if not students_subset:
            return 0.0

        total_matches = sum(
            len(all_matched_results.get(student_id, []))
            for student_id in students_subset
        )

        return total_matches / len(students_subset)

    @staticmethod
    def audit_by_demographic(all_students, all_matched_results):
        """
        Run fairness audit across demographic groups.

        Args:
            all_students: List of Student objects
            all_matched_results: Dict mapping student_id -> list of MatchResult objects

        Returns:
            dict: Audit results with bias detection
        """
        demographic_groups = {
            'gender': defaultdict(list),
            'is_international': defaultdict(list),
            'gpa_band': defaultdict(list),
            'current_scholarship_holder': defaultdict(list)
        }

        for student in all_students:
            demographic_groups['gender'][student.gender].append(student.student_id)
            demographic_groups['is_international'][student.is_international].append(student.student_id)

            if student.gpa < 2.5:
                gpa_band = 'low (<2.5)'
            elif student.gpa <= 3.2:
                gpa_band = 'mid (2.5-3.2)'
            else:
                gpa_band = 'high (>3.2)'
            demographic_groups['gpa_band'][gpa_band].append(student.student_id)

            demographic_groups['current_scholarship_holder'][student.current_scholarship_holder].append(student.student_id)

        audit_results = {}
        bias_alerts = []

        for group_type, groups in demographic_groups.items():
            group_results = {}

            for group_value, student_ids in groups.items():
                match_rate = FairnessAuditor.calculate_match_rate(student_ids, all_matched_results)
                group_results[str(group_value)] = {
                    'count': len(student_ids),
                    'match_rate': round(match_rate, 3),
                    'total_matches': sum(len(all_matched_results.get(sid, [])) for sid in student_ids)
                }

            audit_results[group_type] = group_results

            match_rates = [data['match_rate'] for data in group_results.values()]
            if match_rates:
                gap = max(match_rates) - min(match_rates)

                if gap > FairnessAuditor.BIAS_THRESHOLD:
                    bias_alerts.append({
                        'group_type': group_type,
                        'gap': round(gap, 3),
                        'details': group_results,
                        'severity': 'high' if gap > 0.3 else 'medium'
                    })

        return {
            'demographic_analysis': audit_results,
            'bias_alerts': bias_alerts,
            'bias_detected': len(bias_alerts) > 0,
            'threshold_used': FairnessAuditor.BIAS_THRESHOLD
        }

    @staticmethod
    def generate_fairness_report(audit_results):
        """
        Generate human-readable fairness report.

        Returns:
            str: Formatted report
        """
        report = []
        report.append("FAIRNESS AUDIT REPORT")
        report.append("=" * 60)

        if not audit_results['bias_detected']:
            report.append("\n✅ No significant bias detected")
            report.append(f"   All demographic gaps below {audit_results['threshold_used']*100}% threshold")
        else:
            report.append(f"\n⚠️  {len(audit_results['bias_alerts'])} bias alerts detected\n")

            for alert in audit_results['bias_alerts']:
                report.append(f"\n🚨 {alert['severity'].upper()} SEVERITY")
                report.append(f"   Group: {alert['group_type']}")
                report.append(f"   Gap: {alert['gap']*100:.1f}%")
                report.append(f"   Details:")

                for group_value, data in alert['details'].items():
                    report.append(f"     - {group_value}: {data['match_rate']:.3f} match rate ({data['count']} students)")

        report.append("\n" + "=" * 60)
        return "\n".join(report)

    @staticmethod
    def calculate_diversity_score(matched_scholarships):
        """
        Calculate diversity score for a set of matched scholarships.
        Measures how diverse the student pool is who matched.

        Args:
            matched_scholarships: Dict mapping scholarship_id -> list of matched student IDs

        Returns:
            dict: Diversity metrics
        """
        all_matched_students = set()
        for students in matched_scholarships.values():
            all_matched_students.update(students)

        scholarship_counts = {
            sch_id: len(students)
            for sch_id, students in matched_scholarships.items()
        }

        if not scholarship_counts:
            return {
                'total_unique_students': 0,
                'avg_students_per_scholarship': 0,
                'diversity_score': 0
            }

        avg_students = sum(scholarship_counts.values()) / len(scholarship_counts)

        concentration = sum(
            (count / len(all_matched_students)) ** 2
            for count in scholarship_counts.values()
        )
        diversity_score = 1 - concentration

        return {
            'total_unique_students': len(all_matched_students),
            'avg_students_per_scholarship': round(avg_students, 2),
            'diversity_score': round(diversity_score, 3),
            'interpretation': 'High diversity' if diversity_score > 0.7 else 'Moderate diversity' if diversity_score > 0.4 else 'Low diversity'
        }
