# Actuarial Insights Workbench

A comprehensive actuarial analytics platform for Commercial Property insurance, combining modern ML/AI capabilities with proven actuarial methodologies.

## 🎯 Purpose

This platform demonstrates how actuarial, underwriting, and analytics workflows can be modernized through:
- **Loss Development Analysis** - Track emergence patterns with development triangles
- **Predictive Modeling** - ML-powered loss ratio and severity predictions
- **Segment Analytics** - Deep-dive KPIs across multiple dimensions
- **GenAI Insights** - Natural language explanations using OpenAI GPT-3.5

## ✨ Features

### 1. Loss Development Dashboard
- Cumulative and incremental loss triangles
- Age-to-age development factors
- Ultimate loss projections and IBNR estimation
- Monthly granularity with 36-month development
- Interactive heatmaps and visualizations

### 2. Pricing & Portfolio KPIs
- Segment analysis by Geography, Industry, Policy Size, Risk Rating
- Key metrics: Loss Ratio, Frequency, Severity, Pure Premium
- Frequency vs Severity scatter analysis
- Top/bottom performer identification
- Downloadable reports

### 3. Risk Prediction
- Loss Ratio prediction using LightGBM
- Claim Severity prediction using LightGBM
- Confidence intervals and uncertainty quantification
- Feature importance analysis
- Interactive risk scoring

### 4. GenAI Insights
- Natural language Q&A about portfolio metrics
- Loss ratio explanations with context
- Trend analysis and interpretation
- COPE risk rating explanations
- Powered by OpenAI GPT-3.5-turbo

## 🧱 Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

**Tech Stack:**
- **Frontend**: Streamlit, Plotly, Matplotlib
- **Backend**: FastAPI, Uvicorn
- **ML**: LightGBM, scikit-learn
- **GenAI**: OpenAI GPT-3.5-turbo
- **Data**: Pandas, NumPy
- **Infrastructure**: Docker, Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key
- 8GB RAM minimum
- Ports 8000 and 8501 available

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd actuarial-insights-workbench
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
nano .env
```

Add to `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
BACKEND_HOST=backend
BACKEND_PORT=8000
ENVIRONMENT=development
```

3. **Build and start services**
```bash
docker-compose up --build
```

This will:
- Build the backend and frontend Docker containers
- Start the FastAPI backend on `http://localhost:8000`
- Start the Streamlit frontend on `http://localhost:8501`

4. **Access the application**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### First-Time Setup: Train ML Models

**IMPORTANT**: After starting the services, you must train the ML models for predictions to work. Without trained models, the application will fall back to static rules.

```bash
# Train both Loss Ratio and Severity models
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Restart backend to load the trained models
docker-compose restart backend

# Verify models loaded successfully
docker logs aiw-backend | grep "Loaded"
# Should see: "Loaded Loss Ratio model" and "Loaded Severity model"
```

**What this does:**
- Trains LightGBM models on 1,000 policies and 114 claims
- Creates `backend/models/lr_model.pkl` (Loss Ratio model, ~130 KB)
- Creates `backend/models/severity_model.pkl` (Severity model, ~47 KB)
- Models persist via Docker volume mount

**Model Performance:**
- Loss Ratio Model: MAE 78.81, trained on 800 samples
- Severity Model: MAE $131,291, trained on 86 policies with claims

**Verify it worked:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","data_loaded":true,"model_loaded":true}
```

## 📊 Data

The platform uses synthetic Commercial Property insurance data:
- **1,000 policies** across 3 accident years (2022-2024)
- **100-200 claims** with realistic loss patterns
- **17,000+ exposure records** with monthly granularity

Data is generated using actuarially-sound methods with:
- COPE-based risk ratings (1-10 scale)
- Geographic and industry segmentation
- Realistic severity distributions
- Proper loss development patterns

To regenerate data:
```bash
cd scripts
python generate_data.py
```

## 🛠 Development

### Local Development (without Docker)

1. **Install Python 3.11+**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate data**
```bash
cd scripts
python generate_data.py
cd ..
```

4. **Train models**
```bash
cd scripts
python train_models.py
cd ..
```

5. **Start backend**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

6. **Start frontend** (in new terminal)
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### Project Structure

```
actuarial-insights-workbench/
├── README.md                   # This file
├── VISION.md                   # Project vision
├── ARCHITECTURE.md             # Technical architecture
├── docker-compose.yml          # Docker orchestration
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
│
├── backend/                    # FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # API endpoints
│   ├── services/
│   │   ├── loss_triangle.py    # Loss development logic
│   │   ├── segment_kpis.py     # KPI calculations
│   │   ├── prediction.py       # ML predictions
│   │   └── explain.py          # GenAI explanations
│   ├── models/                 # Trained ML models
│   │   ├── lr_model.pkl
│   │   └── severity_model.pkl
│   └── tests/                  # Unit tests
│
├── frontend/                   # Streamlit UI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                  # Landing page
│   └── pages/
│       ├── 1_Loss_Development.py
│       ├── 2_Pricing_KPIs.py
│       ├── 3_Risk_Prediction.py
│       └── 4_GenAI_Insights.py
│
├── data/                       # Generated datasets
│   ├── policies.csv
│   ├── claims.csv
│   └── exposure.csv
│
├── scripts/                    # Utility scripts
│   ├── generate_data.py        # Data generation
│   └── train_models.py         # Model training
│
└── notebooks/                  # Jupyter notebooks
    ├── 1_data_exploration.ipynb
    ├── 2_loss_triangle_analysis.ipynb
    └── 3_model_development.ipynb
