# Scholarship Matching DSS

**Academic Decision Support System** for matching students with scholarships.

🎓 **Course**: Decision Support Systems (UE)
✅ **Status**: MVP Complete - Core Engine Functional
📊 **Based on**: AHP methodology, Fairness frameworks, Academic literature

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Firebase

```bash
# Copy environment template
cp .env.example .env

# Add your Firebase credentials to .env:
# - FIREBASE_CREDENTIALS_PATH
# - FIREBASE_API_KEY
# - FIREBASE_PROJECT_ID
# etc.
```

### 3. Run Tests

```bash
# Unit tests
python tests/test_matching_engine.py

# Firestore integration test
python tests/test_with_firestore.py

# Fairness audit
python tests/test_fairness.py
```

### 4. Run Flask App

```bash
python run.py
# App runs on http://localhost:5000
```

---

## 📡 API Endpoints

### Match Student

```bash
POST /match/api
Body: {"student_id": "STU_00162"}
```

### Get Explanation

```bash
GET /explain/<scholarship_id>/<student_id>
```

### Run Fairness Audit

```bash
GET /audit
```

---

## 🏗️ System Architecture

### Two-Stage Matching Engine

**Stage 1: Rule-Based Filter** (Hard Constraints)

- GPA threshold
- Course eligibility
- Nationality requirements
- Deadline validation
- Age/gender/citizenship checks

**Stage 2: AHP-Inspired Ranking** (Weighted Scoring)

- GPA Buffer: 25%
- Keyword Match: 25%
- Competitiveness: 20%
- Time to Deadline: 15%
- Document Burden: 15%

### Explainability

- ✅ "Why Matched" with criteria checklist
- ✅ "Why Not Matched" with failed rules
- ✅ Scoring breakdown
- ✅ Actionable recommendations

### Fairness Auditing

- ✅ Demographic gap detection
- ✅ Bias alerts (15% threshold)
- ✅ Diversity metrics

---

## 📁 Project Structure

```
DSS/
├── app/
│   ├── models/
│   │   ├── student.py              # Student data model
│   │   ├── scholarship.py          # Scholarship model
│   │   └── match_result.py         # Match result structure
│   ├── services/
│   │   ├── rule_filter.py          # Rule-based filtering
│   │   ├── ranker.py               # AHP-weighted ranking
│   │   ├── explainer.py            # Explanation generator
│   │   └── fairness_auditor.py     # Bias detection
│   ├── blueprints/
│   │   ├── match.py                # /match endpoint
│   │   ├── explain.py              # /explain endpoint
│   │   └── audit.py                # /audit endpoint
│   └── templates/                  # Jinja2 templates
├── data/
│   ├── raw/                        # Raw datasets
│   └── processed/                  # Processed data
├── tests/                          # Test files
└── scripts/                        # Utility scripts
```

---

## 🎯 Success Metrics

| Metric        | Target           | Status        |
| ------------- | ---------------- | ------------- |
| Match Quality | ≥80% precision  | ✅ Validated  |
| Transparency  | 100%             | ✅ Achieved   |
| Efficiency    | ≥66% time saved | ✅ >95% saved |
| Equity        | <15% gap         | ✅ Monitored  |

---

## 📚 Academic Grounding

Based on peer-reviewed research:

1. **Noviyanto (2023)** - AHP in Scholarship Selection
2. **Bachtiar et al. (2021)** - Method Comparison in DSS
3. **Rasooli et al. (2023)** - Fairness in Educational Assessment
4. **Fajardo et al. (2024)** - ML in Scholarship Prediction

---

## 🧪 Testing

All core components tested:

✅ Rule-based filtering
✅ AHP-weighted ranking
✅ Explainability module
✅ Fairness auditing
✅ Firestore integration

**Test Coverage**: Core engine functions

---

## 📖 Documentation

See **PROJECT_SUMMARY.md** for:

- Detailed implementation status
- Test results
- Academic compliance checklist
- Future enhancements
- Literature references

---

## 🤝 Contributors

UE Decision Support Systems Course Team

**Professor**: George Kolostoumpis
**Institution**: University of Europe for Applied Sciences

---

## 📝 License

Academic project - UE Decision Support Systems Course 2024-2025
