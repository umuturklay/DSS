"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.student import Student
from app.models.scholarship import Scholarship
from datetime import datetime, timedelta


@pytest.fixture
def sample_student():
    """Sample student profile for testing"""
    return Student({
        'student_id': 'TEST001',
        'gpa': 3.5,
        'course': 9991,  # Computer Science
        'gender': 0,  # Female
        'age': 23,
        'is_international': True,
        'nationality': 6,
        'current_scholarship_holder': False,
        'keywords': ['computer science', 'technology', 'engineering']
    })


@pytest.fixture
def high_gpa_student():
    """High GPA student for testing"""
    return Student({
        'student_id': 'TEST_HIGH',
        'gpa': 3.8,
        'course': 9991,
        'gender': 0,
        'age': 22,
        'is_international': False,
        'nationality': 1,
        'current_scholarship_holder': False,
        'keywords': ['computer science', 'AI']
    })


@pytest.fixture
def low_gpa_student():
    """Low GPA student for testing"""
    return Student({
        'student_id': 'TEST_LOW',
        'gpa': 2.2,
        'course': 9773,  # Business
        'gender': 1,  # Male
        'age': 21,
        'is_international': False,
        'nationality': 1,
        'current_scholarship_holder': False,
        'keywords': ['business', 'economics']
    })


@pytest.fixture
def sample_scholarship():
    """Sample scholarship for testing"""
    future_deadline = (datetime.now() + timedelta(days=60)).isoformat()
    return Scholarship({
        'id': 'SCH001',
        'name': 'Test Scholarship',
        'provider': 'Test University',
        'amount': 5000,
        'currency': 'EUR',
        'min_gpa': 3.0,
        'eligible_courses': [9991, 9500],
        'eligible_nationalities': [1, 6, 22],
        'citizenship_required': False,
        'age_max': 30,
        'requires_international': False,
        'deadline': future_deadline,
        'competitiveness': 0.7,
        'keywords': ['computer science', 'technology'],
        'required_documents': ['transcript', 'essay']
    })


@pytest.fixture
def high_gpa_scholarship():
    """Scholarship requiring high GPA"""
    future_deadline = (datetime.now() + timedelta(days=90)).isoformat()
    return Scholarship({
        'id': 'SCH_HIGH',
        'name': 'Excellence Scholarship',
        'provider': 'Test University',
        'amount': 10000,
        'currency': 'EUR',
        'min_gpa': 3.7,
        'eligible_courses': [],
        'eligible_nationalities': [],
        'citizenship_required': False,
        'age_max': 28,
        'requires_international': False,
        'deadline': future_deadline,
        'competitiveness': 0.9,
        'keywords': ['excellence', 'merit'],
        'required_documents': ['transcript']
    })


@pytest.fixture
def international_scholarship():
    """Scholarship for international students only"""
    future_deadline = (datetime.now() + timedelta(days=120)).isoformat()
    return Scholarship({
        'id': 'SCH_INTL',
        'name': 'International Scholarship',
        'provider': 'Global Foundation',
        'amount': 8000,
        'currency': 'EUR',
        'min_gpa': 3.0,
        'eligible_courses': [],
        'eligible_nationalities': [6, 22, 24, 26],
        'citizenship_required': False,
        'age_max': 35,
        'requires_international': True,
        'deadline': future_deadline,
        'competitiveness': 0.6,
        'keywords': ['international', 'diversity'],
        'required_documents': ['transcript', 'passport']
    })


@pytest.fixture
def expired_scholarship():
    """Scholarship with expired deadline"""
    past_deadline = (datetime.now() - timedelta(days=10)).isoformat()
    return Scholarship({
        'id': 'SCH_EXPIRED',
        'name': 'Expired Scholarship',
        'provider': 'Test University',
        'amount': 3000,
        'currency': 'EUR',
        'min_gpa': 2.5,
        'eligible_courses': [],
        'eligible_nationalities': [],
        'citizenship_required': False,
        'age_max': 30,
        'requires_international': False,
        'deadline': past_deadline,
        'competitiveness': 0.5,
        'keywords': ['general'],
        'required_documents': ['transcript']
    })
