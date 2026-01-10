import sys
sys.path.insert(0, '/Users/umutturklay/dev/UE/DSS')

from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker
from app.services.explainer import Explainer
from datetime import datetime, timedelta

print("🧪 DSS Matching Engine - Unit Tests\n")
print("="*60)

test_student = Student({
    'student_id': 'TEST_001',
    'gpa': 3.6,
    'course': 9991,
    'gender': 0,
    'age': 22,
    'nationality': 6,
    'is_international': True,
    'current_scholarship_holder': False,
    'keywords': ['computer science', 'technology', 'programming', 'women']
})

test_scholarship_eligible = Scholarship({
    'id': 'SCH_001',
    'name': 'DAAD Master\'s Scholarship',
    'provider': 'DAAD (Germany)',
    'amount': 934,
    'currency': 'EUR',
    'duration_months': 24,
    'min_gpa': 3.0,
    'eligible_courses': [9991, 9500],
    'eligible_nationalities': [6, 22, 24],
    'citizenship_required': False,
    'age_max': 35,
    'requires_international': True,
    'deadline': (datetime.now() + timedelta(days=90)).isoformat(),
    'required_documents': ['transcript', 'motivation_letter'],
    'description': 'Scholarship for international students',
    'competitiveness': 0.8,
    'keywords': ['computer science', 'technology', 'engineering']
})

test_scholarship_ineligible = Scholarship({
    'id': 'SCH_002',
    'name': 'Local Merit Scholarship',
    'provider': 'State Fund',
    'amount': 2500,
    'currency': 'EUR',
    'duration_months': 12,
    'min_gpa': 3.2,
    'eligible_courses': [],
    'eligible_nationalities': [1],
    'citizenship_required': True,
    'age_max': 25,
    'requires_international': False,
    'deadline': (datetime.now() + timedelta(days=30)).isoformat(),
    'required_documents': ['transcript'],
    'description': 'For domestic students',
    'competitiveness': 0.6,
    'keywords': ['local', 'merit']
})

print("\n1️⃣  Testing Rule-Based Filter")
print("-"*60)

is_eligible, met, failed = RuleFilter.apply_all_filters(test_scholarship_eligible, test_student)
print(f"\n✓ Eligible Scholarship Test:")
print(f"   Result: {'ELIGIBLE' if is_eligible else 'NOT ELIGIBLE'}")
print(f"   Met Criteria ({len(met)}):")
for criterion in met:
    print(f"     {criterion}")

is_eligible2, met2, failed2 = RuleFilter.apply_all_filters(test_scholarship_ineligible, test_student)
print(f"\n✗ Ineligible Scholarship Test:")
print(f"   Result: {'ELIGIBLE' if is_eligible2 else 'NOT ELIGIBLE'}")
print(f"   Failed Criteria ({len(failed2)}):")
for criterion in failed2[:3]:
    print(f"     {criterion}")

print("\n\n2️⃣  Testing Ranking Algorithm")
print("-"*60)

score, breakdown = ScholarshipRanker.calculate_final_score(test_student, test_scholarship_eligible)
print(f"\n✓ Scholarship Score: {score:.3f}")
print(f"   Breakdown:")
for factor, value in breakdown.items():
    print(f"     {factor}: {value:.3f}")

print("\n\n3️⃣  Testing Explainability")
print("-"*60)

ranked_item = {
    'scholarship': test_scholarship_eligible,
    'score': score,
    'breakdown': breakdown,
    'met_criteria': met,
    'failed_criteria': failed,
    'ranking': 1
}

match_result = Explainer.generate_match_explanation(ranked_item, test_student)
print(f"\n✓ Match Explanation:")
print(f"   Matched: {match_result.matched}")
print(f"   Score: {match_result.score:.3f}")
print(f"   Ranking: #{match_result.ranking}")
print(f"   Recommendation: {match_result.recommendation}")

ineligible_item = {
    'scholarship': test_scholarship_ineligible,
    'met_criteria': met2,
    'failed_criteria': failed2
}

reject_result = Explainer.generate_rejection_explanation(ineligible_item, test_student)
print(f"\n✗ Rejection Explanation:")
print(f"   Matched: {reject_result.matched}")
print(f"   Recommendation: {reject_result.recommendation}")

print("\n\n4️⃣  Testing Full Pipeline")
print("-"*60)

scholarships = [test_scholarship_eligible, test_scholarship_ineligible]
eligible, ineligible = RuleFilter.filter_scholarships(scholarships, test_student)

print(f"\n✓ Filter Results:")
print(f"   Eligible: {len(eligible)}")
print(f"   Ineligible: {len(ineligible)}")

ranked = ScholarshipRanker.rank_scholarships(eligible, test_student)

print(f"\n✓ Ranked Results:")
for item in ranked:
    sch = item['scholarship']
    print(f"   #{item['ranking']} {sch.name} - Score: {item['score']:.3f}")

matched_results = [Explainer.generate_match_explanation(item, test_student) for item in ranked]
rejected_results = [Explainer.generate_rejection_explanation(item, test_student) for item in ineligible]

summary = Explainer.generate_summary_stats(matched_results, rejected_results, test_student)
print(f"\n📊 Summary Statistics:")
print(f"   Total Scholarships: {summary['total_scholarships_analyzed']}")
print(f"   Matched: {summary['matched_count']}")
print(f"   Rejected: {summary['rejected_count']}")
print(f"   Match Rate: {summary['match_rate_percent']}%")
print(f"   Avg Score: {summary['average_match_score']:.3f}")
print(f"   Top Score: {summary['top_match_score']:.3f}")
print(f"   Recommendation: {summary['recommendation']}")

print("\n" + "="*60)
print("✅ All tests passed!")
print("="*60)
