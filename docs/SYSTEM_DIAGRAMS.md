# System Architecture Diagrams

This document contains all system diagrams for the Scholarship Matching DSS project.
You can copy these diagrams to your report or convert them to PNG/PDF.

## How to Convert to PNG

### Method 1: Online (Easiest)
1. Go to https://mermaid.live/
2. Copy the Mermaid code below
3. Paste into the editor
4. Click "Download PNG" or "Download SVG"

### Method 2: VS Code
1. Install "Markdown Preview Mermaid Support" extension
2. Open this file in VS Code
3. Press Cmd+Shift+V to preview
4. Right-click diagram → "Copy as Image"

### Method 3: CLI
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/SYSTEM_DIAGRAMS.md -o docs/diagrams/
```

---

## 1. Data Flow Diagram

**Description:** Shows how data flows through the system from student input to final recommendations.

```mermaid
flowchart TB
    Start([Student Accesses System]) --> Input[Student Profile Input<br/>GPA, Course, Age, Nationality, etc.]

    Input --> Firestore1[(Firestore<br/>Students Collection)]
    Firestore1 --> ProfileStored{Profile<br/>Stored?}

    ProfileStored -->|Yes| MatchRequest[Match Request Triggered]
    ProfileStored -->|No| SaveProfile[Save Profile to Firestore]
    SaveProfile --> MatchRequest

    MatchRequest --> FetchScholarships[(Firestore<br/>Scholarships Collection)]
    FetchScholarships --> Scholarships[10 Active Scholarships]

    Scholarships --> RuleFilter[Rule-Based Filter<br/>Stage A]

    RuleFilter --> Check1{GPA ≥ Min?}
    RuleFilter --> Check2{Course Eligible?}
    RuleFilter --> Check3{Nationality OK?}
    RuleFilter --> Check4{Deadline Valid?}
    RuleFilter --> Check5{Age ≤ Max?}
    RuleFilter --> Check6{International Status?}
    RuleFilter --> Check7{Gender Match?}
    RuleFilter --> Check8{Citizenship OK?}

    Check1 --> Eligible{All Rules<br/>Passed?}
    Check2 --> Eligible
    Check3 --> Eligible
    Check4 --> Eligible
    Check5 --> Eligible
    Check6 --> Eligible
    Check7 --> Eligible
    Check8 --> Eligible

    Eligible -->|Yes| EligibleList[Eligible Scholarships List]
    Eligible -->|No| RejectedList[Rejected Scholarships List]

    EligibleList --> Ranker[AHP Weighted Ranker<br/>Stage B]

    Ranker --> Score1[GPA Buffer Score<br/>Weight: 0.25]
    Ranker --> Score2[Keyword Match Score<br/>Weight: 0.25]
    Ranker --> Score3[Competitiveness Score<br/>Weight: 0.20]
    Ranker --> Score4[Deadline Urgency Score<br/>Weight: 0.15]
    Ranker --> Score5[Document Burden Score<br/>Weight: 0.15]

    Score1 --> FinalScore[Weighted Final Score<br/>0.0 - 1.0]
    Score2 --> FinalScore
    Score3 --> FinalScore
    Score4 --> FinalScore
    Score5 --> FinalScore

    FinalScore --> Ranked[Ranked Scholarships<br/>Highest Score First]

    Ranked --> Explainer[Explainability Module]
    RejectedList --> Explainer

    Explainer --> MatchExplain[Match Explanations<br/>Why Matched + Score Breakdown]
    Explainer --> RejectExplain[Rejection Explanations<br/>Why Not Matched + Recommendation]

    MatchExplain --> Results[Results Page<br/>HTMX Dynamic Update]
    RejectExplain --> Results

    Results --> Charts[Chart.js Visualizations<br/>Match Score Distribution]
    Charts --> Display[Display to Student]

    Display --> End([Student Reviews & Applies])

    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style RuleFilter fill:#fff4e6
    style Ranker fill:#e6f3ff
    style Explainer fill:#f0e6ff
    style Firestore1 fill:#ffe6e6
    style FetchScholarships fill:#ffe6e6
    style Results fill:#e1f5e1
