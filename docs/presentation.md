# Scholarship Matching Decision Support System
## A Student-Centric Approach to Scholarship Discovery

**Umut Turklay**
**UE Course Project**
**January 2026**

---

## Problem Statement

### The Challenge
- **Manual scholarship search is time-consuming**: 15-20 minutes per search
- **Students miss opportunities**: Only find 2-3 scholarships manually
- **Lack of transparency**: No clear understanding of eligibility
- **Potential bias**: Inconsistent criteria application

### The Impact
- Students overwhelmed by options
- Qualified candidates miss deadlines
- Wasted time on ineligible applications
- No systematic approach to matching

---

## Research Objectives

### Primary Goal
Build a **transparent, fair, and efficient** Decision Support System for scholarship matching

### Specific Objectives
1. **Accurate Matches**: Achieve ≥80% precision in recommendations
2. **Clear Reasoning**: Provide "Why Matched / Why Not" explanations
3. **Fairness by Design**: Detect and monitor demographic bias
4. **Efficiency**: Reduce search time by ≥50%
5. **Always Fresh**: Auto-updating scholarship listings

---

## Literature Review

### Academic Foundation

| Paper | Key Contribution |
|-------|------------------|
| **Noviyanto (2023)** | AHP for scholarship selection - transparent weight assignment |
| **Bachtiar et al. (2021)** | Comparison: AHP vs TOPSIS vs Deep Learning |
| **Fajardo et al. (2024)** | ML interpretability for scholarship grants |
| **Rasooli et al. (2023)** | Fairness in educational assessment |
| **Ziegler et al. (2021)** | Equity gaps measurement framework |

