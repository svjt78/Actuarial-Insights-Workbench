# ARCHITECTURE.md

## Architectural Overview

```mermaid
flowchart TD
    A[Raw Insurance Data<br>(Policies, Claims, Exposure)] --> B[Data Prep & ETL<br>Python/Spark]
    B --> C[Feature Store<br>(Loss Metrics, Segments, Rating Factors)]
    C --> D[ML Model<br>Predict Severity/LR]
    D --> E[FastAPI Service<br>Model Serving]
    C --> F[Streamlit Dashboard<br>Actuarial Insights]
    E --> F
    F --> G[GenAI Layer<br>Explanation Engine]
```

## Core Components
### 1. Data Layer
- Synthetic P&C dataset.
- Loss development triangles.
- Underwriting segmentation.

### 2. Transform & Feature Engineering
- Severity, frequency, LR calc.
- Risk factor extraction.

### 3. ML Layer
- Random Forest / LightGBM model.
- Prediction: Expected Loss Ratio, Claim Severity.

### 4. API Layer
- FastAPI service hosting the model.
- Endpoints:
  - `/predict`
  - `/segment_insights`
  - `/explain`

### 5. UI Layer
- Streamlit app with:
  - Loss triangles
  - Pricing KPI dashboard
  - Risk scoring
  - GenAI explanation box