```

---

## 2. User Interaction Flow

**Description:** Step-by-step user journey through the system.

```mermaid
sequenceDiagram
    actor Student
    participant Browser
    participant Flask
    participant RuleFilter
    participant Ranker
    participant Explainer
    participant Firestore
    participant HTMX

    Student->>Browser: Visit /match
    Browser->>Flask: GET /match/
    Flask->>Firestore: Fetch all students
    Firestore-->>Flask: Return 500 students
    Flask-->>Browser: Render match.html with student dropdown

    Student->>Browser: Search & select student profile
    Note over Student,Browser: Filter 500 students using JavaScript

    Student->>Browser: Click "Find My Scholarships"
    Browser->>HTMX: hx-post="/match/api"
    HTMX->>Flask: POST /match/api {student_id}

    Flask->>Firestore: Get student by ID
    Firestore-->>Flask: Student profile data

    Flask->>Firestore: Get all scholarships
    Firestore-->>Flask: 10 scholarships

    Flask->>RuleFilter: filter_scholarships(scholarships, student)

    loop For each scholarship
        RuleFilter->>RuleFilter: Check GPA, Course, Nationality...
        RuleFilter->>RuleFilter: Apply 8 rules
    end

    RuleFilter-->>Flask: (eligible_list, ineligible_list)

    Flask->>Ranker: rank_scholarships(eligible, student)

    loop For each eligible scholarship
        Ranker->>Ranker: Calculate GPA buffer score
        Ranker->>Ranker: Calculate keyword match score
        Ranker->>Ranker: Calculate competitiveness score
        Ranker->>Ranker: Calculate deadline urgency
        Ranker->>Ranker: Calculate doc burden score
        Ranker->>Ranker: Weighted sum (AHP)
    end

    Ranker-->>Flask: Ranked scholarships (sorted by score)

    Flask->>Explainer: generate_explanations(matched, rejected, student)

    loop For each matched scholarship
        Explainer->>Explainer: Extract met criteria
        Explainer->>Explainer: Create score breakdown
        Explainer->>Explainer: Generate recommendation
    end

    loop For each rejected scholarship
        Explainer->>Explainer: Extract failed criteria
        Explainer->>Explainer: Generate improvement tips
    end

    Explainer-->>Flask: Match results + Rejection results + Summary

    Flask-->>HTMX: HTML partial (results_partial.html)
    HTMX->>Browser: Swap #results div content

    Browser->>Browser: Initialize Chart.js
    Note over Browser: Render match score bar chart

    Browser->>Browser: Smooth scroll to results

    Student->>Browser: Review matched scholarships
    Student->>Browser: Expand "Show Scoring Breakdown"
    Student->>Browser: Click "View Details" on scholarship

    Browser->>Flask: GET /explain/{scholarship_id}/{student_id}
    Flask->>RuleFilter: Re-run filters for this pair
    Flask->>Ranker: Re-calculate score
    Flask->>Explainer: Generate detailed explanation
    Flask-->>Browser: JSON with full explanation

    Student->>Student: Apply to scholarship
