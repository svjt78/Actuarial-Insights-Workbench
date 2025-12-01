# Actuarial Insights Workbench - Setup Guide

## Quick Start (5 Minutes)

### Step 1: Environment Setup

1. **Create `.env` file:**
```bash
cp .env.example .env
```

2. **Edit `.env` and add your OpenAI API key:**
```env
OPENAI_API_KEY=sk-your-api-key-here
BACKEND_HOST=backend
BACKEND_PORT=8003
ENVIRONMENT=development
```

### Step 2: Launch Application

```bash
docker-compose up --build
```

Wait for both services to start (approximately 2-3 minutes).

### Step 3: Access Application

- **Frontend (Streamlit)**: http://localhost:8502
- **Backend API**: http://localhost:8003
- **API Documentation**: http://localhost:8003/docs

### Step 4: Train ML Models

Open a new terminal and run:

```bash
# Enter backend container
docker exec -it aiw-backend bash

# Navigate to scripts directory and train models
cd ..
python scripts/train_models.py

# Exit container
exit

# Restart backend to load models
docker-compose restart backend
```

### Step 5: Verify Setup

1. Go to http://localhost:8502
2. Navigate to "Risk Prediction" page
3. Click "Predict Both" to test ML models
4. Navigate to "GenAI Insights" and ask a question

---

## Detailed Setup Options

### Option 1: Docker (Recommended)

**Advantages:**
- Consistent environment
- No local Python setup needed
- Easy deployment

**Requirements:**
- Docker Desktop installed
- 8GB RAM
- 5GB free disk space

### Option 2: Local Python

**Advantages:**
- Faster iteration during development
- Direct access to code

**Requirements:**
- Python 3.11+
- pip installed

**Steps:**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Generate data:**
```bash
cd scripts
python generate_data.py
cd ..
```

3. **Train models:**
```bash
cd scripts
python train_models.py
cd ..
```

4. **Start backend** (terminal 1):
```bash
cd backend
uvicorn main:app --reload --port 8003
```

5. **Start frontend** (terminal 2):
```bash
cd frontend
streamlit run app.py --server.port 8502
```

---

## Troubleshooting

### Issue: "Cannot connect to backend API"

**Solution:**
- Verify backend is running: `docker ps`
- Check logs: `docker logs aiw-backend`
- Ensure port 8003 is not in use

### Issue: "OpenAI API key not configured"

**Solution:**
- Verify `.env` file exists with valid API key
- Restart containers: `docker-compose restart`

### Issue: "Model not loaded"

**Solution:**
- Train models using Step 4 above
- Verify model files exist:
  ```bash
  docker exec aiw-backend ls -la models/
  ```

### Issue: Port already in use

**Solution:**
- Change ports in `docker-compose.yml`:
  ```yaml
  ports:
    - "8004:8003"  # Backend
    - "8503:8502"  # Frontend
  ```

### Issue: Docker build fails

**Solution:**
- Clear Docker cache:
  ```bash
  docker-compose down
  docker system prune -a
  docker-compose up --build
  ```

---

## Data Information

### Synthetic Data Overview

The platform generates realistic Commercial Property insurance data:

- **Policies**: 1,000 policies
- **Claims**: 100-200 claims
- **Exposure**: 17,000+ monthly records
- **Time Period**: 3 accident years (2022-2024)

### Regenerating Data

```bash
docker exec -it aiw-backend bash
cd ..
python scripts/generate_data.py
exit
docker-compose restart backend
```

---

## Testing

### Run Unit Tests

```bash
docker exec -it aiw-backend bash
cd /app
pytest tests/ -v --cov=services
```

### Expected Output

```
tests/test_loss_triangle.py ........... PASSED
tests/test_segment_kpis.py ............ PASSED
tests/test_prediction.py .............. PASSED

Coverage: 85%
```

---

## Performance Optimization

### For Better Performance:

1. **Increase Docker resources:**
   - Docker Desktop → Settings → Resources
   - Allocate 4GB+ RAM

2. **Use smaller data:**
   - Edit `scripts/generate_data.py`
   - Reduce `NUM_POLICIES` to 500

3. **Disable GenAI:**
   - Use stub responses instead of OpenAI calls
   - Comment out API calls in `backend/services/explain.py`

---

## Development Workflow

### Making Code Changes

1. **Backend changes:**
   - Edit files in `backend/`
   - Changes auto-reload (thanks to `--reload` flag)

2. **Frontend changes:**
   - Edit files in `frontend/`
   - Streamlit auto-reloads on file save

3. **Service changes:**
   - Edit files in `backend/services/`
   - Restart backend: `docker-compose restart backend`

### Adding New Features

1. Create new service module in `backend/services/`
2. Add endpoint in `backend/main.py`
3. Create new page in `frontend/pages/`
4. Update README and documentation

---

## Production Deployment

### Security Checklist:

- [ ] Change default ports
- [ ] Add authentication/authorization
- [ ] Use HTTPS
- [ ] Restrict CORS origins
- [ ] Enable rate limiting
- [ ] Add logging and monitoring
- [ ] Use secrets management (not .env files)
- [ ] Implement backup strategy

### Recommended Stack:

- **Hosting**: AWS ECS, Google Cloud Run, or Azure Container Apps
- **Database**: PostgreSQL for data persistence
- **Caching**: Redis for improved performance
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or Cloud Logging

---

## Getting Help

### Resources:

- **README**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Vision**: [VISION.md](VISION.md)
- **API Docs**: http://localhost:8003/docs

### Common Questions:

**Q: How do I add more data?**
A: Edit `scripts/generate_data.py` and increase `NUM_POLICIES`.

**Q: Can I use a different LLM provider?**
A: Yes, modify `backend/services/explain.py` to use your preferred provider.

**Q: How do I deploy to production?**
A: See "Production Deployment" section above.

**Q: Can I use real insurance data?**
A: Yes, but ensure data privacy compliance. Modify data loading in `backend/main.py`.

---

## Next Steps

After completing setup:

1. ✅ Explore the Loss Development Dashboard
2. ✅ Review Pricing & KPIs by segment
3. ✅ Test Risk Predictions with different inputs
4. ✅ Try GenAI Insights Q&A feature
5. ✅ Review API documentation at /docs
6. ✅ Run unit tests to verify everything works
7. ✅ Customize for your specific use case

---

**Happy Analyzing! 📊**
