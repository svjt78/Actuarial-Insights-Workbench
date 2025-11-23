# Actuarial Insights Workbench - Quick Start

## 🚀 Get Started in 3 Minutes

### Step 1: Configure Environment
```bash
cp .env.example .env
echo "OPENAI_API_KEY=your-key-here" >> .env
```

### Step 2: Launch
```bash
docker-compose up --build
```

### Step 3: Train Models
```bash
# Open new terminal while app is running
docker exec -it aiw-backend bash -c "cd .. && python scripts/train_models.py"
docker-compose restart backend
```

### Step 4: Access Application
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## 📊 What Can You Do?

### 1. Loss Development Dashboard
- View loss triangles (cumulative/incremental)
- Calculate development factors
- Project ultimate losses and IBNR

### 2. Pricing & KPIs
- Analyze by Geography, Industry, Size, Risk Rating
- View Loss Ratio, Frequency, Severity metrics
- Identify top and bottom performers

### 3. Risk Prediction
- Predict Loss Ratio using ML
- Predict Claim Severity using ML
- Get confidence intervals

### 4. GenAI Insights
- Ask questions in natural language
- Get explanations for trends
- Understand risk ratings

---

## 🎯 Sample Workflows

### Actuarial Analysis
1. Go to "Loss Development"
2. Select "IncurredAmount" and "cumulative"
3. Click "Load Triangle Data"
4. Review IBNR projections

### Underwriting Decision
1. Go to "Risk Prediction"
2. Enter policy characteristics
3. Click "Predict Both"
4. Review predicted loss ratio and severity

### Portfolio Review
1. Go to "Pricing & KPIs"
2. Select segment dimension (e.g., "Geography")
3. Click "Load KPI Data"
4. Analyze performance by segment

### AI Insights
1. Go to "GenAI Insights"
2. Ask: "Which segments should I focus on?"
3. Get AI-powered recommendations

---

## 🔧 Common Commands

### View Logs
```bash
docker logs aiw-backend
docker logs aiw-frontend
```

### Restart Services
```bash
docker-compose restart
```

### Stop Services
```bash
docker-compose down
```

### Rebuild from Scratch
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

### Run Tests
```bash
docker exec aiw-backend pytest tests/ -v
```

### Regenerate Data
```bash
docker exec aiw-backend bash -c "cd .. && python scripts/generate_data.py"
docker-compose restart backend
```

---

## 📚 Key Files

- **README.md** - Comprehensive documentation
- **SETUP_GUIDE.md** - Detailed setup instructions
- **PROJECT_SUMMARY.md** - Complete project overview
- **ARCHITECTURE.md** - Technical architecture
- **VISION.md** - Strategic vision

---

## 💡 Tips

- **First time**: Allow 3-5 minutes for Docker build
- **OpenAI costs**: ~$0.01 per GenAI query (GPT-3.5-turbo)
- **Performance**: Increase Docker RAM to 4GB+ for best experience
- **Development**: Code changes auto-reload in both services

---

## ⚠️ Troubleshooting

**Backend won't start**
→ Check logs: `docker logs aiw-backend`

**Frontend can't connect to backend**
→ Verify backend is running: `docker ps`

**Model predictions not working**
→ Train models (see Step 3 above)

**GenAI not responding**
→ Check OpenAI API key in `.env`

---

## 📞 Need Help?

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

---

**Happy Analyzing!** 📊🎯🚀
