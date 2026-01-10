import json
from datetime import datetime, timedelta

scholarships = [
    {
        "name": "DAAD Master's Scholarship",
        "provider": "DAAD (Germany)",
        "amount": 934,
        "currency": "EUR",
        "duration_months": 24,
        "min_gpa": 3.0,
        "eligible_courses": [9991, 9500, 9119, 9070],
        "eligible_nationalities": [6, 22, 24, 26, 41],
        "citizenship_required": False,
        "age_max": 35,
        "requires_international": True,
        "deadline": (datetime.now() + timedelta(days=90)).isoformat(),
        "required_documents": ["transcript", "motivation_letter", "recommendation_letter"],
        "description": "Full scholarship for international master's students in Germany",
        "competitiveness": 0.8,
        "keywords": ["engineering", "computer science", "technology"]
    },
    {
        "name": "Erasmus+ Mobility Grant",
        "provider": "European Union",
        "amount": 500,
        "currency": "EUR",
        "duration_months": 6,
        "min_gpa": 2.5,
        "eligible_courses": [],
        "eligible_nationalities": [1, 6, 22, 24, 26, 41],
        "citizenship_required": False,
        "age_max": 30,
        "requires_international": False,
        "deadline": (datetime.now() + timedelta(days=120)).isoformat(),
        "required_documents": ["transcript", "learning_agreement"],
        "description": "Mobility support for European students studying abroad",
        "competitiveness": 0.5,
        "keywords": ["exchange", "mobility", "europe"]
    },
    {
        "name": "UE Excellence Scholarship",
        "provider": "University of Europe",
        "amount": 5000,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 3.5,
        "eligible_courses": [9991, 9500, 9119],
        "eligible_nationalities": [],
        "citizenship_required": False,
        "age_max": 28,
        "requires_international": False,
        "deadline": (datetime.now() + timedelta(days=60)).isoformat(),
        "required_documents": ["transcript", "portfolio"],
        "description": "Merit-based scholarship for high-achieving students at UE",
        "competitiveness": 0.9,
        "keywords": ["excellence", "merit", "high achiever"]
    },
    {
        "name": "TURKIYE Scholarship",
        "provider": "Republic of Turkey",
        "amount": 700,
        "currency": "EUR",
        "duration_months": 24,
        "min_gpa": 2.8,
        "eligible_courses": [],
        "eligible_nationalities": [6, 22, 24, 26, 41, 62, 100, 101],
        "citizenship_required": False,
        "age_max": 30,
        "requires_international": True,
        "deadline": (datetime.now() + timedelta(days=150)).isoformat(),
        "required_documents": ["transcript", "health_report", "recommendation_letter"],
        "description": "Full scholarship for international students to study in Turkey",
        "competitiveness": 0.6,
        "keywords": ["turkey", "international", "full scholarship"]
    },
    {
        "name": "Need-Based Financial Aid",
        "provider": "UE Financial Office",
        "amount": 3000,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 2.3,
        "eligible_courses": [],
        "eligible_nationalities": [],
        "citizenship_required": False,
        "age_max": 35,
        "requires_international": False,
        "deadline": (datetime.now() + timedelta(days=45)).isoformat(),
        "required_documents": ["transcript", "income_certificate", "family_declaration"],
        "description": "Financial support for students with demonstrated financial need",
        "competitiveness": 0.4,
        "keywords": ["need-based", "financial aid", "low income"]
    },
    {
        "name": "Women in STEM Scholarship",
        "provider": "STEM Foundation",
        "amount": 4000,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 3.0,
        "eligible_courses": [9991, 9500, 9119, 9070, 9238],
        "eligible_nationalities": [],
        "citizenship_required": False,
        "age_max": 30,
        "requires_international": False,
        "gender_required": 0,
        "deadline": (datetime.now() + timedelta(days=75)).isoformat(),
        "required_documents": ["transcript", "essay"],
        "description": "Supporting women pursuing degrees in STEM fields",
        "competitiveness": 0.7,
        "keywords": ["women", "stem", "diversity"]
    },
    {
        "name": "Local Merit Scholarship",
        "provider": "State Education Fund",
        "amount": 2500,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 3.2,
        "eligible_courses": [],
        "eligible_nationalities": [1],
        "citizenship_required": True,
        "age_max": 25,
        "requires_international": False,
        "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
        "required_documents": ["transcript", "citizenship_proof"],
        "description": "Merit-based scholarship for domestic students",
        "competitiveness": 0.6,
        "keywords": ["local", "merit", "domestic"]
    },
    {
        "name": "Business & Economics Grant",
        "provider": "Business School Association",
        "amount": 3500,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 2.8,
        "eligible_courses": [9773, 9853, 9254],
        "eligible_nationalities": [],
        "citizenship_required": False,
        "age_max": 32,
        "requires_international": False,
        "deadline": (datetime.now() + timedelta(days=100)).isoformat(),
        "required_documents": ["transcript", "business_plan"],
        "description": "Support for students in business and economics programs",
        "competitiveness": 0.5,
        "keywords": ["business", "economics", "management"]
    },
    {
        "name": "Sports Excellence Scholarship",
        "provider": "University Athletics",
        "amount": 2000,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 2.0,
        "eligible_courses": [],
        "eligible_nationalities": [],
        "citizenship_required": False,
        "age_max": 26,
        "requires_international": False,
        "deadline": (datetime.now() + timedelta(days=50)).isoformat(),
        "required_documents": ["transcript", "sports_achievements", "coach_recommendation"],
        "description": "Scholarship for student athletes with proven achievements",
        "competitiveness": 0.7,
        "keywords": ["sports", "athletics", "achievement"]
    },
    {
        "name": "Refugee Support Scholarship",
        "provider": "Humanitarian Education Fund",
        "amount": 6000,
        "currency": "EUR",
        "duration_months": 12,
        "min_gpa": 2.0,
        "eligible_courses": [],
        "eligible_nationalities": [62, 100, 101, 11],
        "citizenship_required": False,
        "age_max": 35,
        "requires_international": True,
        "deadline": (datetime.now() + timedelta(days=180)).isoformat(),
        "required_documents": ["transcript", "refugee_status", "recommendation_letter"],
        "description": "Full support for displaced students seeking higher education",
        "competitiveness": 0.3,
        "keywords": ["refugee", "humanitarian", "support"]
    }
]

print(f"✅ {len(scholarships)} adet scholarship oluşturuldu\n")

for i, sch in enumerate(scholarships, 1):
    print(f"{i}. {sch['name']}")
    print(f"   Provider: {sch['provider']}")
    print(f"   Amount: €{sch['amount']}/month")
    print(f"   Min GPA: {sch['min_gpa']}")
    print(f"   Deadline: {sch['deadline'][:10]}")
    print()

with open('data/processed/scholarships.json', 'w') as f:
    json.dump(scholarships, f, indent=2)

print("💾 Scholarships saved to: data/processed/scholarships.json")
