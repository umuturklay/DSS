from flask import Blueprint, render_template, request, jsonify
import app as app_module
from app.models.student import Student
from app.models.scholarship import Scholarship
from app.services.rule_filter import RuleFilter
from app.services.ranker import ScholarshipRanker
from app.services.explainer import Explainer
import time

bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return match_student()

    students_docs = app_module.db.collection('students').order_by('gpa', direction='DESCENDING').stream()
    students = []
    for doc in students_docs:
        data = doc.to_dict()
        students.append({
            'id': data.get('student_id'),
            'gpa': data.get('gpa', 0),
            'course': data.get('course', 0),
            'gender': 'Female' if data.get('gender') == 0 else 'Male',
            'age': data.get('age', 0),
            'is_international': data.get('is_international', False)
        })

    return render_template('match.html', students=students)

@bp.route('/api', methods=['POST'])
def match_student():
    """
    Main matching endpoint - processes student profile and returns ranked scholarships.

    Input (Form or JSON):
        - student_id: str (to fetch from Firestore)
        OR
        - student_profile: dict (direct profile data)

    Output:
        - HTML (if HTMX request)
        - JSON (if API request)
    """
    start_time = time.time()

    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        if 'student_id' in data:
            student_doc = app_module.db.collection('students').document(data['student_id']).get()
            if not student_doc.exists:
                if request.headers.get('HX-Request'):
                    return '<div class="text-red-600 p-4">Student not found</div>', 404
                return jsonify({'error': 'Student not found'}), 404
            student = Student(student_doc.to_dict())
        elif 'student_profile' in data:
            student = Student(data['student_profile'])
        else:
            if request.headers.get('HX-Request'):
                return '<div class="text-red-600 p-4">Missing student_id or student_profile</div>', 400
            return jsonify({'error': 'Missing student_id or student_profile'}), 400

        scholarships_docs = app_module.db.collection('scholarships').stream()
        scholarships = [Scholarship(doc.to_dict()) for doc in scholarships_docs]

        if not scholarships:
            if request.headers.get('HX-Request'):
                return '<div class="text-red-600 p-4">No scholarships available</div>', 404
            return jsonify({'error': 'No scholarships available'}), 404

        eligible, ineligible = RuleFilter.filter_scholarships(scholarships, student)

        ranked = ScholarshipRanker.rank_scholarships(eligible, student)

        matched_results = [Explainer.generate_match_explanation(item, student) for item in ranked]
        rejected_results = [Explainer.generate_rejection_explanation(item, student) for item in ineligible]

        summary = Explainer.generate_summary_stats(matched_results, rejected_results, student)

        processing_time = round((time.time() - start_time) * 1000, 2)

        if request.headers.get('HX-Request'):
            return render_template('results_partial.html',
                                 matched=Explainer.format_for_json(matched_results),
                                 rejected=Explainer.format_for_json(rejected_results),
                                 summary=summary,
                                 processing_time_ms=processing_time,
                                 student_id=student.student_id)
        else:
            return jsonify({
                'success': True,
                'student_id': student.student_id,
                'matched': Explainer.format_for_json(matched_results),
                'rejected': Explainer.format_for_json(rejected_results),
                'summary': summary,
                'processing_time_ms': processing_time
            })

    except Exception as e:
        if request.headers.get('HX-Request'):
            return f'<div class="text-red-600 p-4">Error: {str(e)}</div>', 500
        return jsonify({'error': str(e)}), 500
