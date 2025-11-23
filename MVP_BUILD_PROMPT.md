# CLAUDE_CODE_MVP_BUILD_PROMPT.md

## Purpose
This markdown file contains the full prompt for instructing a coding-focused LLM agent (such as Claude Code) to build the **Actuarial Insights Workbench (MVP)** based on the previously generated VISION.md, ARCHITECTURE.md, and README.md files.

---

# ✅ **MVP Build Prompt for Claude Code**

## **TITLE:**  
**Build the Actuarial Insights Workbench (MVP) Based on README, VISION, and ARCHITECTURE Files**

---

## **INSTRUCTIONS TO THE AGENT (Claude Code):**

You are an expert full-stack engineer and solution architect.  
Your job is to read and fully understand the following three markdown documents and then build the smallest, fastest, high-impact MVP of the **Actuarial Insights Workbench** as defined in these files:

- **VISION.md**  
- **ARCHITECTURE.md**  
- **README.md**

These documents are located at:

- `/mnt/data/VISION.md`  
- `/mnt/data/ARCHITECTURE.md`  
- `/mnt/data/README.md`  

**Before you build anything, load and deeply analyze all three files.**

---

# **OBJECTIVE**

Using the details from the three markdown documents, build a fully functional **minimum viable prototype** containing:

- A **Streamlit UI**  
- A **FastAPI backend**  
- A **lightweight ML model** (scikit-learn) for expected loss ratio or severity prediction  
- Simple **actuarial visualizations** (loss triangles, LR trends, underwriting KPIs)  
- A basic **GenAI explanation tool** using OpenAI  
- A professional repo structure  
- Fully runnable locally

---

# **REQUIRED DELIVERABLES**

Claude Code must produce:

## **1. Full Repo Structure**
```
actuarial-insights-workbench/
│
├── README.md
├── VISION.md
├── ARCHITECTURE.md
│
├── ui/
│   ├── app.py
│   └── components/
│
├── app/
│   ├── main.py
│   ├── model.pkl
│   ├── features.py
│   ├── loss_triangle.py
│   ├── segment_kpis.py
│   └── explain.py
│
├── data/
│   ├── policies.csv
│   ├── claims.csv
│   └── exposure.csv
│
├── notebooks/
│   ├── data_prep.ipynb
│   ├── loss_triangle.ipynb
│   └── model_training.ipynb
│
└── requirements.txt
```

---

# **MVP FEATURE REQUIREMENTS**

## **(A) Data Layer**
Generate synthetic but actuarially-plausible P&C datasets:
- policies.csv  
- claims.csv  
- exposure.csv  

## **(B) Streamlit UI**
Pages:
1. **Loss Development Dashboard** (triangle + severity/frequency trends)  
2. **Pricing & Portfolio KPIs**  
3. **Risk Score & Expected LR Prediction**  
4. **GenAI Explanation Panel**  

## **(C) ML Model**
- RandomForestRegressor  
- Predict expected LR or severity  
- Save as model.pkl  

## **(D) FastAPI Backend**
Endpoints:
- `/predict`  
- `/segment_insights`  
- `/loss_triangle`  
- `/explain`  

## **(E) GenAI Layer**
- Accept question  
- Integrate simple OpenAI call (or stub)  
- Return structured JSON explanation  

---

# **REQUIREMENTS FILE**
Include:
```
streamlit
fastapi
uvicorn
pandas
numpy
scikit-learn
matplotlib
seaborn
plotly
openai
```

---

# **CODING STANDARDS**
- Clean, modular Python files  
- Clear comments & function boundaries  
- Typed functions where reasonable  
- Simple, attractive Streamlit UI  

---

# **BEFORE WRITING ANY CODE**
Claude Code must:

1. Load `/mnt/data/VISION.md`  
2. Load `/mnt/data/ARCHITECTURE.md`  
3. Load `/mnt/data/README.md`  
4. Provide a summary  
5. Wait for user confirmation  
6. Only then begin building the repo

---

# **FINAL NOTE**
Build ONLY what aligns to the documents above.  
Focus on clarity, maintainability, and MVP-level functionality.

