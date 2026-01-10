# System Diagrams - PNG Files

All diagrams ready for use in your report!

## 📊 Available Diagrams

### 1. Data Flow Diagram
**File:** `1-data-flow-diagram.png` (96 KB, 784×1419)
**Use in:** Methodology section - Data flow architecture
**Shows:** Complete flow from student input through filtering, ranking, to results

---

### 2. User Interaction Sequence
**File:** `2-user-interaction-sequence.png` (90 KB, 784×1195)
**Use in:** Methodology section - User interaction
**Shows:** HTMX-based sequence: Browser → Flask → Firestore → Results

---

### 3. Decision Logic Architecture
**File:** `3-decision-logic-architecture.png` (57 KB, 784×655)
**Use in:** Methodology section - DSS architecture
**Shows:** 3-stage pipeline (Filter → Rank → Explain) with 8 rules + 5 AHP factors

---

### 4. System Architecture Overview
**File:** `4-system-architecture.png` (38 KB, 784×261)
**Use in:** Implementation section - Tech stack
**Shows:** Flask blueprints, services, Firestore, frontend components

---

### 5. Fairness Audit Flow
**File:** `5-fairness-audit-flow.png` (73 KB, 784×894)
**Use in:** Methodology/Results - Fairness framework
**Shows:** Bias detection across 4 demographic groups

---

### 6. Database Schema
**File:** `6-database-schema.png` (103 KB, 784×1308)
**Use in:** Implementation section - Data model
**Shows:** Firestore collections (students, scholarships, match_results)

---

## 📝 How to Use in Report

### MS Word / Google Docs:
1. Insert → Image
2. Select PNG file
3. Add caption: "Figure X: [Diagram title]"

### LaTeX:
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{diagrams/1-data-flow-diagram.png}
    \caption{Data flow from student input to final recommendations}
    \label{fig:dataflow}
\end{figure}
```

### Markdown:
```markdown
![Data Flow Diagram](diagrams/1-data-flow-diagram.png)
*Figure 1: Data flow from student input to final recommendations*
```

---

## ✅ Quality Check

All diagrams:
- ✅ High resolution (784px width)
- ✅ PNG format (transparent background where applicable)
- ✅ Professional styling
- ✅ Clear labels and colors
- ✅ Ready for print

---

**Generated:** 2026-01-10
**Tool:** Mermaid CLI (mmdc)
**Source:** `/docs/SYSTEM_DIAGRAMS.md`
