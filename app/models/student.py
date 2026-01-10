class Student:
    def __init__(self, data):
        self.student_id = data.get('student_id')
        self.gpa = float(data.get('gpa', 0))
        self.course = int(data.get('course', 0))
        self.gender = int(data.get('gender', 1))
        self.age = int(data.get('age', 20))
        self.nationality = int(data.get('nationality', 1))
        self.is_international = bool(data.get('is_international', False))
        self.current_scholarship_holder = bool(data.get('current_scholarship_holder', False))
        self.keywords = data.get('keywords', [])
        self.status = data.get('status', 'Active')

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'gpa': self.gpa,
            'course': self.course,
            'gender': self.gender,
            'age': self.age,
            'nationality': self.nationality,
            'is_international': self.is_international,
            'current_scholarship_holder': self.current_scholarship_holder,
            'keywords': self.keywords,
            'status': self.status
        }

    def __repr__(self):
        return f"<Student {self.student_id} - GPA: {self.gpa}>"
