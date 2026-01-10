"""
Validation Script - Match Quality (Precision) Measurement

This script validates the DSS recommendation accuracy by comparing
top-N recommendations against manually verified ground truth.

Target: ≥80% precision (Professor's requirement)

Usage:
    python scripts/validate_precision.py
"""

import sys
import os
import json
import csv
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import firebase_admin
from firebase_admin import credentials, firestore
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker


# Initialize Firebase
if not firebase_admin._apps:
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Test Student Profiles with Ground Truth
# Ground truth is manually determined by expert review of scholarship criteria
TEST_STUDENTS = [
    {
        'id': 'TEST001',
        'student_id': 'TEST001',
        'name': 'High GPA CS Female International',
        'gpa': 3.6,
        'course': 9991,  # Computer Science
        'gender': 0,  # Female
        'age': 23,
        'is_international': True,
        'nationality': 6,  # Not nationality 1 (local)
        'current_scholarship_holder': False,
        'keywords': ['computer science', 'technology', 'engineering'],
        'expected_scholarships': [
            'DAAD Master\'s Scholarship',  # ✓ GPA 3.6 > 3.0, CS, international
            'Women in STEM Scholarship',   # ✓ GPA 3.6 > 3.0, CS (STEM), female
            'UE Excellence Scholarship',   # ✓ GPA 3.6 > 3.5, CS
            'Erasmus+ Mobility Grant',     # ✓ GPA 3.6 > 2.5, age < 30
            'TURKIYE Scholarship'          # ✓ GPA 3.6 > 2.8, international
        ]
    },
    {
        'id': 'TEST002',
        'student_id': 'TEST002',
        'name': 'Mid GPA Business Male Local',
        'gpa': 2.9,
        'course': 9773,  # Business
        'gender': 1,  # Male
        'age': 21,
        'is_international': False,
        'nationality': 1,  # Local
        'current_scholarship_holder': False,
        'keywords': ['business', 'economics', 'management'],
        'expected_scholarships': [
            'Business & Economics Grant',  # ✓ GPA 2.9 > 2.8, business course
            'Erasmus+ Mobility Grant',     # ✓ GPA 2.9 > 2.5, age < 30
            'Need-Based Financial Aid',    # ✓ GPA 2.9 > 2.3
            'Sports Excellence Scholarship' # ✓ GPA 2.9 > 2.0
        ]
    },
    {
        'id': 'TEST003',
        'student_id': 'TEST003',
        'name': 'Low GPA Engineering Male International',
        'gpa': 2.4,
        'course': 9500,  # Engineering
        'gender': 1,  # Male
        'age': 24,
        'is_international': True,
        'nationality': 22,
        'current_scholarship_holder': False,
        'keywords': ['engineering', 'technology'],
        'expected_scholarships': [
            'Need-Based Financial Aid',     # ✓ GPA 2.4 > 2.3
            'Sports Excellence Scholarship' # ✓ GPA 2.4 > 2.0
        ]
    },
    {
        'id': 'TEST004',
        'student_id': 'TEST004',
        'name': 'Very High GPA CS Female Local',
        'gpa': 3.8,
        'course': 9991,  # Computer Science
        'gender': 0,  # Female
        'age': 22,
        'is_international': False,
        'nationality': 1,  # Local
        'current_scholarship_holder': True,
        'keywords': ['computer science', 'technology', 'AI'],
        'expected_scholarships': [
            'UE Excellence Scholarship',    # ✓ GPA 3.8 > 3.5, CS
            'Women in STEM Scholarship',    # ✓ GPA 3.8 > 3.0, CS, female
            'Local Merit Scholarship',      # ✓ GPA 3.8 > 3.2, citizenship
            'Erasmus+ Mobility Grant',      # ✓ GPA 3.8 > 2.5
            'Need-Based Financial Aid'      # ✓ GPA 3.8 > 2.3
        ]
    },
    {
        'id': 'TEST005',
        'student_id': 'TEST005',
        'name': 'Upper-Mid GPA CS Male International',
        'gpa': 3.3,
        'course': 9991,  # Computer Science
        'gender': 1,  # Male
        'age': 25,
        'is_international': True,
        'nationality': 24,
        'current_scholarship_holder': False,
        'keywords': ['computer science', 'software', 'engineering'],
        'expected_scholarships': [
            'DAAD Master\'s Scholarship',  # ✓ GPA 3.3 > 3.0, CS, international
            'TURKIYE Scholarship',         # ✓ GPA 3.3 > 2.8, international
            'Erasmus+ Mobility Grant',     # ✓ GPA 3.3 > 2.5
            'Need-Based Financial Aid'     # ✓ GPA 3.3 > 2.3
        ]
    },
    {
        'id': 'TEST006',
        'student_id': 'TEST006',
        'name': 'Low GPA Business Female Local',
        'gpa': 2.6,
        'course': 9853,  # Economics
        'gender': 0,  # Female
        'age': 20,
        'is_international': False,
        'nationality': 1,
        'current_scholarship_holder': False,
        'keywords': ['economics', 'business', 'finance'],
        'expected_scholarships': [
            'Erasmus+ Mobility Grant',      # ✓ GPA 2.6 > 2.5
            'Need-Based Financial Aid',     # ✓ GPA 2.6 > 2.3
            'Sports Excellence Scholarship' # ✓ GPA 2.6 > 2.0
        ]
    },
    {
        'id': 'TEST007',
        'student_id': 'TEST007',
        'name': 'High GPA Engineering Female International',
        'gpa': 3.4,
        'course': 9500,  # Engineering
        'gender': 0,  # Female
        'age': 23,
        'is_international': True,
        'nationality': 26,
        'current_scholarship_holder': False,
        'keywords': ['engineering', 'technology', 'design'],
        'expected_scholarships': [
            'DAAD Master\'s Scholarship',  # ✓ GPA 3.4 > 3.0, Engineering, international
            'Women in STEM Scholarship',   # ✓ GPA 3.4 > 3.0, Engineering (STEM), female
            'TURKIYE Scholarship',         # ✓ GPA 3.4 > 2.8, international
            'Erasmus+ Mobility Grant',     # ✓ GPA 3.4 > 2.5
            'Need-Based Financial Aid'     # ✓ GPA 3.4 > 2.3
        ]
    },
    {
        'id': 'TEST008',
        'student_id': 'TEST008',
        'name': 'Mid GPA Random Course Male Local',
        'gpa': 2.7,
        'course': 9254,  # Some other course
        'gender': 1,  # Male
        'age': 22,
        'is_international': False,
        'nationality': 1,
        'current_scholarship_holder': False,
        'keywords': ['general', 'studies'],
        'expected_scholarships': [
            'Erasmus+ Mobility Grant',      # ✓ GPA 2.7 > 2.5
            'Need-Based Financial Aid',     # ✓ GPA 2.7 > 2.3
            'Sports Excellence Scholarship' # ✓ GPA 2.7 > 2.0
        ]
    },
    {
        'id': 'TEST009',
        'student_id': 'TEST009',
        'name': 'High GPA Business Male Local',
        'gpa': 3.3,
        'course': 9773,  # Business
        'gender': 1,  # Male
        'age': 24,
        'is_international': False,
        'nationality': 1,
        'current_scholarship_holder': True,
        'keywords': ['business', 'management', 'entrepreneurship'],
        'expected_scholarships': [
            'Local Merit Scholarship',      # ✓ GPA 3.3 > 3.2, citizenship
            'Business & Economics Grant',   # ✓ GPA 3.3 > 2.8, business
            'Erasmus+ Mobility Grant',      # ✓ GPA 3.3 > 2.5
            'Need-Based Financial Aid'      # ✓ GPA 3.3 > 2.3
        ]
    },
    {
        'id': 'TEST010',
        'student_id': 'TEST010',
        'name': 'Very High GPA CS Female International Refugee',
        'gpa': 3.9,
        'course': 9991,  # Computer Science
        'gender': 0,  # Female
        'age': 26,
        'is_international': True,
        'nationality': 62,  # Refugee-eligible nationality
        'current_scholarship_holder': False,
        'keywords': ['computer science', 'AI', 'machine learning'],
        'expected_scholarships': [
            'UE Excellence Scholarship',    # ✓ GPA 3.9 > 3.5, CS
            'DAAD Master\'s Scholarship',   # ✓ GPA 3.9 > 3.0, CS, international
            'Women in STEM Scholarship',    # ✓ GPA 3.9 > 3.0, CS, female
            'TURKIYE Scholarship',          # ✓ GPA 3.9 > 2.8, international
            'Refugee Support Scholarship'   # ✓ GPA 3.9 > 2.0, refugee nationality
        ]
    }
]


