from datetime import datetime
from app.models.student import Student
from app.models.scholarship import Scholarship

class RuleFilter:
    """
    Rule-based filtering engine for scholarship eligibility.
    Based on Noviyanto (2023) - transparent, auditable DSS approach.
    """

    @staticmethod
    def filter_by_gpa(scholarship, student):
        """Check if student meets minimum GPA requirement"""
        if student.gpa >= scholarship.min_gpa:
            return True, f"✓ GPA {student.gpa:.2f} meets minimum {scholarship.min_gpa:.2f} (+{student.gpa - scholarship.min_gpa:.2f} buffer)"
        else:
            return False, f"✗ GPA {student.gpa:.2f} below minimum {scholarship.min_gpa:.2f} (need +{scholarship.min_gpa - student.gpa:.2f})"

    @staticmethod
    def filter_by_course(scholarship, student):
        """Check if student's course is eligible"""
        if not scholarship.eligible_courses:
            return True, "✓ All courses eligible"

        if student.course in scholarship.eligible_courses:
            return True, f"✓ Course {student.course} is eligible"
        else:
            return False, f"✗ Course {student.course} not in eligible list {scholarship.eligible_courses}"

    @staticmethod
    def filter_by_nationality(scholarship, student):
        """Check if student's nationality is eligible"""
        if not scholarship.eligible_nationalities:
            return True, "✓ All nationalities eligible"

        if student.nationality in scholarship.eligible_nationalities:
            return True, f"✓ Nationality {student.nationality} is eligible"
        else:
            return False, f"✗ Nationality {student.nationality} not eligible (accepted: {scholarship.eligible_nationalities})"

    @staticmethod
    def filter_by_deadline(scholarship):
        """Check if scholarship deadline has not passed"""
        if not scholarship.deadline:
            return True, "✓ No deadline (rolling admission)"

        try:
            deadline_date = datetime.fromisoformat(scholarship.deadline.replace('Z', '+00:00'))
            now = datetime.now(deadline_date.tzinfo)

            if now < deadline_date:
                days_left = (deadline_date - now).days
                return True, f"✓ Deadline {scholarship.deadline[:10]} ({days_left} days remaining)"
            else:
                return False, f"✗ Deadline {scholarship.deadline[:10]} has passed"
        except:
            return True, "✓ Deadline not specified"

    @staticmethod
    def filter_by_age(scholarship, student):
        """Check if student meets age requirement"""
        if student.age <= scholarship.age_max:
            return True, f"✓ Age {student.age} within limit (max {scholarship.age_max})"
        else:
            return False, f"✗ Age {student.age} exceeds maximum {scholarship.age_max}"

    @staticmethod
    def filter_by_international_status(scholarship, student):
        """Check if international status requirement is met"""
        if scholarship.requires_international is None:
            return True, "✓ International status not required"

        if scholarship.requires_international == student.is_international:
            status = "international" if student.is_international else "domestic"
            return True, f"✓ {status.capitalize()} student (as required)"
        else:
            required = "international" if scholarship.requires_international else "domestic"
            actual = "international" if student.is_international else "domestic"
            return False, f"✗ Requires {required} student (you are {actual})"

    @staticmethod
    def filter_by_gender(scholarship, student):
        """Check if gender requirement is met"""
        if scholarship.gender_required is None:
            return True, "✓ Gender not restricted"

        if scholarship.gender_required == student.gender:
            gender_name = "Female" if student.gender == 0 else "Male"
            return True, f"✓ Gender requirement met ({gender_name})"
        else:
            required_gender = "Female" if scholarship.gender_required == 0 else "Male"
            actual_gender = "Female" if student.gender == 0 else "Male"
            return False, f"✗ Requires {required_gender} (you are {actual_gender})"

    @staticmethod
    def filter_by_citizenship(scholarship, student):
        """Check if citizenship requirement is met"""
        if not scholarship.citizenship_required:
            return True, "✓ Citizenship not required"

        if not student.is_international:
            return True, "✓ Citizenship requirement met (domestic student)"
        else:
            return False, "✗ Citizenship required (you are international student)"

    @staticmethod
    def apply_all_filters(scholarship, student):
        """
        Apply all eligibility rules and return result.

        Returns:
            tuple: (is_eligible: bool, met_criteria: list, failed_criteria: list)
        """
        filters = [
            RuleFilter.filter_by_gpa,
            RuleFilter.filter_by_course,
            RuleFilter.filter_by_nationality,
            lambda s, st: RuleFilter.filter_by_deadline(s),
            RuleFilter.filter_by_age,
            RuleFilter.filter_by_international_status,
            RuleFilter.filter_by_gender,
            RuleFilter.filter_by_citizenship
        ]

        met_criteria = []
        failed_criteria = []
        is_eligible = True

        for filter_func in filters:
            try:
                if filter_func.__name__ == '<lambda>':
                    passed, message = filter_func(scholarship, student)
                else:
                    passed, message = filter_func(scholarship, student)

                if passed:
                    met_criteria.append(message)
                else:
                    failed_criteria.append(message)
                    is_eligible = False
            except Exception as e:
                failed_criteria.append(f"✗ Error checking criterion: {str(e)}")
                is_eligible = False

        return is_eligible, met_criteria, failed_criteria

    @staticmethod
    def filter_scholarships(scholarships, student):
        """
        Filter list of scholarships for a student.

        Returns:
            tuple: (eligible: list, ineligible: list)
        """
        eligible = []
        ineligible = []

        for scholarship in scholarships:
            is_eligible, met, failed = RuleFilter.apply_all_filters(scholarship, student)

            result = {
                'scholarship': scholarship,
                'met_criteria': met,
                'failed_criteria': failed
            }

            if is_eligible:
                eligible.append(result)
            else:
                ineligible.append(result)

        return eligible, ineligible
