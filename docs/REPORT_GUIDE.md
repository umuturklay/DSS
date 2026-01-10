# Report Writing Guide - What Goes Where

**Purpose**: This guide shows which parts of the technical documentation to use in each report section.

---

## Report Structure & Content Mapping

### 1. Introduction (WRITE YOURSELF - AI PROHIBITED)

**What to include**:
- Project motivation (why scholarship matching is important)
- Problem statement (students struggle to find scholarships manually)
- Research objectives (from proposal)
- Brief overview of DSS approach

**Use from technical docs**:
- Section 1.2 (Core Objectives) - for inspiration only, rewrite in your own words

---

### 2. Literature Review (WRITE YOURSELF - AI PROHIBITED)

**Required papers** (from professor):
1. Noviyanto (2023) - AHP for Scholarship Selection
2. Bachtiar et al. (2021) - Method Comparison
3. Fajardo et al. (2024) - ML for Scholarship Grants
4. Rasooli et al. (2023) - Fairness in Educational Assessment
5. Ziegler et al. (2021) - Equity Gaps in Education

**What to discuss**:
- AHP methodology and applications in education
- Comparison of DSS methods (AHP, TOPSIS, ML)
- Fairness frameworks in educational systems
- Explainability requirements for DSS
- Gap analysis: what's missing in current research

**Use from technical docs**:
- Section 11 (Academic Grounding) - for paper titles and topics only

---

### 3. Methodology

#### 3.1 Data Preprocessing (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 2

**What to copy**:
- Section 2.1: Dataset Source
- Section 2.2: GPA Normalization (with formula)
- Section 2.3: Missing Value Handling
- Section 2.4: Categorical Variable Encoding
- Section 2.5: Feature Engineering
- Section 2.6: Sampling Strategy (with table)
- Section 2.7: Data Quality Metrics (table)

**Add**:
- Justification for each preprocessing step (refer to literature)

#### 3.2 System Architecture (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 3

**What to copy**:
- Section 3.1: Architecture Overview
- Section 3.2: Flask Blueprints description
- Section 3.3: Core Services (brief description)
- Section 3.4: Database Schema

**Add diagrams**:
- Insert `diagram-4.png` (System Architecture Overview)
- Insert `diagram-6.png` (Database Schema)

**LaTeX example**:
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.85\textwidth]{diagrams/diagram-4.png}
    \caption{System Architecture Overview showing Flask blueprints, services, and Firestore integration}
    \label{fig:architecture}