```

## 📖 API Documentation

### Endpoints

**Predictions:**
- `POST /predict/loss_ratio` - Predict expected loss ratio
- `POST /predict/severity` - Predict claim severity
- `POST /predict/both` - Both predictions

**Analytics:**
- `GET /segment_insights` - Segment-level KPIs
- `GET /loss_triangle` - Loss development triangle

**GenAI:**
- `POST /explain` - Generate natural language explanations

**Utility:**
- `GET /health` - Health check
- `GET /data_summary` - Data summary statistics
- `GET /feature_importance/{model_type}` - Feature importance

Full API documentation available at: http://localhost:8000/docs

## 🧪 Testing

Run unit tests:
```bash
# Inside Docker
docker exec aiw-backend pytest tests/ -v --cov=services

# Or locally
cd backend
pytest tests/ -v --cov=services
```

## 🐛 Troubleshooting

### Models Not Loading / Falling Back to Static Rules

**Symptom**: Predictions always return fixed values (Loss Ratio: 65%, Severity: policy-size based)

**Solution**:
```bash
# Train the models
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Restart backend
docker-compose restart backend

# Verify models loaded
docker logs aiw-backend | grep "Loaded"
```

**Root Cause**: ML models must be trained after first setup. The training script was fixed to handle a column merge conflict that previously prevented training.

### Backend Connection Errors

**Symptom**: Frontend shows "Connection refused" or "Cannot connect to backend"

**Solution**:
```bash
# Check backend is running
docker ps | grep aiw-backend

# Check backend logs for errors
docker logs aiw-backend --tail 50

# Restart backend
docker-compose restart backend
```

### Port Already in Use

**Symptom**: "Address already in use" error on ports 8000 or 8501

**Solution**:
```bash
# Find process using the port
lsof -i :8000  # or :8501

# Stop the process or use different ports in docker-compose.yml
```

### GenAI Features Not Working

**Symptom**: GenAI Insights tab shows errors or timeouts

**Solution**:
- Verify `OPENAI_API_KEY` is set in `.env` file
- Check API key is valid at https://platform.openai.com/api-keys
- Ensure you have API credits available
- Note: GenAI has 30s timeout (normal for API calls)

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables for all secrets
- In production, implement proper authentication
- Restrict CORS origins in production
- Use HTTPS for all external communications

## 📈 Performance

- Backend handles ~100 requests/second
- Frontend supports multiple concurrent users
- Models load in <1 second
- Typical prediction latency: <100ms
- GenAI responses: 2-5 seconds

## 🎓 Use Cases

1. **Actuarial Analysis** - Reserve setting, loss development monitoring
2. **Underwriting** - Risk assessment, pricing guidance
3. **Portfolio Management** - Segment performance, profitability analysis
4. **Decision Support** - AI-powered insights and recommendations

## 🗺 Vision

See [VISION.md](VISION.md) for strategic goals and future capabilities.

## 🤝 Contributing

This is a demonstration/educational project. For production use, consider:
- Adding user authentication
- Implementing database persistence
- Enhanced error handling
- Comprehensive logging
- Performance optimization
- Security hardening

## 📞 Contact

Created by Suvojit Dutta
Email: suvojit.dutta@zensar.com

## 📄 License

This project is for demonstration and educational purposes.

---

**Built with modern actuarial science, machine learning, and AI**
