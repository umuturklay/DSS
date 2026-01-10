"""
Unit tests for ScholarshipRanker service
Tests AHP-based weighted scoring logic
"""
import pytest
from app.services.ranker import ScholarshipRanker
from datetime import datetime, timedelta


class TestGPAScore:
    """Test GPA buffer score calculation"""

    def test_high_gpa_buffer(self, sample_student, sample_scholarship):
        """Student with high GPA above minimum gets high score"""
        # Student: 3.5, Min: 3.0, Buffer: 0.5
        score = ScholarshipRanker.calculate_gpa_score(sample_student, sample_scholarship)

        assert 0.0 <= score <= 1.0
        assert score > 0.1  # Should have decent buffer

    def test_exact_gpa_minimum(self, sample_scholarship):
        """Student exactly at minimum GPA gets low score"""
        from app.models.student import Student

        exact_student = Student({
            'student_id': 'EXACT',
            'gpa': 3.0,  # Exactly at minimum
            'course': 9991,
            'gender': 0,
            'age': 22,
            'is_international': False,
            'nationality': 1
        })

        score = ScholarshipRanker.calculate_gpa_score(exact_student, sample_scholarship)

        assert score == 0.0  # No buffer

    def test_very_high_gpa(self, high_gpa_student, sample_scholarship):
        """Student with very high GPA gets high score"""
        # Student: 3.8, Min: 3.0, Buffer: 0.8
        score = ScholarshipRanker.calculate_gpa_score(high_gpa_student, sample_scholarship)

        assert score > 0.15  # Significant buffer
        assert score <= 1.0


class TestKeywordScore:
    """Test keyword matching score calculation"""

    def test_perfect_keyword_match(self, sample_student, sample_scholarship):
        """Perfect keyword overlap gets high score"""
        # Student: ['computer science', 'technology', 'engineering']
        # Scholarship: ['computer science', 'technology']
        score = ScholarshipRanker.calculate_keyword_score(sample_student, sample_scholarship)

        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should have good overlap

    def test_no_keyword_match(self, low_gpa_student, sample_scholarship):
        """No keyword overlap gets low score"""
        # low_gpa_student: ['business', 'economics']
        # sample_scholarship: ['computer science', 'technology']
        score = ScholarshipRanker.calculate_keyword_score(low_gpa_student, sample_scholarship)

        assert score == 0.0  # No overlap

    def test_partial_keyword_match(self, sample_scholarship):
        """Partial keyword overlap gets medium score"""
        from app.models.student import Student

        partial_student = Student({
            'student_id': 'PARTIAL',
            'gpa': 3.5,
            'course': 9991,
            'gender': 0,
            'age': 22,
            'is_international': False,
            'nationality': 1,
            'keywords': ['computer science', 'design', 'art']  # Only 1 match
        })

        score = ScholarshipRanker.calculate_keyword_score(partial_student, sample_scholarship)

        assert 0.0 < score < 1.0
        assert score < 0.7  # Partial match


class TestCompetitivenessScore:
    """Test competitiveness score calculation"""

    def test_low_competitiveness(self, sample_scholarship):
        """Low competitiveness scholarship gets high score"""
        sample_scholarship.competitiveness = 0.3  # Easy to get

        score = ScholarshipRanker.calculate_competitiveness_score(sample_scholarship)

        assert score > 0.6  # Inverse: low competition = high score

    def test_high_competitiveness(self, high_gpa_scholarship):
        """High competitiveness scholarship gets low score"""
        # high_gpa_scholarship.competitiveness = 0.9
        score = ScholarshipRanker.calculate_competitiveness_score(high_gpa_scholarship)

        assert score < 0.2  # Inverse: high competition = low score

    def test_medium_competitiveness(self, sample_scholarship):
        """Medium competitiveness gets medium score"""
        sample_scholarship.competitiveness = 0.5

        score = ScholarshipRanker.calculate_competitiveness_score(sample_scholarship)

        assert 0.4 <= score <= 0.6


class TestDeadlineScore:
    """Test deadline urgency score calculation"""

    def test_very_soon_deadline(self):
        """Deadline very soon gets high urgency score"""
        from app.models.scholarship import Scholarship

        soon_deadline = (datetime.now() + timedelta(days=15)).isoformat()
        scholarship = Scholarship({
            'id': 'SOON',
            'name': 'Soon Deadline',
            'min_gpa': 3.0,
            'eligible_courses': [],
            'eligible_nationalities': [],
            'deadline': soon_deadline
        })

        score = ScholarshipRanker.calculate_deadline_score(scholarship)

        assert score > 0.5  # High urgency

    def test_far_future_deadline(self):
        """Deadline far in future gets low urgency score"""
        from app.models.scholarship import Scholarship

        far_deadline = (datetime.now() + timedelta(days=200)).isoformat()
        scholarship = Scholarship({
            'id': 'FAR',
            'name': 'Far Deadline',
            'min_gpa': 3.0,
            'eligible_courses': [],
            'eligible_nationalities': [],
            'deadline': far_deadline
        })

        score = ScholarshipRanker.calculate_deadline_score(scholarship)

        assert score < 0.3  # Low urgency

    def test_deadline_score_bounds(self, sample_scholarship):
        """Deadline score is always between 0 and 1"""
        score = ScholarshipRanker.calculate_deadline_score(sample_scholarship)

        assert 0.0 <= score <= 1.0


