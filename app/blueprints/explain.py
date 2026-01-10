from flask import Blueprint, render_template, request, jsonify
import app as app_module
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker
from app.services.explainer import Explainer

bp = Blueprint('explain', __name__, url_prefix='/explain')

@bp.route('/<scholarship_id>/<student_id>', methods=['GET'])
def explain_match(scholarship_id, student_id):
    """
    Detailed explanation for why a student matched/didn't match a scholarship.

    Args:
        scholarship_id: Scholarship document ID
        student_id: Student document ID

    Returns:
        JSON with detailed explanation, criteria checklist, scoring breakdown
    """
    try:
        student_doc = app_module.db.collection('students').document(student_id).get()
        if not student_doc.exists:
            return jsonify({'error': 'Student not found'}), 404
        student = Student(student_doc.to_dict())

        scholarship_doc = app_module.db.collection('scholarships').document(scholarship_id).get()
        if not scholarship_doc.exists:
            return jsonify({'error': 'Scholarship not found'}), 404
        scholarship = Scholarship(scholarship_doc.to_dict())

        is_eligible, met_criteria, failed_criteria = RuleFilter.apply_all_filters(scholarship, student)

        if is_eligible:
            score, breakdown = ScholarshipRanker.calculate_final_score(student, scholarship)
            ranked_item = {
                'scholarship': scholarship,
                'score': score,
                'breakdown': breakdown,
                'met_criteria': met_criteria,
                'failed_criteria': failed_criteria,
                'ranking': 1
            }
            result = Explainer.generate_match_explanation(ranked_item, student)
        else:
            ineligible_item = {
                'scholarship': scholarship,
                'met_criteria': met_criteria,
                'failed_criteria': failed_criteria
            }
            result = Explainer.generate_rejection_explanation(ineligible_item, student)

        return jsonify({
            'success': True,
            'explanation': result.to_dict()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Use /explain/<scholarship_id>/<student_id> to get detailed explanation"
    })
