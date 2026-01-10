import sys
sys.path.insert(0, '/Users/umutturklay/dev/UE/DSS')

from app import create_app
import app as app_module
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker
from app.services.explainer import Explainer
from app.services.fairness_auditor import FairnessAuditor

print("🧪 Fairness Auditing Test\n")
print("="*60)

app = create_app()

with app.app_context():
    print("\n1️⃣  Fetching all students and scholarships...")
    students_docs = app_module.db.collection('students').limit(100).stream()
    students = [Student(doc.to_dict()) for doc in students_docs]

    scholarships_docs = app_module.db.collection('scholarships').stream()
    scholarships = [Scholarship(doc.to_dict()) for doc in scholarships_docs]

    print(f"✅ Loaded {len(students)} students")
    print(f"✅ Loaded {len(scholarships)} scholarships")

    print("\n2️⃣  Running matching for all students...")
    all_matched_results = {}

    for i, student in enumerate(students, 1):
        eligible, _ = RuleFilter.filter_scholarships(scholarships, student)
        ranked = ScholarshipRanker.rank_scholarships(eligible, student)
        matched = [Explainer.generate_match_explanation(item, student) for item in ranked]
        all_matched_results[student.student_id] = matched

        if i % 20 == 0:
            print(f"   Processed {i}/{len(students)} students...")

    print(f"✅ Matching complete for all students")

    print("\n3️⃣  Running fairness audit...")
    audit_results = FairnessAuditor.audit_by_demographic(students, all_matched_results)

    print(f"\n📊 Demographic Analysis:")
    print("-"*60)

    for group_type, group_data in audit_results['demographic_analysis'].items():
        print(f"\n{group_type.upper()}:")
        for group_value, data in group_data.items():
            print(f"  {group_value}:")
            print(f"    Students: {data['count']}")
            print(f"    Match Rate: {data['match_rate']:.3f}")
            print(f"    Total Matches: {data['total_matches']}")

    print(f"\n\n🚨 Bias Detection:")
    print("-"*60)

    if audit_results['bias_detected']:
        print(f"⚠️  {len(audit_results['bias_alerts'])} bias alert(s) detected!\n")
        for alert in audit_results['bias_alerts']:
            print(f"\n{alert['severity'].upper()} SEVERITY - {alert['group_type']}")
            print(f"  Gap: {alert['gap']*100:.1f}%")
    else:
        print(f"✅ No significant bias detected")
        print(f"   All gaps below {audit_results['threshold_used']*100}% threshold")

    print("\n\n📈 Diversity Metrics:")
    print("-"*60)

    scholarship_matches = {}
    for student_id, matches in all_matched_results.items():
        for match in matches:
            sch_id = match.scholarship.id
            if sch_id not in scholarship_matches:
                scholarship_matches[sch_id] = []
            scholarship_matches[sch_id].append(student_id)

    diversity = FairnessAuditor.calculate_diversity_score(scholarship_matches)
    print(f"   Total Unique Students Matched: {diversity['total_unique_students']}")
    print(f"   Avg Students per Scholarship: {diversity['avg_students_per_scholarship']}")
    print(f"   Diversity Score: {diversity['diversity_score']}")
    print(f"   Interpretation: {diversity['interpretation']}")

    print("\n\n📄 Fairness Report:")
    print("-"*60)
    report = FairnessAuditor.generate_fairness_report(audit_results)
    print(report)

print("\n" + "="*60)
print("✅ Fairness audit complete!")
print("="*60)
