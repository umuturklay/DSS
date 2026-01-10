"""
Unit tests for Explainer service
Tests explanation generation logic
"""
import pytest
from app.services.explainer import Explainer


class TestMatchExplanation:
    """Test match explanation generation"""

    def test_generate_match_explanation(self, sample_student, sample_scholarship):
        """Generate explanation for matched scholarship"""
        ranked_item = {
            'scholarship': sample_scholarship,
            'score': 0.75,
            'breakdown': {
                'gpa_buffer': 0.125,
                'keyword_match': 0.200,
                'competitiveness': 0.075,
                'time_to_deadline': 0.100,
                'doc_burden': 0.112
            },
            'met_criteria': [
                '✓ GPA 3.5 meets minimum 3.0',
                '✓ Course Computer Science is eligible',
                '✓ Nationality eligible'
            ],
            'failed_criteria': [],
            'ranking': 1
        }

        result = Explainer.generate_match_explanation(ranked_item, sample_student)

        # Verify basic fields
        assert result.scholarship == sample_scholarship
        assert result.matched is True
        assert result.score == 0.75
        assert result.ranking == 1

        # Verify reasons
        assert len(result.reasons.met_criteria) == 3
        assert result.reasons.scoring_breakdown == ranked_item['breakdown']

        # Verify recommendation exists
        assert result.recommendation is not None
        assert len(result.recommendation) > 0

    def test_top_ranking_recommendation(self, sample_student, sample_scholarship):
        """Top-ranked scholarship gets encouraging recommendation"""
        ranked_item = {
            'scholarship': sample_scholarship,
            'score': 0.85,
            'breakdown': {},
            'met_criteria': [],
            'failed_criteria': [],
            'ranking': 1
        }

        result = Explainer.generate_match_explanation(ranked_item, sample_student)

        # Top ranking should have strong recommendation
        assert 'strong' in result.recommendation.lower() or 'excellent' in result.recommendation.lower() or 'apply' in result.recommendation.lower()


class TestRejectionExplanation:
    """Test rejection explanation generation"""

    def test_generate_rejection_explanation(self, low_gpa_student, sample_scholarship):
        """Generate explanation for rejected scholarship"""
        ineligible_item = {
            'scholarship': sample_scholarship,
            'met_criteria': [
                '✓ Course eligible',
                '✓ Age within limit'
            ],
            'failed_criteria': [
                '✗ GPA 2.2 below minimum 3.0',
                '✗ Nationality not eligible'
            ]
        }

        result = Explainer.generate_rejection_explanation(ineligible_item, low_gpa_student)

        # Verify basic fields
        assert result.scholarship == sample_scholarship
        assert result.matched is False
        assert result.score is None
        assert result.ranking is None

        # Verify reasons
        assert len(result.reasons.failed_criteria) == 2
        assert '✗ GPA' in result.reasons.failed_criteria[0]

        # Verify recommendation exists
        assert result.recommendation is not None
        assert len(result.recommendation) > 0

    def test_gpa_failure_recommendation(self, low_gpa_student):
        """GPA failure gets relevant recommendation"""
        from app.models.scholarship import Scholarship
        from datetime import datetime, timedelta

        scholarship = Scholarship({
            'id': 'HIGH_GPA',
            'name': 'Excellence',
            'min_gpa': 3.5,
            'eligible_courses': [],
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        })

        ineligible_item = {
            'scholarship': scholarship,
            'met_criteria': [],
            'failed_criteria': ['✗ GPA 2.2 below minimum 3.5']
        }

        result = Explainer.generate_rejection_explanation(ineligible_item, low_gpa_student)

        # Recommendation should mention GPA
        assert 'gpa' in result.recommendation.lower() or 'grade' in result.recommendation.lower()


class TestSummaryStats:
    """Test summary statistics generation"""

    def test_generate_summary_stats(self, sample_student):
        """Generate summary stats from match and rejection results"""
        from app.models.match_result import MatchResult

        # Create mock matched results
        matched = [
            MatchResult(
                scholarship=None,
                matched=True,
                score=0.85,
                ranking=1,
                reasons=None,
                recommendation=""
            ),
            MatchResult(
                scholarship=None,
                matched=True,
                score=0.70,
                ranking=2,
                reasons=None,
                recommendation=""
            )
        ]

        # Create mock rejected results
        rejected = [
            MatchResult(
                scholarship=None,
                matched=False,
                score=None,
                ranking=None,
                reasons=None,
                recommendation=""
            )
        ]

        summary = Explainer.generate_summary_stats(matched, rejected, sample_student)

        # Verify counts
        assert summary['matched_count'] == 2
        assert summary['rejected_count'] == 1
        assert summary['total_scholarships'] == 3

        # Verify match rate
        expected_rate = round((2 / 3) * 100, 1)
        assert summary['match_rate_percent'] == expected_rate

        # Verify top score
        assert summary['top_match_score'] == 0.85

        # Verify recommendation exists
        assert 'recommendation' in summary
        assert len(summary['recommendation']) > 0

    def test_summary_no_matches(self, sample_student):
        """Summary with no matches"""
        summary = Explainer.generate_summary_stats([], [], sample_student)

        assert summary['matched_count'] == 0
        assert summary['rejected_count'] == 0
        assert summary['top_match_score'] == 0.0

    def test_summary_all_matched(self, sample_student):
        """Summary with all scholarships matched"""
        from app.models.match_result import MatchResult

        matched = [
            MatchResult(scholarship=None, matched=True, score=0.9, ranking=1, reasons=None, recommendation=""),
            MatchResult(scholarship=None, matched=True, score=0.8, ranking=2, reasons=None, recommendation="")
        ]

        summary = Explainer.generate_summary_stats(matched, [], sample_student)

        assert summary['match_rate_percent'] == 100.0
        assert summary['top_match_score'] == 0.9


class TestFormatForJSON:
    """Test JSON formatting"""

    def test_format_single_result(self, sample_student, sample_scholarship):
        """Format single match result for JSON"""
        from app.models.match_result import MatchResult, MatchReasons

        reasons = MatchReasons(
            met_criteria=['✓ GPA eligible'],
            failed_criteria=[],
            scoring_breakdown={'gpa_buffer': 0.125}
        )

        result = MatchResult(
            scholarship=sample_scholarship,
            matched=True,
            score=0.75,
            ranking=1,
            reasons=reasons,
            recommendation="Apply soon"
        )

        formatted = Explainer.format_for_json([result])

        assert len(formatted) == 1
        assert formatted[0]['matched'] is True
        assert formatted[0]['score'] == 0.75
        assert formatted[0]['ranking'] == 1
        assert formatted[0]['scholarship_name'] == sample_scholarship.name
        assert 'reasons' in formatted[0]
        assert 'recommendation' in formatted[0]

    def test_format_multiple_results(self, sample_student, sample_scholarship, high_gpa_scholarship):
        """Format multiple results for JSON"""
        from app.models.match_result import MatchResult

        results = [
            MatchResult(scholarship=sample_scholarship, matched=True, score=0.8, ranking=1, reasons=None, recommendation=""),
            MatchResult(scholarship=high_gpa_scholarship, matched=True, score=0.7, ranking=2, reasons=None, recommendation="")
        ]

        formatted = Explainer.format_for_json(results)

        assert len(formatted) == 2
        assert formatted[0]['scholarship_name'] == sample_scholarship.name
        assert formatted[1]['scholarship_name'] == high_gpa_scholarship.name

    def test_format_empty_list(self):
        """Format empty list returns empty"""
        formatted = Explainer.format_for_json([])

        assert formatted == []
