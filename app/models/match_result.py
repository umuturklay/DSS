class MatchResult:
    def __init__(self, scholarship, student, matched=False, score=0.0):
        self.scholarship = scholarship
        self.student = student
        self.matched = matched
        self.score = score
        self.ranking = 0
        self.met_criteria = []
        self.failed_criteria = []
        self.scoring_breakdown = {}
        self.recommendation = ""

    def to_dict(self):
        return {
            'scholarship_id': self.scholarship.id,
            'scholarship_name': self.scholarship.name,
            'provider': self.scholarship.provider,
            'amount': self.scholarship.amount,
            'currency': self.scholarship.currency,
            'deadline': self.scholarship.deadline,
            'matched': self.matched,
            'score': round(self.score, 3),
            'ranking': self.ranking,
            'reasons': {
                'met_criteria': self.met_criteria,
                'failed_criteria': self.failed_criteria,
                'scoring_breakdown': self.scoring_breakdown
            },
            'recommendation': self.recommendation
        }

    def __repr__(self):
        status = "MATCHED" if self.matched else "NOT MATCHED"
        return f"<MatchResult {self.scholarship.name} - {status} - Score: {self.score:.2f}>"
