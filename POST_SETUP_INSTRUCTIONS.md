# Post-Setup Instructions - IMPORTANT

## ⚠️ Required Steps After Initial Docker Launch

After running `docker-compose up --build` for the first time, you **must** complete these additional steps for full functionality:

---

## Step 1: Add OpenAI API Key ✅ REQUIRED

The GenAI features will not work without an OpenAI API key.

```bash
# Edit the .env file
nano .env  # or use your preferred editor

# Add your API key:
OPENAI_API_KEY=sk-your-actual-api-key-here
```

After adding the key:
```bash
docker-compose restart frontend
docker-compose restart backend
```

**Without this:**
- ❌ GenAI Insights page will show errors
- ❌ `/explain` API endpoint will return 503 errors

**With this:**
- ✅ GenAI Insights page fully functional
- ✅ Natural language Q&A works
- ✅ AI-powered explanations work

---

## Step 2: Train ML Models ✅ REQUIRED for ML Features

The `backend/models/` folder is **empty** by design. You must train the models.

### Why Models Aren't Included:

1. **Size**: Model files can be large (several MB)
2. **Customization**: You may want to retrain with different parameters
3. **Data Dependency**: Models are trained on generated data
4. **Flexibility**: Easy to retrain as data changes

### How to Train Models:

```bash
# Option A: Using Docker (Recommended)
docker exec -it aiw-backend bash
cd /app/..
python scripts/train_models.py
exit
docker-compose restart backend

# Option B: Local Python (if running locally)
cd scripts
python train_models.py
cd ..
# Restart backend manually
```

### Training Output:

You should see output like:
```
============================================================
ACTUARIAL INSIGHTS WORKBENCH - MODEL TRAINING
============================================================

Loading data...
Loaded 1000 policies, 114 claims, 17865 exposure records

============================================================
TRAINING LOSS RATIO MODEL
============================================================

Training samples: 800
Test samples: 200

Training LightGBM model...

------------------------------------------------------------
MODEL PERFORMANCE
------------------------------------------------------------

Training Set:
  MAE:  12.45
  RMSE: 15.32
  R²:   0.7234

Test Set:
  MAE:  13.67
  RMSE: 16.89
  R²:   0.6891

Feature Importance:
  RiskRating          : 0.4523
  Geography           : 0.2134
  Industry            : 0.1876
  PolicySize          : 0.0987
  ExposureUnits       : 0.0321
  AnnualPremium       : 0.0159

============================================================
TRAINING SEVERITY MODEL
============================================================

[Similar output for severity model...]

✅ Loss Ratio model saved to ../backend/models/lr_model.pkl
✅ Severity model saved to ../backend/models/severity_model.pkl

============================================================
MODEL TRAINING COMPLETE!
============================================================
```

### Verify Models Were Created:

```bash
# Check models exist
docker exec aiw-backend ls -la /app/models/

# Should show:
# lr_model.pkl
# severity_model.pkl
```

### What Happens If You Skip This Step:

**Before Training Models:**
- ⚠️ Predictions use **rule-based fallback logic**
- ⚠️ Message shown: "Model not loaded - using default estimate"
- ⚠️ Less accurate predictions
- ✅ App still runs and shows UI

**After Training Models:**
- ✅ Predictions use **trained LightGBM models**
- ✅ Accurate ML-based predictions
- ✅ Confidence intervals based on model performance
- ✅ Feature importance available

---

## Step 3: Verify Everything Works

### Check Backend Health:
```bash
curl http://localhost:8003/health
```

Expected response:
```json
{
  "status": "healthy",
  "data_loaded": true,
  "model_loaded": true  // Should be true after Step 2
}
```

### Check Frontend:
1. Go to http://localhost:8502
2. Navigate to "Risk Prediction" page
3. Enter any policy details
4. Click "Predict Both"
5. Should see actual predictions (not "Model not loaded" message)

### Check GenAI:
1. Go to "GenAI Insights" page
2. Type a question: "What is driving portfolio performance?"
3. Click "Get Answer"
4. Should see AI-generated response (not API key error)

---

## Common Issues & Solutions

### Issue: "OpenAI API key not configured"

**Solution:**
```bash
# 1. Check .env file exists and has the key
cat .env | grep OPENAI_API_KEY

# 2. Restart services
docker-compose restart
```

### Issue: "Model not loaded" message in predictions

**Solution:**
```bash
# 1. Check if models exist
docker exec aiw-backend ls -la /app/models/

# 2. If empty, train models (see Step 2 above)

# 3. Restart backend
docker-compose restart backend
```

### Issue: Training script fails with "ModuleNotFoundError"

**Solution:**
```bash
# Install dependencies inside container
docker exec -it aiw-backend bash
pip install -r requirements.txt
cd /app/..
python scripts/train_models.py
exit
```

### Issue: "Cannot connect to backend API"

**Solution:**
```bash
# 1. Check backend is running
docker ps | grep aiw-backend

# 2. Check backend logs
docker logs aiw-backend

# 3. Restart backend
docker-compose restart backend
```

---

## Optional: Regenerate Data

If you want different data:

```bash
docker exec -it aiw-backend bash
cd /app/..
python scripts/generate_data.py
# This will regenerate all data files

# Then retrain models
python scripts/train_models.py
exit

# Restart backend
docker-compose restart backend
```

---

## Complete Setup Checklist

Use this checklist to ensure everything is configured:

- [ ] Docker containers running (`docker ps`)
- [ ] `.env` file created with OpenAI API key
- [ ] Services restarted after adding API key
- [ ] ML models trained (`backend/models/*.pkl` exist)
- [ ] Backend restarted after model training
- [ ] Health check passes (model_loaded: true)
- [ ] Frontend accessible at http://localhost:8502
- [ ] Backend accessible at http://localhost:8003
- [ ] API docs accessible at http://localhost:8003/docs
- [ ] GenAI Insights page works (no API errors)
- [ ] Risk Prediction page shows ML predictions (not fallback)
- [ ] All 4 dashboard pages load without errors

---

## Time Estimates

- **Step 1 (API Key):** 2 minutes
- **Step 2 (Model Training):** 3-5 minutes
- **Step 3 (Verification):** 2 minutes

**Total:** ~10 minutes for complete setup

---

## Need Help?

See the following documentation:
- **SETUP_GUIDE.md** - Detailed troubleshooting
- **QUICKSTART.md** - Quick reference
- **README.md** - Comprehensive documentation

---

**Once you complete these steps, your Actuarial Insights Workbench will be fully functional with all ML and GenAI features enabled!** ✅
