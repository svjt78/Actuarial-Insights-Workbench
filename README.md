# Actuarial Insights Workbench

**An open-source, AI-powered actuarial analytics platform for Commercial Property insurance**

Combining proven actuarial methodologies (chain-ladder, loss development) with modern ML/AI capabilities (LightGBM, OpenAI GPT-3.5) to deliver enterprise-grade analytics at zero licensing cost.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Why Choose AIW?](#-why-choose-aiw)
- [Documentation](#-documentation)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Data](#-data)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Performance](#-performance)
- [Use Cases](#-use-cases)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🎯 Overview

### What Is AIW?

Actuarial Insights Workbench (AIW) is a comprehensive analytics platform designed for actuaries, underwriters, and insurance analysts working with Commercial Property portfolios. It provides:

- **Loss Development Analysis** - Automated triangle generation, IBNR estimation, and reserve projections
- **ML-Powered Predictions** - Risk-based loss ratio and severity forecasting using LightGBM
- **Segment Analytics** - Multi-dimensional KPI analysis across geography, industry, and risk characteristics
- **GenAI Insights** - Natural language explanations and Q&A powered by OpenAI GPT-3.5

### The Problem We Solve

Traditional actuarial software is:
- **Expensive** - Enterprise tools cost $100k-$500k+ annually
- **Slow** - Hours spent in spreadsheets for routine analyses
- **Opaque** - Proprietary calculations in black-box systems
- **Complex** - 3-12 month implementations, steep learning curves

Small and mid-sized insurers, as well as InsurTech startups, are often priced out of enterprise-grade actuarial tools.

### Our Solution

AIW delivers professional actuarial analytics with:
- ⚡ **<100ms** prediction latency
- 💰 **$0** licensing fees (open source)
- 🚀 **15 minutes** to deploy (Docker-based)
- 📊 **4 integrated dashboards** covering the complete workflow
- 🔍 **Full transparency** - auditable code and calculations

---

## ✨ Key Features

### 1. Loss Development Dashboard
- **Cumulative and incremental loss triangles** with monthly granularity
- **Age-to-age development factors** using volume-weighted averages
- **Ultimate loss projections** via chain-ladder method
- **IBNR estimation** with development patterns up to 36 months
- **Interactive heatmaps** and downloadable reports
- Real-time triangle recalculation with configurable parameters

### 2. Pricing & Portfolio KPIs
- **Multi-dimensional segmentation** by Geography, Industry, Policy Size, Risk Rating
- **Core metrics**: Loss Ratio, Frequency, Severity, Pure Premium
- **Frequency vs Severity scatter analysis** for segment comparison
- **Top/bottom performer identification** for portfolio optimization
- **Downloadable CSV reports** for external analysis
- **Overall portfolio benchmarks** vs segment performance

### 3. Risk Prediction Engine
- **Loss Ratio prediction** using LightGBM regression (MAE: 78.81)
- **Claim Severity prediction** using LightGBM regression (MAE: $131,291)
- **Confidence intervals** with uncertainty quantification
- **Feature importance analysis** across 6 input features
- **Interactive risk scoring** with real-time feedback
- **Batch prediction support** for portfolio-wide analysis

### 4. GenAI Insights
- **Natural language Q&A** about portfolio metrics and trends
- **Loss ratio explanations** with actuarial context
- **Trend analysis and interpretation** across segments
- **COPE risk rating explanations** (Construction, Occupancy, Protection, Exposure)
- **Powered by OpenAI GPT-3.5-turbo** with 30-second timeout
- Context-aware responses using portfolio data

---

## 🏆 Why Choose AIW?

### vs. Enterprise Actuarial Software

| Feature | AIW | Milliman Arius | SAS Insurance | Earnix | WTW Radar |
|---------|-----|----------------|---------------|--------|-----------|
| **Annual Cost** | $0 (open source) | $50k-$200k | $100k-$500k+ | $75k-$300k | $30k-$100k |
| **Deployment Time** | 15 minutes | 6+ months | 6-12 months | 3-6 months | 1-3 months |
| **GenAI Integration** | ✅ Native | ❌ Not available | ❌ Not available | ⚠️ Add-on | ❌ Not available |
| **Open Source** | ✅ Fully auditable | ❌ Proprietary | ❌ Proprietary | ❌ Proprietary | ❌ Proprietary |
| **ML Predictions** | ✅ Trainable models | ⚠️ Limited | ✅ Advanced | ⚠️ Limited | ❌ Not included |
| **Cloud-Ready** | ✅ Docker-native | ⚠️ Legacy | ✅ Cloud | ✅ SaaS | ❌ Desktop only |
| **API Access** | ✅ Full REST API | ⚠️ Limited | ⚠️ Add-on | ✅ Yes | ❌ None |
| **Customization** | ✅ Full control | ❌ Vendor-locked | ⚠️ Limited | ⚠️ Limited | ❌ None |

### Key Advantages

1. **Zero Licensing Costs** - No per-user fees, no annual contracts, no hidden charges
2. **Rapid Deployment** - Production-ready in minutes with Docker Compose
3. **Modern AI Integration** - Built-in GenAI and ML, not bolted-on afterthoughts
4. **Full Transparency** - Inspect every calculation, audit every formula
5. **Developer-Friendly** - REST API, Python ecosystem, extensible architecture
6. **Actuarial Rigor** - Implements standard methodologies (chain-ladder, frequency-severity)

---

## 📚 Documentation

Comprehensive documentation is available for all user types:

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute guide to get up and running
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation and configuration
- **[POST_SETUP_INSTRUCTIONS.md](POST_SETUP_INSTRUCTIONS.md)** - Next steps after installation

### Business & Strategy
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Value proposition, competitive analysis, ROI
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Feature overview, deliverables, roadmap
- **[COMPETITIVE_ANALYSIS.md](COMPETITIVE_ANALYSIS.md)** - Detailed comparison vs enterprise tools
- **[EXECUTIVE_WALKTHROUGH.md](EXECUTIVE_WALKTHROUGH.md)** - Business user guide with screenshots

### Collaboration & Workflows
- **[ACTUARY_UNDERWRITER_COLLAB.md](ACTUARY_UNDERWRITER_COLLAB.md)** - Cross-functional workflows
- **[AGENTS.md](AGENTS.md)** - AI agent architecture and capabilities

### Technical Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, microservices, data flow
- **[CLAUDE.md](CLAUDE.md)** - Developer guide for Claude Code (AI pair programming)
- **[HOT_RELOAD_GUIDE.md](HOT_RELOAD_GUIDE.md)** - Development workflow with live reloading
- **[DELIVERABLES.md](DELIVERABLES.md)** - Complete list of project deliverables

### Actuarial Methodology
- **[LOSS_DEVELOPMENT_FORMULAS.md](LOSS_DEVELOPMENT_FORMULAS.md)** - Chain-ladder method, age-to-age factors, IBNR
- **[PRICING_KPIS_FORMULAS.md](PRICING_KPIS_FORMULAS.md)** - Loss ratio, frequency, severity, pure premium
- **[RISK_PREDICTION_FORMULAS.md](RISK_PREDICTION_FORMULAS.md)** - ML model specifications, feature engineering

### Project History
- **[CHANGELOG.md](CHANGELOG.md)** - Version history, bug fixes, improvements
- **[VISION.md](VISION.md)** - Strategic roadmap and future capabilities
- **[MODEL_TRAINING_FIX.md](MODEL_TRAINING_FIX.md)** - Deep dive into ML model training resolution
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - Model performance benchmarks

---

## 🚀 Quick Start

### Prerequisites
- **Docker** and **Docker Compose** installed
- **OpenAI API key** (for GenAI features - optional for other modules)
- **8GB RAM** minimum recommended
- **Ports 8003 and 8502** available

### Installation

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd actuarial-insights-workbench
```

**2. Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key (optional)
nano .env
```

Add to `.env`:
```bash
OPENAI_API_KEY=your_openai_api_key_here  # Optional: Required only for GenAI tab
BACKEND_HOST=backend
BACKEND_PORT=8003
ENVIRONMENT=development
```

**3. Build and start services**
```bash
docker-compose up --build
```

This will:
- Build backend (FastAPI) and frontend (Streamlit) containers
- Start backend API on `http://localhost:8003`
- Start frontend UI on `http://localhost:8502`
- Load 1,000 policies, 114 claims, 17,865 exposure records

**4. Access the application**
- **Frontend Dashboard**: http://localhost:8502
- **Backend API**: http://localhost:8003
- **Interactive API Docs**: http://localhost:8003/docs
- **Health Check**: http://localhost:8003/health

### First-Time Setup: Train ML Models

**CRITICAL**: After starting services, train the ML models for real predictions. Without trained models, the application falls back to static rules:
- Loss Ratio: Always 65%
- Severity: Policy-size-based ($50k/$100k/$250k/$500k)

**Train the models:**
```bash
# Train both Loss Ratio and Severity models
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Restart backend to load the trained models
docker-compose restart backend

# Verify models loaded successfully
docker logs aiw-backend | grep "Loaded"
# Expected output:
# ✅ Loaded Loss Ratio model from /app/models/lr_model.pkl
# ✅ Loaded Severity model from /app/models/severity_model.pkl
```

**What this does:**
- Trains LightGBM models on 1,000 policies and 114 claims
- Creates `backend/models/lr_model.pkl` (Loss Ratio model, ~130 KB)
- Creates `backend/models/severity_model.pkl` (Severity model, ~47 KB)
- Models persist via Docker volume mount

**Model Performance:**
- **Loss Ratio Model**: MAE 78.81, trained on 800 samples, 6 features
- **Severity Model**: MAE $131,291, trained on 86 policies with claims, R² 0.37

**Verify it worked:**
```bash
curl http://localhost:8003/health
# Should return: {"status":"healthy","data_loaded":true,"model_loaded":true}
```

---

## 🧱 Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Streamlit)                     │
│                      Port 8502                               │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Loss Dev     │ Pricing KPIs │ Risk Predict │ GenAI Insights │
│ Dashboard    │ Dashboard    │ Dashboard    │ Dashboard      │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │              │              │                │
       └──────────────┴──────────────┴────────────────┘
                         │
                         │ HTTP/REST
                         ▼
       ┌────────────────────────────────────────────┐
       │       BACKEND (FastAPI) - Port 8003        │
       ├────────────────────────────────────────────┤
       │  API Layer (9 RESTful endpoints)           │
       ├──────────┬─────────┬──────────┬────────────┤
       │ Loss     │ Segment │ Predict  │ Explain    │
       │ Triangle │ KPIs    │ Service  │ Service    │
       │ Service  │ Service │ (ML)     │ (GenAI)    │
       └──────┬───┴─────┬───┴──────┬───┴────────┬───┘
              │         │          │            │
              └─────────┴──────────┴────────────┘
                         │
                         ▼
       ┌────────────────────────────────────────────┐
       │         DATA LAYER (CSV Files)             │
       ├────────────────────────────────────────────┤
       │ • policies.csv      (1,000 records)        │
       │ • claims.csv        (114 records)          │
       │ • exposure.csv      (17,865 records)       │
       └────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- Streamlit 1.29+ - Interactive dashboards
- Plotly - Interactive charts
- Matplotlib/Seaborn - Statistical visualizations
- Requests - API communication

**Backend:**
- FastAPI 0.109 - REST API framework
- Uvicorn - ASGI server with auto-reload
- Pydantic 2.5 - Request/response validation
- Python-dotenv - Environment configuration

**ML/AI:**
- LightGBM 4.3 - Gradient boosting models
- Scikit-learn 1.4 - Feature encoding, metrics
- OpenAI 1.10 - GPT-3.5-turbo integration
- Joblib - Model serialization

**Data:**
- Pandas 2.1 - DataFrame operations
- NumPy 1.26 - Numerical computing

**Infrastructure:**
- Docker & Docker Compose - Containerization
- Git - Version control

### Service Architecture

The backend uses **isolated service modules** for maintainability:

1. **`services/loss_triangle.py`** - Loss development calculations (chain-ladder)
2. **`services/segment_kpis.py`** - Portfolio KPI aggregation and analysis
3. **`services/prediction.py`** - ML model serving (LightGBM)
4. **`services/explain.py`** - GenAI explanation generation (OpenAI)

Each service is **stateless** and initialized on backend startup. Services share read-only access to CSV data mounted via Docker volumes.

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 📊 Data

### Synthetic Data Generation

The platform uses actuarially-sound synthetic data for Commercial Property insurance:

| Dataset | Records | Description |
|---------|---------|-------------|
| **policies.csv** | 1,000 | Policy attributes (geography, industry, risk rating, premium) |
| **claims.csv** | 114 | Claims with incurred/paid amounts, development months |
| **exposure.csv** | 17,865 | Monthly earned premium exposure by policy-period |

**Time Period**: 3 accident years (2022-2024)

**Segmentation Dimensions:**
- **Geography**: Northeast, Southeast, Midwest, Southwest, West, Northwest
- **Industry**: Manufacturing, Retail, Office, Warehouse, Healthcare, Education, Hospitality, Technology
- **Policy Size**: Small, Medium, Large, Enterprise
- **Risk Rating**: COPE-based scale from 1.0 (best) to 10.0 (worst)

### Data Quality Features

- **COPE-based risk ratings** (Construction, Occupancy, Protection, Exposure)
- **Geographic variation** in loss patterns and premium levels
- **Industry-specific** severity distributions
- **Realistic development patterns** following standard actuarial curves
- **Correlated features** (higher risk ratings → higher loss ratios)

### Regenerate Data

To create fresh synthetic data:

```bash
docker exec aiw-backend bash -c "cd .. && python scripts/generate_data.py"
docker-compose restart backend

# After data regeneration, retrain models:
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"
docker-compose restart backend
```

---

## 📖 API Documentation

### Endpoints Overview

**Predictions (POST):**
- `POST /predict/loss_ratio` - Predict expected loss ratio for a policy
- `POST /predict/severity` - Predict expected claim severity
- `POST /predict/both` - Get both predictions in one call

**Analytics (GET):**
- `GET /segment_insights?segment_by=Geography&min_premium=0` - Segment-level KPIs
- `GET /loss_triangle?value_col=IncurredAmount&triangle_type=cumulative&max_dev_months=36` - Loss development triangle

**GenAI (POST):**
- `POST /explain` - Generate natural language explanations (4 types: question, loss_ratio, trend, cope_rating)

**Utility (GET):**
- `GET /health` - Health check and status
- `GET /data_summary` - Dataset statistics and summary
- `GET /feature_importance/{model_type}` - Model feature importance (loss_ratio or severity)

### Example: Loss Ratio Prediction

**Request:**
```bash
curl -X POST "http://localhost:8003/predict/loss_ratio" \
  -H "Content-Type: application/json" \
  -d '{
    "geography": "Northeast",
    "industry": "Manufacturing",
    "policy_size": "Medium",
    "risk_rating": 6.5,
    "exposure_units": 50.0,
    "annual_premium": 25000.0
  }'
```

**Response:**
```json
{
  "prediction": 68.34,
  "confidence_interval": {
    "lower": 45.12,
    "upper": 91.56
  },
  "model_type": "loss_ratio",
  "model_loaded": true
}
```

### Interactive API Documentation

Full Swagger/OpenAPI documentation with interactive testing available at:
**http://localhost:8003/docs**

---

## 🛠 Development

### Local Development (without Docker)

**1. Install Python 3.11+**

**2. Install dependencies**
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

**3. Generate synthetic data**
```bash
cd scripts
python generate_data.py
cd ..
```

**4. Train ML models**
```bash
cd scripts
python train_models.py
cd ..
```

**5. Start backend** (Terminal 1)
```bash
cd backend
uvicorn main:app --reload --port 8003
```

**6. Start frontend** (Terminal 2)
```bash
cd frontend
streamlit run app.py --server.port 8502
```

### Development with Docker (Recommended)

Docker volumes enable **hot reloading** - code changes reflect immediately without rebuilding:

```bash
# Start services
docker-compose up

# In another terminal, edit any .py file
# Changes auto-reload in both backend and frontend

# View logs
docker logs -f aiw-backend   # Backend logs
docker logs -f aiw-frontend  # Frontend logs

# Restart specific service (if needed)
docker-compose restart backend
```

For detailed hot reload workflows, see [HOT_RELOAD_GUIDE.md](HOT_RELOAD_GUIDE.md).

### Project Structure

```
actuarial-insights-workbench/
├── README.md                       # This file
├── .env.example                    # Environment template
├── docker-compose.yml              # Docker orchestration
├── requirements.txt                # Root dependencies (optional)
│
├── backend/                        # FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                     # API endpoints (9 endpoints)
│   ├── services/
│   │   ├── loss_triangle.py        # Loss development calculations
│   │   ├── segment_kpis.py         # KPI calculations
│   │   ├── prediction.py           # ML model serving
│   │   └── explain.py              # GenAI explanations
│   ├── models/                     # Trained ML models (created by training)
│   │   ├── lr_model.pkl            # Loss Ratio model (~130 KB)
│   │   └── severity_model.pkl      # Severity model (~47 KB)
│   └── tests/                      # Unit tests (85%+ coverage)
│       ├── test_loss_triangle.py
│       ├── test_segment_kpis.py
│       └── test_prediction.py
│
├── frontend/                       # Streamlit UI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                      # Landing page
│   └── pages/
│       ├── 1_Loss_Development.py   # Loss triangles, IBNR
│       ├── 2_Pricing_KPIs.py       # Segment analytics
│       ├── 3_Risk_Prediction.py    # ML predictions
│       └── 4_GenAI_Insights.py     # Natural language Q&A
│
├── data/                           # Synthetic datasets
│   ├── policies.csv                # 1,000 policies
│   ├── claims.csv                  # 114 claims
│   └── exposure.csv                # 17,865 exposure records
│
├── scripts/                        # Utility scripts
│   ├── generate_data.py            # Synthetic data generation
│   └── train_models.py             # ML model training
│
├── notebooks/                      # Jupyter notebooks (planned)
│   └── (empty - placeholder for analysis notebooks)
│
└── docs/                           # Documentation (see Documentation section)
    ├── ARCHITECTURE.md
    ├── VISION.md
    ├── QUICKSTART.md
    └── [22 additional .md files]
```

### Common Development Commands

```bash
# === Docker Management ===
docker-compose up --build          # Build and start (first time)
docker-compose up                  # Start services
docker-compose down                # Stop and remove containers
docker-compose restart backend     # Restart specific service

# === Data & Models ===
docker exec aiw-backend bash -c "cd .. && python scripts/generate_data.py"   # Regenerate data
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"    # Train models

# === Testing ===
docker exec aiw-backend pytest tests/ -v --cov=services                      # Run all tests
docker exec aiw-backend pytest tests/test_prediction.py -v                   # Run specific test

# === Debugging ===
docker logs -f aiw-backend                                                   # Tail backend logs
docker logs aiw-backend --tail 50                                           # Last 50 lines
docker exec -it aiw-backend bash                                            # Enter backend shell
docker exec -it aiw-frontend bash                                           # Enter frontend shell

# === Health Checks ===
curl http://localhost:8003/health                                            # Backend health
curl http://localhost:8003/data_summary                                      # Data statistics
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests with coverage report
docker exec aiw-backend pytest tests/ -v --cov=services

# Run specific test file
docker exec aiw-backend pytest tests/test_prediction.py -v

# Run single test function
docker exec aiw-backend pytest tests/test_prediction.py::test_feature_encoding -v

# Generate HTML coverage report
docker exec aiw-backend pytest tests/ --cov=services --cov-report=html
# View report: backend/htmlcov/index.html
```

### Test Coverage

Current test coverage: **85%+**

**Test Files:**
- `test_loss_triangle.py` - Chain-ladder method, development factors, IBNR calculations
- `test_segment_kpis.py` - KPI formulas, aggregations, segment filtering, benchmarking
- `test_prediction.py` - Feature encoding, model predictions, confidence intervals

**Testing Philosophy:**
- Each test file mirrors a service module
- Tests use synthetic fixture data, not production CSV files
- Focus on business logic correctness and edge cases
- Validate actuarial formula implementations

---

## 🐛 Troubleshooting

### 1. Models Not Loading / Static Predictions

**Symptom**: Predictions always return fixed values (Loss Ratio: 65%, Severity: policy-size based)

**Root Cause**: ML models haven't been trained yet

**Solution**:
```bash
# Train the models
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Restart backend to load trained models
docker-compose restart backend

# Verify models loaded
docker logs aiw-backend | grep "Loaded"
# Expected: "✅ Loaded Loss Ratio model" and "✅ Loaded Severity model"

# Check health endpoint
curl http://localhost:8003/health
# Should return: {"status":"healthy","data_loaded":true,"model_loaded":true}
```

**Note**: The training script was fixed on 2024-11-24 to handle a column merge conflict. If using an older version, update to the latest `scripts/train_models.py`.

### 2. Backend Connection Errors

**Symptom**: Frontend shows "Connection refused" or "Cannot connect to backend"

**Diagnosis**:
```bash
# Check if backend container is running
docker ps | grep aiw-backend

# Check backend logs for errors
docker logs aiw-backend --tail 50

# Check if backend is healthy
curl http://localhost:8003/health
```

**Solution**:
```bash
# Restart backend
docker-compose restart backend

# If still failing, check for port conflicts
lsof -i :8003

# Rebuild if necessary
docker-compose down
docker-compose up --build
```

### 3. Port Already in Use

**Symptom**: "Address already in use" error on ports 8003 or 8502

**Solution**:
```bash
# Find process using the port
lsof -i :8003   # Backend
lsof -i :8502   # Frontend

# Kill the process (replace PID)
kill -9 <PID>

# Or use different ports in docker-compose.yml
# Change "8003:8003" to "8004:8003" for backend
# Change "8502:8502" to "8503:8502" for frontend
```

### 4. GenAI Features Not Working

**Symptom**: GenAI Insights tab shows errors, timeouts, or "API key not configured"

**Checklist**:
1. Verify `OPENAI_API_KEY` is set in `.env` file
2. Check API key is valid at https://platform.openai.com/api-keys
3. Ensure you have API credits available in your OpenAI account
4. Note: GenAI requests have 30-second timeout (normal for API calls)

**Solution**:
```bash
# Check if API key is loaded
docker exec aiw-backend printenv | grep OPENAI_API_KEY

# Restart backend after updating .env
docker-compose restart backend

# Test explanation endpoint
curl -X POST "http://localhost:8003/explain" \
  -H "Content-Type: application/json" \
  -d '{"explanation_type":"question","data":{"question":"What is a loss ratio?"}}'
```

### 5. Data Changes Not Reflected

**Symptom**: Modified CSV files don't show updated data in dashboards

**Root Cause**: Backend loads data on startup only

**Solution**:
```bash
# Restart backend to reload data
docker-compose restart backend

# Verify data loaded
curl http://localhost:8003/data_summary
```

### 6. Model Training Fails

**Symptom**: Training script fails with `KeyError` or column not found errors

**Common Causes**:
- Column name conflicts during pandas merge (duplicate columns)
- Missing columns in source CSV files
- Incorrect working directory when running script

**Solution**:
```bash
# Ensure you're running from correct directory in Docker
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Check data files exist and have correct columns
docker exec aiw-backend bash -c "head -1 data/policies.csv"
docker exec aiw-backend bash -c "head -1 data/claims.csv"
docker exec aiw-backend bash -c "head -1 data/exposure.csv"

# If data is corrupted, regenerate
docker exec aiw-backend bash -c "cd .. && python scripts/generate_data.py"
```

For more troubleshooting help, see [CLAUDE.md](CLAUDE.md) section "Common Gotchas".

---

## 📈 Performance

### Benchmarks

- **Backend Startup**: ~2-3 seconds (loads 17,865 exposure records)
- **ML Prediction**: <100ms per request
- **Triangle Calculation**: <500ms for 36-month development
- **GenAI Explanation**: 2-5 seconds (OpenAI API latency)
- **Segment KPI Aggregation**: <200ms across 4 dimensions
- **Throughput**: ~100 requests/second (backend)

### Scalability Characteristics

**Current Capacity** (single Docker host):
- 1,000 policies, 114 claims, 17,865 exposure records
- Multiple concurrent frontend users
- Sub-second response times for most operations

**Bottlenecks**:
1. **GenAI API calls** - External OpenAI latency (2-5s)
2. **Large dataset aggregations** - In-memory pandas operations (>50K records)
3. **Triangle calculations** - Nested loops for development patterns

**Optimization Strategies** (for production scale):
- Implement Redis caching for frequent queries
- Use PostgreSQL for datasets >100K records
- Add Celery for async GenAI and batch predictions
- Implement pagination for large result sets
- Consider Dask/Ray for parallel triangle calculations

---

## 🎓 Use Cases

### 1. Actuarial Analysis
- **Reserve Setting**: Automated IBNR estimation using chain-ladder method
- **Loss Development Monitoring**: Track emergence patterns monthly
- **Experience Studies**: Analyze historical loss ratios by segment
- **Rate Adequacy Testing**: Compare actual vs expected loss ratios

### 2. Underwriting Support
- **Risk Assessment**: ML-powered loss ratio predictions for new business
- **COPE Rating Validation**: Explain risk ratings using GenAI
- **Pricing Guidance**: Severity predictions inform premium levels
- **Portfolio Steering**: Identify profitable vs unprofitable segments

### 3. Portfolio Management
- **Segment Profitability**: Multi-dimensional KPI analysis
- **Competitive Positioning**: Benchmark loss ratios by geography/industry
- **Reinsurance Planning**: Ultimate loss projections for treaty negotiations
- **Capital Planning**: Risk-based loss forecasts for solvency analysis

### 4. Decision Support
- **Executive Dashboards**: High-level portfolio metrics with drill-down
- **Natural Language Q&A**: GenAI explanations for non-technical stakeholders
- **Trend Analysis**: AI-powered interpretation of emerging patterns
- **What-If Scenarios**: Test pricing changes using ML predictions

---

## 🔒 Security Notes

**Important Security Considerations:**

- ⚠️ **Never commit `.env` file** with real API keys to version control
- ✅ **Use environment variables** for all secrets (API keys, passwords)
- ⚠️ **In production, implement authentication** (OAuth, JWT, API keys)
- ⚠️ **Restrict CORS origins** - Current setting (`allow_origins=["*"]`) is for development only
- ✅ **Use HTTPS** for all external communications in production
- ⚠️ **Validate input data** - Current implementation trusts all inputs
- ⚠️ **Rate limiting** - Add throttling for GenAI endpoints to prevent abuse
- ✅ **Audit logs** - Implement logging for predictions and data access

**Production Hardening Checklist:**
- [ ] Replace `allow_origins=["*"]` with specific domains in `backend/main.py`
- [ ] Add API authentication (FastAPI dependencies + JWT)
- [ ] Implement rate limiting (e.g., slowapi)
- [ ] Set up HTTPS with valid SSL certificates
- [ ] Add input validation and sanitization
- [ ] Enable audit logging for compliance
- [ ] Restrict Docker network exposure
- [ ] Use secrets management (AWS Secrets Manager, HashiCorp Vault)

---

## 🗺 Vision & Roadmap

See [VISION.md](VISION.md) for strategic goals and future capabilities.

**Near-Term Enhancements** (Next 3-6 months):
- PostgreSQL integration for production-scale data
- User authentication and role-based access control
- Advanced visualizations (D3.js, Recharts)
- Batch prediction API for portfolio-wide scoring
- Scheduled model retraining pipeline

**Long-Term Goals** (6-12+ months):
- Multi-line support (GL, Auto, Workers Comp)
- Real-time streaming data integration
- Advanced ML models (XGBoost, neural networks)
- Cloud deployment guides (AWS, Azure, GCP)
- Mobile-responsive dashboards

---

## 🤝 Contributing

This is a demonstration/educational project. For production use, consider:

**Code Contributions:**
- Follow PEP 8 style guide for Python code
- Add unit tests for new features (maintain 85%+ coverage)
- Update relevant formula documentation (.md files)
- Test in Docker environment before submitting

**Documentation Improvements:**
- Fix typos, clarify instructions
- Add examples and use cases
- Improve API documentation
- Translate to other languages

**Bug Reports:**
- Include system info (OS, Docker version)
- Provide reproduction steps
- Share relevant logs (backend/frontend)
- Check existing issues first

**Feature Requests:**
- Describe business use case
- Explain expected behavior
- Consider backward compatibility
- Propose implementation approach

---

## 📞 Contact

**Author**: Suvojit Dutta
**Email**: suvojit.dutta@zensar.com

**Questions?**
- Check [Documentation](#-documentation) first
- Review [Troubleshooting](#-troubleshooting) section
- Open an issue on GitHub

---

## 📄 License

This project is for **demonstration and educational purposes**.

For commercial use, consider:
- Implementing security hardening (see Security Notes)
- Adding production-grade error handling
- Setting up comprehensive monitoring and logging
- Obtaining appropriate software licenses for dependencies
- Consulting with legal counsel for insurance-specific regulations

---

**Built with modern actuarial science, machine learning, and AI** 🚀

*Empowering insurers with transparent, affordable, AI-powered analytics*
