"""
Unit tests for RuleFilter service
Tests eligibility logic for scholarship matching
"""
import pytest
from app.services.rule_filter import RuleFilter
from app.models.scholarship import Scholarship
from datetime import datetime, timedelta


class TestGPAFilter:
    """Test GPA filtering logic"""

    def test_gpa_meets_requirement(self, sample_student, sample_scholarship):
        """Student GPA meets minimum requirement"""
        # Student GPA: 3.5, Required: 3.0
        is_eligible, message, _ = RuleFilter.filter_by_gpa(sample_scholarship, sample_student)

        assert is_eligible is True
        assert "meets minimum" in message.lower()
        assert "3.5" in message
        assert "3.0" in message

    def test_gpa_below_requirement(self, low_gpa_student, sample_scholarship):
        """Student GPA below minimum requirement"""
        # Student GPA: 2.2, Required: 3.0
        is_eligible, message, _ = RuleFilter.filter_by_gpa(sample_scholarship, low_gpa_student)

        assert is_eligible is False
        assert "below minimum" in message.lower()
        assert "2.2" in message or "2.20" in message

    def test_gpa_exact_match(self, sample_scholarship):
        """Student GPA exactly matches minimum"""
        from app.models.student import Student

        exact_student = Student({
            'gpa': 3.0,
            'course': 9991,
            'gender': 0,
            'age': 22,
            'is_international': False,
            'nationality': 1
        })

        is_eligible, message, _ = RuleFilter.filter_by_gpa(sample_scholarship, exact_student)

        assert is_eligible is True
        assert "meets minimum" in message.lower()


class TestCourseFilter:
    """Test course/major filtering logic"""

    def test_course_in_eligible_list(self, sample_student, sample_scholarship):
        """Student course is in eligible courses list"""
        # Student: 9991 (CS), Eligible: [9991, 9500]
        is_eligible, message, _ = RuleFilter.filter_by_course(sample_scholarship, sample_student)

        assert is_eligible is True
        assert "eligible" in message.lower()

    def test_course_not_in_eligible_list(self, low_gpa_student, sample_scholarship):
        """Student course is not in eligible courses list"""
        # Student: 9773 (Business), Eligible: [9991, 9500]
        is_eligible, message, _ = RuleFilter.filter_by_course(sample_scholarship, low_gpa_student)

        assert is_eligible is False
        assert "not in eligible" in message.lower() or "not eligible" in message.lower()

    def test_empty_eligible_courses(self, sample_student):
        """Empty eligible courses means all courses accepted"""
        from app.models.scholarship import Scholarship

        any_course_scholarship = Scholarship({
            'id': 'TEST',
            'name': 'Any Course',
            'min_gpa': 2.0,
            'eligible_courses': [],  # Empty = all courses
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        })

        is_eligible, message, _ = RuleFilter.filter_by_course(any_course_scholarship, sample_student)

        assert is_eligible is True
        assert "all courses" in message.lower() or "any course" in message.lower()


class TestNationalityFilter:
    """Test nationality filtering logic"""

    def test_nationality_in_eligible_list(self, sample_student, sample_scholarship):
        """Student nationality is in eligible list"""
        # Student: 6, Eligible: [1, 6, 22]
        is_eligible, message, _ = RuleFilter.filter_by_nationality(sample_scholarship, sample_student)

        assert is_eligible is True
        assert "eligible" in message.lower()

    def test_nationality_not_in_eligible_list(self, sample_student):
        """Student nationality is not in eligible list"""
        from app.models.scholarship import Scholarship

        restricted_scholarship = Scholarship({
            'id': 'TEST',
            'name': 'Local Only',
            'min_gpa': 2.0,
            'eligible_courses': [],
            'eligible_nationalities': [1],  # Only local
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        })

        # Student nationality: 6
        is_eligible, message, _ = RuleFilter.filter_by_nationality(restricted_scholarship, sample_student)

        assert is_eligible is False
        assert "not in eligible" in message.lower() or "not eligible" in message.lower()

    def test_empty_eligible_nationalities(self, sample_student, sample_scholarship):
        """Empty eligible nationalities means all accepted"""
        sample_scholarship.eligible_nationalities = []

        is_eligible, message, _ = RuleFilter.filter_by_nationality(sample_scholarship, sample_student)

        assert is_eligible is True
        assert "all nationalities" in message.lower()


class TestDeadlineFilter:
    """Test deadline filtering logic"""

    def test_future_deadline(self, sample_scholarship):
        """Scholarship deadline is in the future"""
        is_eligible, message = RuleFilter.filter_by_deadline(sample_scholarship)

        assert is_eligible is True
        assert "active" in message.lower() or "open" in message.lower()

    def test_expired_deadline(self, expired_scholarship):
        """Scholarship deadline has passed"""
        is_eligible, message = RuleFilter.filter_by_deadline(expired_scholarship)

        assert is_eligible is False
        assert "expired" in message.lower() or "passed" in message.lower()


class TestAgeFilter:
    """Test age filtering logic"""

    def test_age_within_limit(self, sample_student, sample_scholarship):
        """Student age is within limit"""
        # Student: 23, Max: 30
        is_eligible, message, _ = RuleFilter.filter_by_age(sample_scholarship, sample_student)

        assert is_eligible is True
        assert "within limit" in message.lower() or "eligible" in message.lower()

    def test_age_exceeds_limit(self, sample_scholarship):
        """Student age exceeds limit"""
        from app.models.student import Student

        old_student = Student({
            'student_id': 'OLD',
            'gpa': 3.5,
            'course': 9991,
            'gender': 0,
            'age': 35,  # Max is 30
            'is_international': False,
            'nationality': 1
        })

        is_eligible, message, _ = RuleFilter.filter_by_age(sample_scholarship, old_student)

        assert is_eligible is False
        assert "exceeds" in message.lower() or "above" in message.lower()


