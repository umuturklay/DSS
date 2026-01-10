from datetime import datetime

class Scholarship:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.provider = data.get('provider')
        self.amount = float(data.get('amount', 0))
        self.currency = data.get('currency', 'EUR')
        self.duration_months = int(data.get('duration_months', 12))
        self.min_gpa = float(data.get('min_gpa', 0))
        self.eligible_courses = data.get('eligible_courses', [])
        self.eligible_nationalities = data.get('eligible_nationalities', [])
        self.citizenship_required = bool(data.get('citizenship_required', False))
        self.age_max = int(data.get('age_max', 99))
        self.requires_international = data.get('requires_international')
        self.gender_required = data.get('gender_required')
        self.deadline = data.get('deadline')
        self.required_documents = data.get('required_documents', [])
        self.description = data.get('description', '')
        self.competitiveness = float(data.get('competitiveness', 0.5))
        self.keywords = data.get('keywords', [])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'amount': self.amount,
            'currency': self.currency,
            'duration_months': self.duration_months,
            'min_gpa': self.min_gpa,
            'eligible_courses': self.eligible_courses,
            'eligible_nationalities': self.eligible_nationalities,
            'citizenship_required': self.citizenship_required,
            'age_max': self.age_max,
            'requires_international': self.requires_international,
            'gender_required': self.gender_required,
            'deadline': self.deadline,
            'required_documents': self.required_documents,
            'description': self.description,
            'competitiveness': self.competitiveness,
            'keywords': self.keywords
        }

    def days_to_deadline(self):
        if not self.deadline:
            return 365
        try:
            deadline_date = datetime.fromisoformat(self.deadline.replace('Z', '+00:00'))
            delta = deadline_date - datetime.now(deadline_date.tzinfo)
            return max(1, delta.days)
        except:
            return 365

    def __repr__(self):
        return f"<Scholarship {self.name} - Min GPA: {self.min_gpa}>"