```

---

## 3. Decision Logic Architecture

**Description:** Hierarchical view of the DSS decision-making components.

```mermaid
graph TB
    subgraph Input Layer
        StudentProfile[Student Profile<br/>━━━━━━━━━━<br/>• GPA: 3.5<br/>• Course: CS<br/>• Age: 23<br/>• International: Yes<br/>• Keywords: AI, ML]
        ScholarshipPool[Scholarship Pool<br/>━━━━━━━━━━<br/>10 Active Scholarships<br/>from Firestore]
    end

    subgraph Stage A - Rule-Based Filter
        direction TB
        FilterEngine[Rule Filter Engine<br/>8 Hard Constraints]

        Rule1[1. GPA Filter<br/>student.gpa ≥ scholarship.min_gpa]
        Rule2[2. Course Filter<br/>student.course IN eligible_courses]
        Rule3[3. Nationality Filter<br/>student.nationality IN eligible_nationalities]
        Rule4[4. Deadline Filter<br/>deadline > today]
        Rule5[5. Age Filter<br/>student.age ≤ scholarship.age_max]
        Rule6[6. International Filter<br/>requires_international == is_international]
        Rule7[7. Gender Filter<br/>gender_required == student.gender]
        Rule8[8. Citizenship Filter<br/>citizenship_required → verify nationality]

        FilterEngine --> Rule1
        FilterEngine --> Rule2
        FilterEngine --> Rule3
        FilterEngine --> Rule4
        FilterEngine --> Rule5
        FilterEngine --> Rule6
        FilterEngine --> Rule7
        FilterEngine --> Rule8

        Rule1 --> FilterResult{All Rules<br/>Pass?}
        Rule2 --> FilterResult
        Rule3 --> FilterResult
        Rule4 --> FilterResult
        Rule5 --> FilterResult
        Rule6 --> FilterResult
        Rule7 --> FilterResult
        Rule8 --> FilterResult
    end

    subgraph Stage B - AHP Ranking
        direction TB
        RankEngine[AHP Weighted Ranker<br/>5 Scoring Factors]

        Factor1[GPA Buffer<br/>━━━━━━━━━━<br/>Weight: 0.25<br/>Formula: buffer / 4.0]
        Factor2[Keyword Match<br/>━━━━━━━━━━<br/>Weight: 0.25<br/>Formula: Jaccard similarity]
        Factor3[Competitiveness<br/>━━━━━━━━━━<br/>Weight: 0.20<br/>Formula: 1 - competitiveness]
        Factor4[Deadline Urgency<br/>━━━━━━━━━━<br/>Weight: 0.15<br/>Formula: urgency score]
        Factor5[Document Burden<br/>━━━━━━━━━━<br/>Weight: 0.15<br/>Formula: 1 - doc_count/max]

        RankEngine --> Factor1
        RankEngine --> Factor2
        RankEngine --> Factor3
        RankEngine --> Factor4
        RankEngine --> Factor5

        Factor1 --> WeightedSum[Σ weight_i × score_i]
        Factor2 --> WeightedSum
        Factor3 --> WeightedSum
        Factor4 --> WeightedSum
        Factor5 --> WeightedSum

        WeightedSum --> FinalScore[Final Score<br/>0.0 - 1.0]
    end

    subgraph Stage C - Explainability
        direction TB
        ExplainEngine[Explanation Generator]

        MatchPath[Matched Path<br/>━━━━━━━━━━<br/>• Met criteria list<br/>• Score breakdown<br/>• Recommendation]

        RejectPath[Rejected Path<br/>━━━━━━━━━━<br/>• Failed criteria list<br/>• Improvement tips<br/>• Alternative suggestions]

        ExplainEngine --> MatchPath
        ExplainEngine --> RejectPath
    end

    subgraph Output Layer
        Results[Student Results<br/>━━━━━━━━━━<br/>• Ranked matches<br/>• Rejections<br/>• Summary stats<br/>• Visualizations]
    end

    StudentProfile --> FilterEngine
    ScholarshipPool --> FilterEngine

    FilterResult -->|Pass| RankEngine
    FilterResult -->|Fail| ExplainEngine

    FinalScore --> ExplainEngine

    MatchPath --> Results
    RejectPath --> Results

    style StudentProfile fill:#e1f5e1
    style ScholarshipPool fill:#ffe6e6
    style FilterEngine fill:#fff4e6
    style RankEngine fill:#e6f3ff
    style ExplainEngine fill:#f0e6ff
    style Results fill:#e1f5e1
    style FilterResult fill:#ffcccc
    style WeightedSum fill:#cce5ff
    style FinalScore fill:#d1f2eb