class TestDocBurdenScore:
    """Test document burden score calculation"""

    def test_few_documents(self, sample_scholarship):
        """Few required documents gets high score"""
        sample_scholarship.required_documents = ['transcript']  # Only 1 doc

        score = ScholarshipRanker.calculate_doc_burden_score(sample_scholarship)

        assert score > 0.8  # Easy application

    def test_many_documents(self):
        """Many required documents gets low score"""
        from app.models.scholarship import Scholarship

        heavy_scholarship = Scholarship({
            'id': 'HEAVY',
            'name': 'Heavy Docs',
            'min_gpa': 3.0,
            'eligible_courses': [],
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat(),
            'required_documents': ['transcript', 'essay', 'recommendation', 'portfolio', 'research_proposal']
        })

        score = ScholarshipRanker.calculate_doc_burden_score(heavy_scholarship)

        assert score < 0.5  # Burdensome application


class TestFinalScore:
    """Test weighted final score calculation"""

    def test_calculate_final_score(self, sample_student, sample_scholarship):
        """Calculate weighted final score"""
        score, breakdown = ScholarshipRanker.calculate_final_score(
            sample_student, sample_scholarship
        )

        # Verify score is in valid range
        assert 0.0 <= score <= 1.0

        # Verify breakdown contains all factors
        assert 'gpa_buffer' in breakdown
        assert 'keyword_match' in breakdown
        assert 'competitiveness' in breakdown
        assert 'time_to_deadline' in breakdown
        assert 'doc_burden' in breakdown

        # Verify all breakdown scores are valid
        for factor_score in breakdown.values():
            assert 0.0 <= factor_score <= 1.0

    def test_weights_sum_to_one(self):
        """Verify AHP weights sum to 1.0"""
        weights = ScholarshipRanker.WEIGHTS

        total = sum(weights.values())

        assert abs(total - 1.0) < 0.001  # Should sum to 1.0

    def test_high_scoring_profile(self, high_gpa_student, sample_scholarship):
        """High-quality student gets high score"""
        # High GPA, matching keywords, etc.
        sample_scholarship.competitiveness = 0.3  # Easy scholarship
        sample_scholarship.required_documents = ['transcript']  # Few docs

        score, _ = ScholarshipRanker.calculate_final_score(
            high_gpa_student, sample_scholarship
        )

        assert score > 0.5  # Should score well


class TestRankScholarships:
    """Test ranking multiple scholarships"""

    def test_rank_single_scholarship(self, sample_student, sample_scholarship):
        """Rank single eligible scholarship"""
        eligible = [{'scholarship': sample_scholarship, 'met_criteria': [], 'failed_criteria': []}]

        ranked = ScholarshipRanker.rank_scholarships(eligible, sample_student)

        assert len(ranked) == 1
        assert 'scholarship' in ranked[0]
        assert 'score' in ranked[0]
        assert 'breakdown' in ranked[0]
        assert 'ranking' in ranked[0]
        assert ranked[0]['ranking'] == 1

    def test_rank_multiple_scholarships(self, sample_student):
        """Rank multiple scholarships in correct order"""
        from app.models.scholarship import Scholarship

        # Create 3 scholarships with different competitiveness
        easy_scholarship = Scholarship({
            'id': 'EASY',
            'name': 'Easy',
            'min_gpa': 2.0,
            'eligible_courses': [9991],
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat(),
            'competitiveness': 0.2,  # Very easy
            'keywords': ['computer science'],
            'required_documents': ['transcript']
        })

        medium_scholarship = Scholarship({
            'id': 'MEDIUM',
            'name': 'Medium',
            'min_gpa': 2.5,
            'eligible_courses': [9991],
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat(),
            'competitiveness': 0.5,  # Medium
            'keywords': ['computer science'],
            'required_documents': ['transcript', 'essay']
        })

        hard_scholarship = Scholarship({
            'id': 'HARD',
            'name': 'Hard',
            'min_gpa': 3.0,
            'eligible_courses': [9991],
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat(),
            'competitiveness': 0.9,  # Very hard
            'keywords': ['computer science'],
            'required_documents': ['transcript', 'essay', 'portfolio']
        })

        eligible = [
            {'scholarship': hard_scholarship, 'met_criteria': [], 'failed_criteria': []},
            {'scholarship': easy_scholarship, 'met_criteria': [], 'failed_criteria': []},
            {'scholarship': medium_scholarship, 'met_criteria': [], 'failed_criteria': []}
        ]

        ranked = ScholarshipRanker.rank_scholarships(eligible, sample_student)

        # Should be ranked by score (highest first)
        assert len(ranked) == 3
        assert ranked[0]['score'] >= ranked[1]['score'] >= ranked[2]['score']

        # Rankings should be 1, 2, 3
        assert ranked[0]['ranking'] == 1
        assert ranked[1]['ranking'] == 2
        assert ranked[2]['ranking'] == 3

    def test_rank_empty_list(self, sample_student):
        """Rank empty list returns empty"""
        eligible = []

        ranked = ScholarshipRanker.rank_scholarships(eligible, sample_student)

        assert ranked == []