\end{figure}
```

#### 3.3 Matching Algorithm (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 4

**What to copy**:
- Section 4.1: Two-Stage Pipeline (explain why 2 stages)
- Section 4.2: Stage A - Rule-Based Filter (8 rules with implementation example)
- Section 4.3: Stage B - AHP Ranking (5 factors with formulas)

**Add diagrams**:
- Insert `diagram-1.png` (Data Flow Diagram)
- Insert `diagram-3.png` (Decision Logic Architecture)

**Add justification**:
- "This two-stage approach follows Noviyanto (2023) and Bachtiar et al. (2021), ensuring transparent hard constraints before weighted scoring..."

#### 3.4 Explainability Framework (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 5

**What to copy**:
- Section 5.1: Design Philosophy
- Section 5.2: Match Explanation Structure (with JSON example)
- Section 5.3: Rejection Explanation Structure

**Add diagram**:
- Insert `diagram-2.png` (User Interaction Flow)

**Add justification**:
- "Following Fajardo et al. (2024), we implement full explainability using rule traces..."

#### 3.5 Fairness Auditing (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 6

**What to copy**:
- Section 6.1: Fairness Framework
- Section 6.2: Demographic Groups Analyzed
- Section 6.3: Bias Detection Methodology (with formulas)
- Section 6.5: Diversity Metrics

**Add diagram**:
- Insert `diagram-5.png` (Fairness Audit Flow)

**Add justification**:
- "Based on Rasooli et al. (2023) and Ziegler et al. (2021), we implement systematic bias detection across 4 demographic groups..."

---

### 4. Implementation

#### 4.1 Technology Stack (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 8

**What to copy**:
- Section 8.1: Backend technologies (table)
- Section 8.2: Frontend technologies (table)
- Section 8.3: Database (table)
- Section 8.5: Project Structure (file tree)

**Add**:
- Justification for each technology choice
- Why HTMX over React/Vue (professor approved, simpler)
- Why Firestore over PostgreSQL (scalability, real-time)

#### 4.2 Testing Strategy (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 7

**What to copy**:
- Section 7.1: Testing Framework
- Section 7.2: Test Coverage (table)
- Section 7.3: Test Examples (code snippets)

**Add**:
- "As requested by Professor George, we implemented pytest tests for eligibility logic..."

---

### 5. Results

#### 5.1 Match Quality (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 10.2

**What to copy**:
- Precision: 86.0% (with table)
- Validation methodology (Section 7.4)
- Test profiles table (Section 7.5)

**Add**:
- Interpretation: "This exceeds the professor's target of ≥80% precision..."

#### 5.2 Fairness Analysis (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 10.3

**What to copy**:
- Bias Gaps Detected (table)
- Root Causes analysis
- Section 6.6: Bias Analysis Findings

**Add**:
- Critical discussion of why bias exists
- Whether bias is acceptable or problematic
- Mitigation strategies

#### 5.3 Efficiency (COPY FROM DOCS ✅)

**Source**: `TECHNICAL_DOCUMENTATION.md` Section 10.4

**What to copy**:
- Baseline vs DSS performance
- Time reduction calculation

**Add**:
- "User survey results will be collected to validate end-to-end efficiency gains..."

#### 5.4 Screenshots (ADD FROM RUNNING SYSTEM)

**What to include**:
1. Screenshot of student selection page (`http://localhost:5002/match/`)
2. Screenshot of match results with score bars
3. Screenshot of fairness dashboard (`http://localhost:5002/audit/`)
4. Screenshot of detailed explanation

**Caption example**:
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\textwidth]{screenshots/match-results.png}
    \caption{Match Results Page showing ranked scholarships with score breakdowns and Chart.js visualization}
    \label{fig:results}