```

---

## 4. System Architecture Overview

**Description:** High-level architecture showing all components and their interactions.

```mermaid
graph TB
    subgraph Client Side
        Browser[Web Browser<br/>TailwindCSS + HTMX]
        ChartJS[Chart.js<br/>Visualizations]
    end

    subgraph Flask Application
        direction TB

        subgraph Blueprints
            MatchBP[Match Blueprint<br/>/match/]
            ExplainBP[Explain Blueprint<br/>/explain/]
            AuditBP[Audit Blueprint<br/>/audit/]
        end

        subgraph Services
            RuleFilterSvc[RuleFilter<br/>8 Eligibility Rules]
            RankerSvc[ScholarshipRanker<br/>AHP Weighted Scoring]
            ExplainerSvc[Explainer<br/>Transparency Engine]
            FairnessSvc[FairnessAuditor<br/>Bias Detection]
        end

        subgraph Models
            StudentModel[Student Model]
            ScholarshipModel[Scholarship Model]
            MatchResultModel[MatchResult Model]
        end
    end

    subgraph Firebase
        Firestore[(Firestore Database<br/>━━━━━━━━━━<br/>• students<br/>• scholarships)]
        FirebaseAuth[Firebase Auth<br/>Future: User Login]
        FirebaseStorage[Firebase Storage<br/>Future: Documents]
    end

    subgraph External Data
        KaggleData[Kaggle Dataset<br/>Student Success Data]
        SyntheticData[Synthetic Scholarships<br/>10 Scholarships]
    end

    Browser -->|HTMX Request| MatchBP
    Browser -->|HTMX Request| ExplainBP
    Browser -->|HTTP GET| AuditBP

    MatchBP --> RuleFilterSvc
    MatchBP --> RankerSvc
    MatchBP --> ExplainerSvc

    ExplainBP --> RuleFilterSvc
    ExplainBP --> RankerSvc
    ExplainBP --> ExplainerSvc

    AuditBP --> RuleFilterSvc
    AuditBP --> RankerSvc
    AuditBP --> FairnessSvc

    RuleFilterSvc --> StudentModel
    RuleFilterSvc --> ScholarshipModel
    RankerSvc --> StudentModel
    RankerSvc --> ScholarshipModel
    ExplainerSvc --> MatchResultModel

    MatchBP --> Firestore
    ExplainBP --> Firestore
    AuditBP --> Firestore

    KaggleData -.->|Preprocessed| Firestore
    SyntheticData -.->|Loaded| Firestore

    MatchBP -->|HTML Partial| Browser
    ExplainBP -->|JSON| Browser
    AuditBP -->|HTML + Charts| Browser

    Browser --> ChartJS

    style Browser fill:#e1f5e1
    style Firestore fill:#ffe6e6
    style RuleFilterSvc fill:#fff4e6
    style RankerSvc fill:#e6f3ff
    style ExplainerSvc fill:#f0e6ff
    style FairnessSvc fill:#ffebe6
    style ChartJS fill:#e1f5e1