def get_top_n_recommendations(student_data, n=5):
    """
    Get top-N scholarship recommendations from DSS for a student.

    Args:
        student_data: Student profile dict
        n: Number of top recommendations to return

    Returns:
        List of scholarship names
    """
    student = Student(student_data)

    # Fetch all scholarships from Firestore
    scholarships_docs = db.collection('scholarships').stream()
    scholarships = [Scholarship(doc.to_dict()) for doc in scholarships_docs]

    # Apply rule filter
    eligible, ineligible = RuleFilter.filter_scholarships(scholarships, student)

    # Rank eligible scholarships
    ranked = ScholarshipRanker.rank_scholarships(eligible, student)

    # Extract top-N scholarship names
    top_n = [item['scholarship'].name for item in ranked[:n]]

    return top_n


def calculate_precision(predicted, expected):
    """
    Calculate precision: (True Positives) / (All Predicted)

    Args:
        predicted: List of predicted scholarship names
        expected: List of expected (ground truth) scholarship names

    Returns:
        Tuple of (precision, correct_count, total_predicted)
    """
    if not predicted:
        return 0.0, 0, 0

    correct = 0
    for scholarship in predicted:
        if scholarship in expected:
            correct += 1

    precision = correct / len(predicted)
    return precision, correct, len(predicted)


