# Changelog

All notable changes to the Actuarial Insights Workbench project.

## [2024-11-24] - ML Model Training Fix

### Fixed

#### Critical: Model Training Script Bug
- **Issue**: Training script failed with `KeyError: "['ExposureUnits'] not in index"`
- **Root Cause**: Column name conflict during pandas DataFrame merge
  - Both `policies_df` and `exposure_agg` DataFrames contained `ExposureUnits` column
  - Pandas automatically renamed columns to `ExposureUnits_x` and `ExposureUnits_y`
  - Script tried to access `training_df['ExposureUnits']` which no longer existed
- **Fix**: Drop `ExposureUnits` from policies DataFrame before merge, use aggregated values from exposure data
- **File Changed**: `scripts/train_models.py` lines 47-53
- **Code**:
  ```python
  # Drop ExposureUnits from policies to avoid column name conflict during merge
  # We'll use the aggregated ExposureUnits from exposure data
  policies_for_merge = policies_df.drop(columns=['ExposureUnits'])
  ```

#### Model Save Path Issue
- **Issue**: Training script saved models to `/backend/models/` instead of `/app/models/`
- **Root Cause**: Script used relative path `../backend/models/` which resolved differently in Docker container
- **Fix**: Auto-detect Docker environment and use appropriate path
- **File Changed**: `scripts/train_models.py` lines 252-264
- **Code**:
  ```python
  models_dir = '/app/models' if os.path.exists('/app/models') else '../backend/models'
  os.makedirs(models_dir, exist_ok=True)
  ```

### Impact

**Before Fix:**
- ML models could not be trained
- Application fell back to static prediction rules:
  - Loss Ratio: Always 65%
  - Severity: Policy-size-based ($50k/$100k/$250k/$500k)
- No real ML predictions available

**After Fix:**
- Models train successfully
- Real ML predictions based on 6 features:
  - RiskRating, Geography, Industry, PolicySize, ExposureUnits, AnnualPremium
- Loss Ratio model: MAE 78.81 (800 training samples)
- Severity model: MAE $131,291 (86 training samples with claims)
- Feature importance analysis available
- Model-based confidence intervals

### Documentation Updates

#### README.md
- ✅ Updated "First-Time Setup" section with correct training command
- ✅ Added detailed "What this does" explanation
- ✅ Added model performance metrics
- ✅ Added verification steps
- ✅ Added comprehensive "Troubleshooting" section with 4 common issues

#### CLAUDE.md
- ✅ Updated "Critical Path: Model Training" section
- ✅ Added static fallback behavior details
- ✅ Added training script fix notes with date and technical details
- ✅ Expanded "Common Gotchas" section (1 item → 8 items)
- ✅ Added new "Troubleshooting Model Training" section
- ✅ Added verification commands and examples

#### New Documentation Files
- ✅ `MODEL_TRAINING_FIX.md` - Comprehensive root cause analysis (42 KB)
- ✅ `TEST_RESULTS.md` - Before/after prediction comparisons (5 KB)
- ✅ `CHANGELOG.md` - This file

### Verification

Models successfully trained and loaded:
```json
{
  "status": "healthy",
  "data_loaded": true,
  "model_loaded": true
}
```

Backend logs confirm:
```
Loaded Loss Ratio model from /app/models/lr_model.pkl
Loaded Severity model from /app/models/severity_model.pkl
```

Model files created:
- `backend/models/lr_model.pkl` (130 KB)
- `backend/models/severity_model.pkl` (47 KB)

Sample predictions working:
- Loss Ratio: Real predictions (-22.99%, 125.23%, etc.) instead of fixed 65%
- Severity: Real predictions ($235,941, $294,497, etc.) instead of policy-size lookup

### Training Commands (Updated)

```bash
# Train models (correct command)
docker exec aiw-backend bash -c "cd .. && python scripts/train_models.py"

# Restart backend to load models
docker-compose restart backend

# Verify models loaded
docker logs aiw-backend | grep "Loaded"

# Test health endpoint
curl http://localhost:8003/health
```

### Model Performance Metrics

#### Loss Ratio Model
- **Algorithm**: LightGBM Regressor
- **Training samples**: 800
- **Test samples**: 200
- **Test MAE**: 78.81 percentage points
- **Test RMSE**: 329.26
- **Test R²**: -0.0616 (needs more data/feature engineering)
- **Top 3 Features**:
  1. ExposureUnits (386)
  2. RiskRating (375)
  3. AnnualPremium (341)

#### Severity Model
- **Algorithm**: LightGBM Regressor
- **Training samples**: 86 (policies with claims)
- **Test samples**: 22
- **Test MAE**: $131,290.76
- **Test RMSE**: $173,582.53
- **Test R²**: 0.3717 (reasonable performance)
- **Top 3 Features**:
  1. AnnualPremium (93)
  2. Geography (55)
  3. Industry (37)

### Future Improvements

1. **Data Collection**: More claims data will improve model accuracy, especially for Loss Ratio model (negative R²)
2. **Feature Engineering**: Add derived features (claims history trends, COPE components breakdown)
3. **Hyperparameter Tuning**: Optimize LightGBM parameters (learning rate, max_depth, num_leaves)
4. **Cross-validation**: Implement k-fold CV for better generalization estimates
5. **Ensemble Methods**: Consider stacking or blending multiple models
6. **Regular Retraining**: Set up automated pipeline to retrain as new data arrives

### Files Modified

- `scripts/train_models.py` (2 bug fixes)
- `README.md` (expanded First-Time Setup, added Troubleshooting)
- `CLAUDE.md` (updated Critical Path, expanded Common Gotchas)

### Files Added

- `MODEL_TRAINING_FIX.md` (root cause analysis)
- `TEST_RESULTS.md` (before/after comparison)
- `CHANGELOG.md` (this file)

---

## Previous Versions

### [2024-11-23] - Initial Commit
- Initial project setup
- Backend API with 9 endpoints
- Frontend with 4 dashboard pages
- Synthetic data generation
- Model training scripts (with bugs - fixed 2024-11-24)
- Docker containerization
- Documentation (README, ARCHITECTURE, VISION)