```

---

## 5. Fairness Audit Process Flow

**Description:** How the fairness auditing system detects bias.

```mermaid
flowchart TD
    Start([Fairness Audit Triggered]) --> FetchAll[Fetch All Students<br/>& Scholarships]

    FetchAll --> RunMatching[Run Matching Engine<br/>for ALL Students]

    RunMatching --> Results[Student Match Results<br/>500 students × 10 scholarships]

    Results --> Segment[Demographic Segmentation]

    Segment --> Group1[Gender Groups<br/>• Female: 461 students<br/>• Male: 39 students]
    Segment --> Group2[Nationality Groups<br/>• Domestic: 495 students<br/>• International: 5 students]
    Segment --> Group3[GPA Bands<br/>• Low <2.5: 256 students<br/>• Mid 2.5-3.2: 241 students<br/>• High >3.2: 3 students]
    Segment --> Group4[Scholarship Status<br/>• Has scholarship: 142<br/>• No scholarship: 358]

    Group1 --> CalcRate1[Calculate Match Rate<br/>Female: 2.02 avg matches/student<br/>Male: 1.23 avg matches/student]
    Group2 --> CalcRate2[Calculate Match Rate<br/>Domestic: 1.97 avg<br/>International: 0.40 avg]
    Group3 --> CalcRate3[Calculate Match Rate<br/>Low: 1.14 avg<br/>Mid: 2.80 avg<br/>High: 4.33 avg]
    Group4 --> CalcRate4[Calculate Match Rate<br/>Has: 2.38 avg<br/>No: 1.79 avg]

    CalcRate1 --> Gap1{Gap > 0.15<br/>Threshold?}
    CalcRate2 --> Gap2{Gap > 0.15<br/>Threshold?}
    CalcRate3 --> Gap3{Gap > 0.15<br/>Threshold?}
    CalcRate4 --> Gap4{Gap > 0.15<br/>Threshold?}

    Gap1 -->|Yes| Alert1[🚨 BIAS ALERT<br/>Gender Gap: 0.79]
    Gap2 -->|Yes| Alert2[🚨 BIAS ALERT<br/>Nationality Gap: 1.57]
    Gap3 -->|Yes| Alert3[🚨 BIAS ALERT<br/>GPA Gap: 3.19]
    Gap4 -->|Yes| Alert4[🚨 BIAS ALERT<br/>Scholarship Holder Gap: 0.59]

    Gap1 -->|No| NoAlert1[✅ Fair]
    Gap2 -->|No| NoAlert2[✅ Fair]
    Gap3 -->|No| NoAlert3[✅ Fair]
    Gap4 -->|No| NoAlert4[✅ Fair]

    Alert1 --> Dashboard[Fairness Dashboard]
    Alert2 --> Dashboard
    Alert3 --> Dashboard
    Alert4 --> Dashboard
    NoAlert1 --> Dashboard
    NoAlert2 --> Dashboard
    NoAlert3 --> Dashboard
    NoAlert4 --> Dashboard

    Dashboard --> Visualize[Chart.js Visualizations<br/>• Pie charts<br/>• Bar charts<br/>• Alert cards]

    Visualize --> Report[Fairness Report<br/>• Demographic breakdown<br/>• Bias alerts<br/>• Recommendations]

    Report --> End([Admin Reviews & Acts])

    style Start fill:#e1f5e1
    style Alert1 fill:#ffcccc
    style Alert2 fill:#ffcccc
    style Alert3 fill:#ffcccc
    style Alert4 fill:#ffcccc
    style NoAlert1 fill:#ccffcc
    style NoAlert2 fill:#ccffcc
    style NoAlert3 fill:#ccffcc
    style NoAlert4 fill:#ccffcc
    style Dashboard fill:#e6f3ff
    style End fill:#e1f5e1
```

---

## 6. Database Schema (Firestore Collections)

**Description:** Firestore collections and document structure.

```mermaid
erDiagram
    STUDENTS {
        string student_id PK
        float gpa
        int course
        int gender
        int age
        boolean is_international
        int nationality
        boolean current_scholarship_holder
        array keywords
        timestamp created_at
    }

    SCHOLARSHIPS {
        string id PK
        string name
        string provider
        float amount
        string currency
        int duration_months
        float min_gpa
        array eligible_courses
        array eligible_nationalities
        boolean citizenship_required
        int age_max
        boolean requires_international
        int gender_required
        datetime deadline
        array required_documents
        string description
        float competitiveness
        array keywords
    }

    STUDENTS ||--o{ MATCH_RESULTS : "matches with"
    SCHOLARSHIPS ||--o{ MATCH_RESULTS : "matched to"

    MATCH_RESULTS {
        string student_id FK
        string scholarship_id FK
        boolean matched
        float score
        int ranking
        array met_criteria
        array failed_criteria
        object scoring_breakdown
        string recommendation
        timestamp created_at
    }
```

---

## Notes

- All diagrams are in Mermaid format (Markdown-compatible)
- Can be rendered in GitHub, GitLab, VS Code, and online tools
- Easy to edit and version control
- Export to PNG/SVG for reports using mermaid.live or VS Code

---

**Created:** 2026-01-10
**For:** Scholarship Matching DSS - UE Course Project
**Professor:** George