### Design Choice
✅ **Start Simple**: Rule-based DSS (professor's guidance)
⏳ **Future**: ML-based ranker (decision trees, logistic regression)

---

## System Architecture

### Three-Tier Architecture

```
┌─────────────────────────────────────────┐
│   Presentation Layer                    │
│   HTMX + Jinja2 + TailwindCSS          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   Application Layer                     │
│   Flask Blueprints + Business Services  │
│   - Match Blueprint                     │
│   - Explain Blueprint                   │
│   - Audit Blueprint                     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   Data Layer                            │
│   Firebase Firestore (NoSQL)            │
│   - 500 Students                        │
│   - 10 Scholarships                     │
└─────────────────────────────────────────┘
```

**Why This Stack?**
- **HTMX**: Dynamic updates without SPA complexity
- **Flask**: Lightweight, modular (blueprints)
- **Firestore**: Real-time, scalable NoSQL

---

## Data Preprocessing

### Dataset
- **Source**: Kaggle Student Success Dataset (5,416 students)
- **Processed**: 500 students (stratified sample)
- **Scholarships**: 10 diverse opportunities (manually created)

### Key Preprocessing Steps

| Step | Method | Result |
|------|--------|--------|
| **GPA Normalization** | Linear transformation (95-190 → 0-4.0) | Mean: 2.46, Range: 0.17-3.92 |
| **Missing Values** | Analysis + validation | 0 missing values (100% complete) |
| **Categorical Encoding** | Gender: 0/1, Nationality: codes | Consistent format |
| **Feature Engineering** | Keyword extraction from courses | Jaccard similarity matching |
| **Stratified Sampling** | Preserve demographics | 92.2% Female, 7.8% Male |

**Quality**: 100% complete, valid, unique

---

## Matching Algorithm: Two-Stage Pipeline

### Stage A: Rule-Based Filter
**Purpose**: Hard constraints (binary: pass/fail)

**8 Eligibility Rules**:
1. ✓ GPA: `student.gpa >= scholarship.min_gpa`
2. ✓ Course: `student.course IN eligible_courses`
3. ✓ Nationality: `student.nationality IN eligible_nationalities`
4. ✓ Deadline: `scholarship.deadline > today`
5. ✓ Age: `student.age <= scholarship.age_max`
6. ✓ International Status: `Required international == student.is_international`
7. ✓ Gender: `Gender-specific scholarships (e.g., Women in STEM)`
8. ✓ Citizenship: `Local-only scholarships require domestic status`

**Output**: Eligible vs Ineligible scholarships

---

## Matching Algorithm: AHP Ranking

### Stage B: Weighted Scoring
**Purpose**: Rank eligible scholarships by fit

**5 AHP Factors**:

| Factor | Weight | Formula |
|--------|--------|---------|
| **GPA Buffer** | 25% | `(student.gpa - min_gpa) / 4.0` |
| **Keyword Match** | 25% | Jaccard similarity of keywords |
| **Competitiveness** | 20% | `1 - competitiveness` (easier to win) |
| **Time to Deadline** | 15% | Urgency (sooner = higher) |
| **Document Burden** | 15% | `1 - (docs / max_docs)` (fewer = easier) |

**Final Score**: Weighted sum → Range: 0.0 - 1.0

**Inspiration**: Noviyanto (2023) - AHP methodology

---

## Explainability Framework

### "Why Matched / Why Not" Transparency

**For Matched Scholarships**:
```
DAAD Master's Scholarship - Score: 0.87 (Rank #1)

✓ GPA 3.6 meets minimum 3.0 (+0.6 buffer)
✓ Computer Science major eligible
✓ International student (required)
✓ Age 22 within limit (max 35)
✓ Deadline April 10, 2026 (78 days remaining)

Score Breakdown:
- GPA Buffer: 0.15
- Keyword Match: 0.20
- Competitiveness: 0.16
- Deadline: 0.12
- Doc Burden: 0.13

Recommendation: Strong match - Apply by April 10
```

**For Rejected Scholarships**:
```
✗ Citizenship required: You are international student
✗ GPA 2.8 below minimum 3.2

Recommendation: Consider improving GPA or citizenship
```

---

## Fairness Auditing

### Demographic Bias Detection

**4 Groups Analyzed**:
1. Gender (Male vs Female)
2. Nationality (Domestic vs International)
3. GPA Band (Low <2.5 vs Mid 2.5-3.2 vs High >3.2)
4. Scholarship Holder Status (Has vs No scholarship)

**Bias Threshold**: 15% gap triggers alert

**Methodology** (Rasooli et al. 2023):
```
Match Rate = Total Matches / Number of Students
Gap = Max(Match Rates) - Min(Match Rates)

If Gap > 0.15 → BIAS ALERT 🚨
```

---

## Fairness Results

### Bias Gaps Detected

| Demographic | Gap | Severity | Interpretation |
|-------------|-----|----------|----------------|
| **Gender** | 78.9% | 🔴 High | Females: 2.02 avg, Males: 1.23 avg |
| **Nationality** | 157.4% | 🔴 High | Domestic: 1.97 avg, International: 0.40 avg |
| **GPA** | 319.2% | 🟡 Medium | High GPA: 3.54 avg, Low GPA: 0.84 avg |

### Root Causes
- **Gender**: Females have higher avg GPA (2.46 vs 2.17)
- **Nationality**: Only 5 international students (1%), most scholarships require citizenship
- **GPA**: Expected for merit-based scholarships (acceptable bias)

### Mitigation
✅ Add more international scholarships
✅ Add need-based (low GPA) scholarships
✅ Monitor gender-specific scholarships

---

## Testing & Validation

### Testing Strategy (pytest)
**Total Tests**: 53 unit tests
- 25 tests: Rule-based filtering
- 18 tests: AHP scoring algorithm
- 10 tests: Explanation generation

**Status**: ✅ Core business logic validated

---

## Validation Results

### Match Quality (Professor's Requirement: ≥80%)

**Method**: 10 diverse test profiles with manually verified ground truth

| Test Profile | Predicted | Expected | Correct | Precision |
|--------------|-----------|----------|---------|-----------|
| High GPA CS (3.8) | 8 | 8 | 8 | 100% |
| Low GPA Business (2.2) | 2 | 2 | 2 | 100% |
| International STEM (3.5) | 5 | 5 | 5 | 100% |
| Female Engineering (3.2) | 6 | 6 | 6 | 100% |
| Mid-GPA IT (2.9) | 5 | 5 | 5 | 100% |
| ... | ... | ... | ... | ... |

### 🎯 Result: 86% Average Precision
✅ **EXCEEDS 80% TARGET**

**Formula**: `Precision = Correct Recommendations / Total Recommendations`

---

## Results Summary

### Achieved Metrics

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| **Match Quality** | ≥80% precision | 86% | ✅ Exceeded |
| **Transparency** | 100% explanations | 100% | ✅ Met |
| **Efficiency** | ≥50% time saved | ~99.7% (algorithmic) | ✅ Exceeded |
| **Equity** | <15% bias gap | Varies by group | ⚠️ Needs work |

### Database Statistics
- **Students**: 500 (stratified sample)
- **Scholarships**: 10 diverse opportunities
- **Average Matches**: 1.96 per student (19.6% match rate)

---

## System Demo: Student Selection

![Student Selection Page](screenshots/student-selection.png)

**Features**:
- All 500 students accessible
- Search/filter by student ID, GPA, course
- Sorted by GPA (descending)
- Real-time HTMX form submission

---

## System Demo: Match Results

![Match Results](screenshots/match-results.png)

**Features**:
- Ranked scholarships with score bars
- "Why Matched" criteria checklist
- Chart.js visualization
- Collapsible rejected scholarships

---

## System Demo: Fairness Dashboard

![Fairness Dashboard](screenshots/fairness-dashboard.png)

**Features**:
- 4 Chart.js visualizations (gender, nationality, GPA, scholarship holder)
- Bias alert cards with severity
- Demographic analysis tables
- Diversity metrics

---

## Key Contributions

### 1. Academic Rigor
✅ Literature-grounded design (5 papers)
✅ AHP-based ranking (Noviyanto 2023)
✅ Fairness framework (Rasooli 2023, Ziegler 2021)

### 2. Technical Implementation
✅ Two-stage pipeline (Filter → Rank)
✅ 8 eligibility rules + 5 AHP factors
✅ Full explainability (rule traces)
✅ Demographic bias detection

### 3. Validation
✅ 86% precision (exceeds 80% target)
✅ 53 pytest tests
✅ Complete documentation

---

## Limitations

### Current Limitations
1. **Small Dataset**: 500 students, 10 scholarships (demo scale)
2. **Manual Weights**: AHP weights assigned by domain expert (not learned)
3. **No User Feedback**: Cannot adjust weights based on application success
4. **Static Scholarships**: No auto-updating from external sources
5. **Bias Issues**: Gender/nationality bias needs mitigation (add more scholarships)

### Technical Limitations
- No mobile app (web-only)
- No email notifications
- No document upload (Firebase Storage)
- No admin panel for scholarship CRUD

---

## Future Work

### Short-Term (Post-MVP)
1. **ML-Based Ranker**: Decision tree or logistic regression to learn weights
2. **User Feedback Loop**: "Was this helpful?" ratings to improve ranking
3. **Larger Database**: Expand to 50+ scholarships
4. **Bias Mitigation**: Add international and need-based scholarships

### Long-Term
1. **Mobile App**: Flutter/React Native with push notifications
2. **Email Alerts**: Notify students when new scholarships match profile
3. **Document Upload**: Store transcripts, CVs in Firebase Storage
4. **Admin Panel**: Scholarship CRUD, user management, analytics
5. **Integration**: Scrape scholarship websites for auto-updates

---

## Lessons Learned

### What Worked Well
✅ **Start Simple**: Rule-based approach was transparent and debuggable
✅ **HTMX**: Dynamic updates without SPA complexity
✅ **Firestore**: NoSQL flexibility for rapid prototyping
✅ **Two-Stage Pipeline**: Clear separation (eligibility → ranking)

### What Was Challenging
⚠️ **Bias Detection**: Difficult to distinguish acceptable vs problematic bias
⚠️ **Weight Assignment**: No clear methodology for AHP weights
⚠️ **Small Dataset**: Limited diversity in test data
⚠️ **Manual Scholarships**: Creating realistic scholarship data time-consuming

### Key Takeaway
**Transparency is hard but essential** - Every design choice affects fairness

---

## Conclusion

### Summary
- ✅ Built functional DSS with 86% precision (exceeds 80% target)
- ✅ Implemented full transparency ("Why Matched / Why Not")
- ✅ Detected demographic bias (gender, nationality, GPA)
- ✅ Validated with 53 pytest tests
- ✅ Complete technical documentation + 6 diagrams

### Impact
- Students can find scholarships in **3 seconds** (vs 15-20 minutes manually)
- Transparent recommendations build trust
- Fairness auditing ensures equity monitoring
- Scalable foundation for ML-based enhancements

### Final Thought
> "A good DSS doesn't just recommend - it explains, learns, and ensures fairness"

---

## Questions?

**Contact**: Umut Turklay
**Project Repository**: `/Users/umutturklay/dev/UE/DSS`
**Documentation**: `/docs/TECHNICAL_DOCUMENTATION.md`
**Demo**: `http://localhost:5002`

---

## Appendix: System Diagrams

### Data Flow Diagram
![Data Flow](diagrams/diagram-1.png)

Complete flow from student input → Firestore → RuleFilter → Ranker → Explainer → Results

---

## Appendix: Decision Logic Architecture

![Decision Logic](diagrams/diagram-3.png)

Three-stage pipeline:
- **Stage A**: Rule-based filter (8 hard constraints)
- **Stage B**: AHP ranker (5 weighted factors)
- **Stage C**: Explainability module

---

## Appendix: Fairness Audit Flow

![Fairness Audit](diagrams/diagram-5.png)

Bias detection process:
- Segment students by demographics
- Calculate match rates per group
- Compare gaps against 15% threshold
- Generate bias alerts if exceeded

---

## Thank You!

**Questions?**

**Demo Available**: `http://localhost:5002`
