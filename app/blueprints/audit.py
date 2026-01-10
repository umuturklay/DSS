from flask import Blueprint, render_template, request, jsonify
import app as app_module
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker
from app.services.explainer import Explainer
from app.services.fairness_auditor import FairnessAuditor

bp = Blueprint('audit', __name__, url_prefix='/audit')

@bp.route('/', methods=['GET'])
def index():
    """
    Run fairness audit across all students and scholarships.

    Returns:
        HTML (if browser request) or JSON (if API request)
    """
    try:
        students_docs = app_module.db.collection('students').stream()
        students = [Student(doc.to_dict()) for doc in students_docs]

        scholarships_docs = app_module.db.collection('scholarships').stream()
        scholarships = [Scholarship(doc.to_dict()) for doc in scholarships_docs]

        all_matched_results = {}

        for student in students:
            eligible, _ = RuleFilter.filter_scholarships(scholarships, student)
            ranked = ScholarshipRanker.rank_scholarships(eligible, student)
            matched = [Explainer.generate_match_explanation(item, student) for item in ranked]

            all_matched_results[student.student_id] = matched

        audit_results = FairnessAuditor.audit_by_demographic(students, all_matched_results)

        fairness_report = FairnessAuditor.generate_fairness_report(audit_results)

        scholarship_matches = {}
        for student_id, matches in all_matched_results.items():
            for match in matches:
                sch_id = match.scholarship.id
                if sch_id not in scholarship_matches:
                    scholarship_matches[sch_id] = []
                scholarship_matches[sch_id].append(student_id)

        diversity_metrics = FairnessAuditor.calculate_diversity_score(scholarship_matches)

        # Return JSON if requested via Accept header or query param
        if request.args.get('format') == 'json' or request.headers.get('Accept') == 'application/json':
            return jsonify({
                'success': True,
                'total_students_analyzed': len(students),
                'total_scholarships_analyzed': len(scholarships),
                'audit_results': audit_results,
                'diversity_metrics': diversity_metrics,
                'fairness_report': fairness_report
            })

        # Otherwise render HTML template
        return render_template('audit.html',
                             total_students=len(students),
                             total_scholarships=len(scholarships),
                             audit_results={'demographic_analysis': audit_results['demographic_analysis']},
                             bias_detected=audit_results['bias_detected'],
                             bias_alerts=audit_results['bias_alerts'],
                             threshold=audit_results['threshold_used'],
                             diversity_metrics=diversity_metrics)

    except Exception as e:
        if request.args.get('format') == 'json' or request.headers.get('Accept') == 'application/json':
            return jsonify({'error': str(e)}), 500
        return f'<div class="text-red-600 p-4">Error: {str(e)}</div>', 500
