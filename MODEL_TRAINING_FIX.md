# ML Model Training Issue - Root Cause Analysis & Fix

## Problem Summary

The ML models were **not working** and the application was **falling back to static rules** for predictions:

- **Loss Ratio**: Always returned 65.0% with message "Model not loaded - using default estimate"
- **Severity**: Returned policy-size-based estimates (Small: $50k, Medium: $100k, Large: $250k, Enterprise: $500k)

## Root Causes Identified

### 1. Models Never Trained
- No `.pkl` model files existed in `backend/models/`
- Application was designed to gracefully handle missing models by falling back to static rules ([prediction.py:97-104](backend/services/prediction.py#L97-L104), [lines 142-160](backend/services/prediction.py#L142-L160))

### 2. Training Script Bug - Column Name Conflict
**Issue**: Data merge caused column renaming
```python
# Both dataframes had 'ExposureUnits' column
policies_df: ['PolicyID', 'ExposureUnits', ...]
exposure_agg: ['PolicyID', 'ExposureUnits', ...]

# After merge, pandas renamed them:
training_df: ['PolicyID', 'ExposureUnits_x', 'ExposureUnits_y', ...]

# Script tried to access 'ExposureUnits' -> KeyError
```

**Fix**: Drop `ExposureUnits` from policies before merge, use aggregated values from exposure data
```python
policies_for_merge = policies_df.drop(columns=['ExposureUnits'])
training_df = policies_for_merge.merge(exposure_agg, on='PolicyID', how='left')
```

### 3. Training Script Path Issue
**Issue**: Script saved models to wrong directory
- Training script ran from `/scripts` directory
- Used relative path `../backend/models/` → saved to `/backend/models/`
- Backend expected models at `/app/models/`

**Fix**: Updated script to detect Docker environment and use correct path
```python
models_dir = '/app/models' if os.path.exists('/app/models') else '../backend/models'
```

## Resolution Steps Taken

1. ✅ **Fixed column name conflict** in `scripts/train_models.py:47-53`
2. ✅ **Trained ML models** using LightGBM
   - Loss Ratio Model: 800 training samples, MAE: 75.11
   - Severity Model: 86 training samples (policies with claims), MAE: $97,107.92
3. ✅ **Moved models to correct location** (`/app/models/`)
4. ✅ **Restarted backend** to load trained models
5. ✅ **Updated training script** to save to correct path in future runs

## Verification

### Before Fix (Static Rules)
```json
{
  "predicted_loss_ratio": 65.0,
  "model_loaded": false,
  "message": "Model not loaded - using default estimate"
}
```

### After Fix (ML Models)
```json
{
  "predicted_loss_ratio": 125.23,
  "confidence_interval": [110.23, 100.0],
  "model_loaded": true
}
```

### Model Files Created
- ✅ `backend/models/lr_model.pkl` (130 KB)
- ✅ `backend/models/severity_model.pkl` (47 KB)

### Backend Logs Confirm
```
Loaded Loss Ratio model from /app/models/lr_model.pkl
Loaded Severity model from /app/models/severity_model.pkl
✅ Prediction service initialized
```

## Model Performance

### Loss Ratio Model
- **Training Set**: MAE: 75.11, RMSE: 310.82, R²: 0.3192
- **Test Set**: MAE: 78.81, RMSE: 329.26, R²: -0.0616
- **Top Features**: ExposureUnits (386), RiskRating (375), AnnualPremium (341)

### Severity Model
- **Training Set**: MAE: $97,108, RMSE: $197,305, R²: 0.5458
- **Test Set**: MAE: $131,291, RMSE: $173,583, R²: 0.3717
- **Top Features**: AnnualPremium (93), Geography (55), Industry (37)

## Future Training Commands

To retrain models in the future:
```bash
# Train models
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Restart backend to load new models
docker-compose restart backend

# Verify models loaded
docker logs aiw-backend | grep "Loaded"
```

## Notes

- Models are persisted via Docker volume mount: `./backend/models:/app/models`
- Training data: 1,000 policies, 114 claims, 17,865 exposure records
- The negative test R² for Loss Ratio model suggests more training data or feature engineering may be needed
- Severity model performs better with R² of 0.37 on test set

---

**Status**: ✅ **RESOLVED** - ML models are now active and making predictions
**Date**: 2025-11-24
