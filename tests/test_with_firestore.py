import sys
sys.path.insert(0, '/Users/umutturklay/dev/UE/DSS')

from app import create_app
import app as app_module
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker
from app.services.explainer import Explainer

print("🧪 DSS with Real Firestore Data\n")
print("="*60)

application = create_app()

with application.app_context():
    print("\n1️⃣  Fetching student from Firestore...")
    student_doc = app_module.db.collection('students').document('STU_00000').get()

    if not student_doc.exists:
        print("❌ Student not found")
        exit(1)

    student = Student(student_doc.to_dict())
    print(f"✅ Student loaded: {student.student_id}")
    print(f"   GPA: {student.gpa}")
    print(f"   Course: {student.course}")
    print(f"   International: {student.is_international}")

    print("\n2️⃣  Fetching scholarships from Firestore...")
    scholarships_docs = app_module.db.collection('scholarships').stream()
    scholarships = [Scholarship(doc.to_dict()) for doc in scholarships_docs]
    print(f"✅ {len(scholarships)} scholarships loaded")

    print("\n3️⃣  Running matching engine...")
    eligible, ineligible = RuleFilter.filter_scholarships(scholarships, student)
    print(f"   Eligible: {len(eligible)}")
    print(f"   Ineligible: {len(ineligible)}")

    print("\n4️⃣  Ranking scholarships...")
    ranked = ScholarshipRanker.rank_scholarships(eligible, student)

    print(f"\n🎯 Top 5 Matches:")
    print("-"*60)
    for item in ranked[:5]:
        sch = item['scholarship']
        print(f"\n   #{item['ranking']} {sch.name}")
        print(f"      Provider: {sch.provider}")
        print(f"      Amount: €{sch.amount}")
        print(f"      Score: {item['score']:.3f}")
        print(f"      Min GPA: {sch.min_gpa}")

    print("\n\n5️⃣  Generating explanations...")
    matched_results = [Explainer.generate_match_explanation(item, student) for item in ranked]
    rejected_results = [Explainer.generate_rejection_explanation(item, student) for item in ineligible]

    if matched_results:
        top_match = matched_results[0]
        print(f"\n✅ Top Match Details:")
        print(f"   {top_match.scholarship.name}")
        print(f"   Score: {top_match.score:.3f}")
        print(f"   Recommendation: {top_match.recommendation}")
        print(f"\n   Met Criteria:")
        for criterion in top_match.met_criteria[:4]:
            print(f"     {criterion}")

    if rejected_results:
        print(f"\n\n❌ Sample Rejection:")
        reject = rejected_results[0]
        print(f"   {reject.scholarship.name}")
        print(f"   Recommendation: {reject.recommendation}")
        print(f"\n   Failed Criteria:")
        for criterion in reject.failed_criteria[:3]:
            print(f"     {criterion}")

    summary = Explainer.generate_summary_stats(matched_results, rejected_results, student)
    print(f"\n\n📊 Summary:")
    print("-"*60)
    print(f"   Total Scholarships Analyzed: {summary['total_scholarships_analyzed']}")
    print(f"   Matched: {summary['matched_count']}")
    print(f"   Rejected: {summary['rejected_count']}")
    print(f"   Match Rate: {summary['match_rate_percent']}%")
    print(f"   Average Match Score: {summary['average_match_score']:.3f}")
    print(f"   Top Match Score: {summary['top_match_score']:.3f}")
    print(f"\n   Recommendation:")
    print(f"   {summary['recommendation']}")

print("\n" + "="*60)
print("✅ Firestore integration test complete!")
print("="*60)