class TestInternationalFilter:
    """Test international student requirement filtering"""

    def test_international_required_and_is_international(self, sample_student, international_scholarship):
        """Scholarship requires international, student is international"""
        is_eligible, message, _ = RuleFilter.filter_by_international_status(
            international_scholarship, sample_student
        )

        assert is_eligible is True
        assert "international" in message.lower()

    def test_international_required_but_is_local(self, high_gpa_student, international_scholarship):
        """Scholarship requires international, student is local"""
        is_eligible, message, _ = RuleFilter.filter_by_international_status(
            international_scholarship, high_gpa_student
        )

        assert is_eligible is False
        assert "requires international" in message.lower() or "must be international" in message.lower()

    def test_international_not_required(self, sample_student, sample_scholarship):
        """Scholarship doesn't require international status"""
        sample_scholarship.requires_international = False

        is_eligible, message, _ = RuleFilter.filter_by_international_status(
            sample_scholarship, sample_student
        )

        assert is_eligible is True


class TestGenderFilter:
    """Test gender requirement filtering"""

    def test_gender_required_and_matches(self, sample_student):
        """Scholarship requires female, student is female"""
        from app.models.scholarship import Scholarship

        female_scholarship = Scholarship({
            'id': 'WOMEN',
            'name': 'Women in STEM',
            'min_gpa': 3.0,
            'eligible_courses': [9991],
            'eligible_nationalities': [],
            'gender_required': 0,  # Female
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        })

        is_eligible, message, _ = RuleFilter.filter_by_gender(female_scholarship, sample_student)

        assert is_eligible is True
        assert "matches" in message.lower() or "eligible" in message.lower()

    def test_gender_required_but_not_matches(self, low_gpa_student):
        """Scholarship requires female, student is male"""
        from app.models.scholarship import Scholarship

        female_scholarship = Scholarship({
            'id': 'WOMEN',
            'name': 'Women in STEM',
            'min_gpa': 2.0,
            'eligible_courses': [],
            'eligible_nationalities': [],
            'gender_required': 0,  # Female
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        })

        # low_gpa_student is male (gender=1)
        is_eligible, message, _ = RuleFilter.filter_by_gender(female_scholarship, low_gpa_student)

        assert is_eligible is False
        assert "does not match" in message.lower() or "required" in message.lower()


class TestApplyAllFilters:
    """Test combined filter application"""

    def test_all_filters_pass(self, sample_student, sample_scholarship):
        """Student passes all filters"""
        is_eligible, met_criteria, failed_criteria = RuleFilter.apply_all_filters(
            sample_scholarship, sample_student
        )

        assert is_eligible is True
        assert len(met_criteria) > 0
        assert len(failed_criteria) == 0

    def test_one_filter_fails(self, low_gpa_student, sample_scholarship):
        """Student fails GPA filter"""
        # low_gpa_student: 2.2, Required: 3.0
        is_eligible, met_criteria, failed_criteria = RuleFilter.apply_all_filters(
            sample_scholarship, low_gpa_student
        )

        assert is_eligible is False
        assert len(failed_criteria) > 0
        assert any("gpa" in msg.lower() for msg in failed_criteria)

    def test_expired_scholarship_fails(self, sample_student, expired_scholarship):
        """Expired scholarship fails deadline filter"""
        is_eligible, met_criteria, failed_criteria = RuleFilter.apply_all_filters(
            expired_scholarship, sample_student
        )

        assert is_eligible is False
        assert any("deadline" in msg.lower() or "expired" in msg.lower() for msg in failed_criteria)


class TestFilterScholarships:
    """Test filtering multiple scholarships"""

    def test_filter_multiple_scholarships(self, sample_student, sample_scholarship,
                                         high_gpa_scholarship, expired_scholarship):
        """Filter list of scholarships returns eligible and ineligible"""
        scholarships = [sample_scholarship, high_gpa_scholarship, expired_scholarship]

        eligible, ineligible = RuleFilter.filter_scholarships(scholarships, sample_student)

        # sample_scholarship: eligible (GPA 3.5 > 3.0)
        # high_gpa_scholarship: ineligible (GPA 3.5 < 3.7)
        # expired_scholarship: ineligible (deadline passed)

        assert len(eligible) > 0
        assert len(ineligible) > 0
        assert len(eligible) + len(ineligible) == len(scholarships)

    def test_all_scholarships_eligible(self, high_gpa_student):
        """All scholarships are eligible for high-achieving student"""
        from app.models.scholarship import Scholarship

        easy_scholarship = Scholarship({
            'id': 'EASY',
            'name': 'Easy Scholarship',
            'min_gpa': 2.0,
            'eligible_courses': [],
            'eligible_nationalities': [],
            'deadline': (datetime.now() + timedelta(days=30)).isoformat()
        })

        scholarships = [easy_scholarship]

        eligible, ineligible = RuleFilter.filter_scholarships(scholarships, high_gpa_student)

        assert len(eligible) == 1
        assert len(ineligible) == 0