\end{figure}
```

---

### 6. Discussion (WRITE YOURSELF - AI PROHIBITED)

**What to discuss**:
- Interpretation of 86% precision result
- Analysis of fairness bias findings
  - Is gender bias problematic or expected?
  - Is GPA bias acceptable for merit-based scholarships?
  - How to address nationality bias (add more international scholarships)?
- Comparison to literature
  - How does our AHP implementation compare to Noviyanto (2023)?
  - Advantages of rule-based over ML (Bachtiar et al. 2021)
- Limitations
  - Small dataset (500 students, 10 scholarships)
  - No user feedback loop yet
  - Weights are manually assigned (not learned)
- Future work
  - ML-based ranker
  - Larger scholarship database
  - Mobile app

**Use from technical docs**:
- Section 10 (Results) - for factual data only
- Section 12 (Future Enhancements) - for ideas

---

### 7. Conclusion (WRITE YOURSELF - AI PROHIBITED)

**What to include**:
- Summary of contributions
  - Implemented rule-based DSS with 8 eligibility criteria
  - Achieved 86% precision (exceeds target)
  - Full transparency with explanations
  - Fairness auditing with bias detection
- Key findings
  - System successfully matches students to scholarships
  - Some demographic bias detected (needs attention)
  - High precision demonstrates effectiveness
- Practical implications
  - Can reduce scholarship search time significantly
  - Provides transparent recommendations
  - Scalable to larger databases
- Final thoughts

---

## Quick Checklist

### ✅ What to COPY directly from docs:
- [ ] Data preprocessing methodology (Section 2)
- [ ] GPA normalization formula
- [ ] Sampling strategy table
- [ ] System architecture description (Section 3)
- [ ] Database schema
- [ ] Matching algorithm (8 rules + 5 AHP factors) with formulas
- [ ] Explainability framework structure
- [ ] Fairness methodology
- [ ] Technology stack tables
- [ ] Testing summary
- [ ] Precision validation results (86%)
- [ ] Bias analysis tables
- [ ] All 6 PNG diagrams

### ❌ What to WRITE yourself (AI prohibited):
- [ ] Introduction
- [ ] Literature Review (5 papers)
- [ ] Justifications for design choices (cite literature)
- [ ] Discussion of results
- [ ] Interpretation of bias findings
- [ ] Limitations
- [ ] Conclusion

### 📊 What to ADD (not in docs yet):
- [ ] Screenshots of running system (4-5 screenshots)
- [ ] User survey results (if collected)
- [ ] References section (cite 5 papers + datasets)

---

## Diagram Usage

### All 6 Diagrams - Insert Points:

1. **diagram-1.png** (Data Flow)
   - **Insert in**: Methodology → Matching Algorithm → Data Flow
   - **Caption**: "Complete data flow from student input to final recommendations showing Firestore interactions, filtering, ranking, and explanation generation"

2. **diagram-2.png** (User Interaction)
   - **Insert in**: Methodology → Explainability Framework OR Implementation → User Interface
   - **Caption**: "HTMX-based user interaction sequence showing browser-server communication for dynamic match results"

3. **diagram-3.png** (Decision Logic)
   - **Insert in**: Methodology → Matching Algorithm → Pipeline Architecture
   - **Caption**: "Three-stage decision pipeline: Rule-based filter (8 constraints), AHP ranker (5 weighted factors), and explainability module"

4. **diagram-4.png** (System Architecture)
   - **Insert in**: Methodology → System Architecture OR Implementation → Tech Stack
   - **Caption**: "System architecture overview showing Flask blueprints, business logic services, Firestore database, and frontend components"

5. **diagram-5.png** (Fairness Audit)
   - **Insert in**: Methodology → Fairness Auditing OR Results → Fairness Analysis
   - **Caption**: "Fairness audit process flow with demographic segmentation, match rate calculation, and bias threshold detection"

6. **diagram-6.png** (Database Schema)
   - **Insert in**: Methodology → System Architecture → Data Model
   - **Caption**: "Firestore database schema showing students, scholarships, and match_results collections with their relationships"

---

## File Locations

### Documentation Files:
- **Main Tech Doc**: `/Users/umutturklay/dev/UE/DSS/docs/TECHNICAL_DOCUMENTATION.md`
- **Preprocessing Details**: `/Users/umutturklay/dev/UE/DSS/docs/DATA_PREPROCESSING.md`
- **Diagrams Source**: `/Users/umutturklay/dev/UE/DSS/docs/SYSTEM_DIAGRAMS.md`
- **Testing Details**: `/Users/umutturklay/dev/UE/DSS/tests/README.md`

### Diagrams (PNG):
- All 6 diagrams: `/Users/umutturklay/dev/UE/DSS/docs/diagrams/diagram-*.png`

### Validation Results:
- CSV: `/Users/umutturklay/dev/UE/DSS/data/validation/precision_validation_20260110_170016.csv`
- JSON: `/Users/umutturklay/dev/UE/DSS/data/validation/precision_validation_20260110_170016.json`
- Summary: `/Users/umutturklay/dev/UE/DSS/data/validation/precision_summary_20260110_170016.txt`

---

## Tips for Report Writing

### 1. Introduction & Literature Review
- **DO**: Write in your own words, cite papers properly
- **DON'T**: Copy AI-generated text (will be detected)

### 2. Methodology
- **DO**: Copy technical details (formulas, algorithms, tables)
- **DO**: Add justifications referencing literature
- **Example**: "We chose AHP-based ranking following Noviyanto (2023), as it provides transparent weight assignment and has been proven effective in educational decision support systems."

### 3. Results
- **DO**: Present data objectively (tables, charts, precision numbers)
- **DO**: Add brief interpretations
- **Example**: "The system achieved 86% precision, exceeding the target of ≥80%, indicating high match quality."

### 4. Discussion
- **DO**: Critically analyze results
- **DO**: Compare to literature findings
- **DO**: Discuss limitations honestly
- **Example**: "While our gender bias finding (78.9% gap) is concerning, it reflects underlying GPA differences in the dataset rather than algorithmic bias..."

### 5. Formatting
- **DO**: Use professional academic formatting (IEEE, APA, or as specified)
- **DO**: Number all figures and tables
- **DO**: Reference diagrams in text ("As shown in Figure 3...")

---

**Good luck with your report!** 🎓

Remember: Technical content can be copied, but Introduction, Literature Review, Discussion, and Conclusion MUST be in your own words.