def run_validation(n=5, verbose=True):
    """
    Run validation on all test students.

    Args:
        n: Number of top recommendations to evaluate
        verbose: Print detailed results

    Returns:
        Dict with validation results
    """
    results = []

    print(f"\n{'='*70}")
    print(f"SCHOLARSHIP MATCHING DSS - PRECISION VALIDATION")
    print(f"{'='*70}")
    print(f"Evaluating top-{n} recommendations for {len(TEST_STUDENTS)} test students\n")

    for i, test_student in enumerate(TEST_STUDENTS, 1):
        if verbose:
            print(f"{i}. {test_student['name']}")
            print(f"   Profile: GPA {test_student['gpa']}, Age {test_student['age']}, "
                  f"{'International' if test_student['is_international'] else 'Local'}, "
                  f"{'Female' if test_student['gender'] == 0 else 'Male'}")

        # Get DSS predictions
        predicted = get_top_n_recommendations(test_student, n=n)
        expected = test_student['expected_scholarships']

        # Calculate precision
        precision, correct, total = calculate_precision(predicted, expected)

        # Store result
        result = {
            'student_id': test_student['id'],
            'student_name': test_student['name'],
            'predicted': predicted,
            'expected': expected,
            'precision': precision,
            'correct': correct,
            'total': total
        }
        results.append(result)

        if verbose:
            print(f"   Predicted ({len(predicted)}): {predicted[:3]}{'...' if len(predicted) > 3 else ''}")
            print(f"   Expected ({len(expected)}):  {expected[:3]}{'...' if len(expected) > 3 else ''}")
            print(f"   ✓ Precision: {precision:.1%} ({correct}/{total} correct)")

            # Show mismatches
            wrong = [s for s in predicted if s not in expected]
            if wrong:
                print(f"   ✗ False Positives: {wrong}")
            print()

    # Calculate overall metrics
    avg_precision = sum(r['precision'] for r in results) / len(results)
    total_correct = sum(r['correct'] for r in results)
    total_predicted = sum(r['total'] for r in results)

    print(f"{'='*70}")
    print(f"OVERALL RESULTS")
    print(f"{'='*70}")
    print(f"Average Precision: {avg_precision:.1%}")
    print(f"Total Correct: {total_correct}/{total_predicted}")
    print(f"Target: ≥80%")

    if avg_precision >= 0.80:
        print(f"Status: ✅ TARGET ACHIEVED")
    else:
        gap = 0.80 - avg_precision
        print(f"Status: ❌ BELOW TARGET (need {gap:.1%} improvement)")

    print(f"{'='*70}\n")

    return {
        'results': results,
        'avg_precision': avg_precision,
        'total_correct': total_correct,
        'total_predicted': total_predicted,
        'target_met': avg_precision >= 0.80,
        'timestamp': datetime.now().isoformat()
    }


def export_results(validation_results, output_dir='data/validation'):
    """
    Export validation results to CSV and JSON.

    Args:
        validation_results: Results dict from run_validation()
        output_dir: Directory to save output files
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Export to CSV
    csv_path = os.path.join(output_dir, f'precision_validation_{timestamp}.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'student_id', 'student_name', 'precision', 'correct', 'total',
            'predicted', 'expected'
        ])
        writer.writeheader()

        for result in validation_results['results']:
            writer.writerow({
                'student_id': result['student_id'],
                'student_name': result['student_name'],
                'precision': f"{result['precision']:.1%}",
                'correct': result['correct'],
                'total': result['total'],
                'predicted': '; '.join(result['predicted']),
                'expected': '; '.join(result['expected'])
            })

    print(f"✓ CSV exported to: {csv_path}")

    # Export to JSON
    json_path = os.path.join(output_dir, f'precision_validation_{timestamp}.json')
    with open(json_path, 'w') as f:
        json.dump(validation_results, f, indent=2)

    print(f"✓ JSON exported to: {json_path}")

    # Export summary for report
    summary_path = os.path.join(output_dir, f'precision_summary_{timestamp}.txt')
    with open(summary_path, 'w') as f:
        f.write("SCHOLARSHIP MATCHING DSS - PRECISION VALIDATION SUMMARY\n")
        f.write("="*70 + "\n\n")
        f.write(f"Date: {validation_results['timestamp']}\n")
        f.write(f"Test Students: {len(validation_results['results'])}\n")
        f.write(f"Top-N Evaluated: 5\n\n")
        f.write(f"Average Precision: {validation_results['avg_precision']:.1%}\n")
        f.write(f"Total Correct: {validation_results['total_correct']}/{validation_results['total_predicted']}\n")
        f.write(f"Target: ≥80%\n")
        f.write(f"Status: {'✅ ACHIEVED' if validation_results['target_met'] else '❌ NOT MET'}\n\n")

        f.write("Per-Student Results:\n")
        f.write("-"*70 + "\n")
        for result in validation_results['results']:
            f.write(f"{result['student_name']}: {result['precision']:.1%} "
                   f"({result['correct']}/{result['total']})\n")

    print(f"✓ Summary exported to: {summary_path}\n")


if __name__ == '__main__':
    # Run validation
    results = run_validation(n=5, verbose=True)

    # Export results
    export_results(results)

    print("Validation complete! Use these results in your report's 'Match Quality' section.")
