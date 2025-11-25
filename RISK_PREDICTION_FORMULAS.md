# Risk Prediction Tab - Formula Reference Guide

**Version**: 1.0
**Last Updated**: November 23, 2024
**Purpose**: Complete mathematical reference for all formulas and calculations used in the Risk Prediction Dashboard

---

## Table of Contents

1. [Feature Encoding](#1-feature-encoding)
2. [Loss Ratio Prediction](#2-loss-ratio-prediction)
3. [Severity Prediction](#3-severity-prediction)
4. [Confidence Interval (Loss Ratio)](#4-confidence-interval-loss-ratio)
5. [Confidence Interval (Severity)](#5-confidence-interval-severity)
6. [Expected Loss](#6-expected-loss)
7. [Expected Profit](#7-expected-profit)
8. [Profit Margin](#8-profit-margin)
9. [Composite Risk Score](#9-composite-risk-score)
10. [Prediction Uncertainty](#10-prediction-uncertainty)
11. [Default Prediction (Loss Ratio)](#11-default-prediction-loss-ratio)
12. [Default Prediction (Severity)](#12-default-prediction-severity)
13. [Feature Importance](#13-feature-importance)
14. [ML Model Architecture Overview](#14-ml-model-architecture-overview)

---

## 1. Feature Encoding

### Purpose
Transform categorical and numerical input features into a format suitable for machine learning model predictions.

### Categorical Variable Encoding

**Geography Encoding** (Label Encoding):
```
Geography → Numeric Code
─────────────────────────
Northeast   →   0
Southeast   →   1
Midwest     →   2
Southwest   →   3
West        →   4
Northwest   →   5
```

**Industry Encoding** (Label Encoding):
```
Industry        → Numeric Code
─────────────────────────────
Manufacturing   →   0
Retail          →   1
Office          →   2
Warehouse       →   3
Healthcare      →   4
Education       →   5
Hospitality     →   6
Technology      →   7
```

**Policy Size Encoding** (Ordinal Encoding):
```
Policy Size   → Numeric Code
───────────────────────────
Small         →   0
Medium        →   1
Large         →   2
Enterprise    →   3
```

### Code Reference
[backend/services/prediction.py:61-85](backend/services/prediction.py#L61-L85)

### Example Encoding

**Input Data**:
```
Geography: "Northeast"
Industry: "Manufacturing"
Policy Size: "Large"
Risk Rating: 6.5
Exposure Units: 75.0
Annual Premium: $50,000
```

**Encoded Features**:
```
Feature Vector:
  Geography → 0 (Northeast)
  Industry → 0 (Manufacturing)
  PolicySize → 2 (Large)
  RiskRating → 6.5 (unchanged - continuous)
  ExposureUnits → 75.0 (unchanged - continuous)
  AnnualPremium → 50000.0 (unchanged - continuous)

Feature DataFrame:
  [0, 0, 2, 6.5, 75.0, 50000.0]
```

### Numerical Features

**Continuous Features** (No Encoding Required):
```
RiskRating: 1.0 - 10.0 (COPE-based risk score)
ExposureUnits: Building value in $100K units
AnnualPremium: Premium amount in dollars
```

### Feature Vector Construction

**Complete Feature Vector**:
```python
features = {
    'Geography': encoded_geography,        # 0-5
    'Industry': encoded_industry,          # 0-7
    'PolicySize': encoded_policy_size,     # 0-3
    'RiskRating': risk_rating,             # 1.0-10.0
    'ExposureUnits': exposure_units,       # Float
    'AnnualPremium': annual_premium        # Float
}
```

### Business Interpretation

**Label Encoding** (Geography, Industry):
- Categorical variables with no inherent order
- Numeric codes assigned for model processing
- Tree-based models (LightGBM) can handle label encoding effectively
- Order doesn't imply ranking (Northeast isn't "less" than West)

**Ordinal Encoding** (Policy Size):
- Categorical variable with natural order
- Small < Medium < Large < Enterprise
- Numeric codes reflect relative size ordering

**Standardization Note**:
- Numerical features NOT standardized for tree-based models
- LightGBM is scale-invariant
- Original scales preserved for interpretability

---

## 2. Loss Ratio Prediction

### Purpose
Predict the expected loss ratio for a policy based on its risk characteristics using a trained machine learning model.

### Formula (ML Model)

**Prediction Function**:
```
Predicted Loss Ratio = f(X)

Where:
  f = Trained LightGBM model
  X = Feature vector [Geography, Industry, PolicySize, RiskRating, ExposureUnits, AnnualPremium]
```

**Model Type**: LightGBM Gradient Boosting Regressor

### Code Reference
[backend/services/prediction.py:87-131](backend/services/prediction.py#L87-L131)
[frontend/pages/3_Risk_Prediction.py:108-122](frontend/pages/3_Risk_Prediction.py#L108-L122)

### Example Prediction

**Input Features**:
```
Geography: Northeast (encoded as 0)
Industry: Manufacturing (encoded as 0)
Policy Size: Large (encoded as 2)
Risk Rating: 6.5
Exposure Units: 75.0
Annual Premium: $50,000
```

**Model Prediction**:
```
Feature Vector X = [0, 0, 2, 6.5, 75.0, 50000.0]

Predicted Loss Ratio = LightGBM_Model.predict(X)
                     = 68.5%
```

### LightGBM Model Architecture

**Model Components**:
```
Input Layer: 6 features
  ↓
Decision Tree Ensemble (100-500 trees)
  • Gradient boosting framework
  • Leaf-wise tree growth
  • Feature-based splits
  ↓
Output: Predicted Loss Ratio (%)
```

**Training Objective**:
```
Minimize: Mean Squared Error (MSE)

MSE = (1/n) × Σ(y_actual - y_predicted)²

Where:
  n = number of training samples
  y_actual = historical loss ratio
  y_predicted = model prediction
```

### Interpretation

**Predicted Loss Ratio of 68.5%**:
- For every $1.00 of premium, expect $0.685 in losses
- Slightly above typical 65% target
- Indicates moderate risk
- May require pricing adjustment or enhanced underwriting

### Prediction Ranges

**Typical Output Ranges**:
```
Loss Ratio Range    Risk Level       Action
───────────────────────────────────────────────
0% - 50%           Very Low         Verify/investigate
50% - 60%          Low              Competitive pricing
60% - 70%          Moderate         Standard pricing
70% - 85%          Elevated         Higher premium needed
85% - 100%         High             Decline or major rate increase
> 100%             Very High        Decline
```

### Model Confidence

**When Model Not Loaded**:
```
Default Prediction = 65.0% (industry average)
Confidence Interval = [50.0%, 80.0%]
Message: "Model not loaded - using default estimate"
```

### Business Applications

1. **Underwriting Decision**:
   ```
   If Predicted LR < 70%: Approve at quoted premium
   If 70% ≤ Predicted LR < 85%: Request higher premium
   If Predicted LR ≥ 85%: Decline or refer to senior underwriter
   ```

2. **Pricing Adjustment**:
   ```
   Current Premium: $50,000
   Predicted LR: 68.5%
   Target LR: 65%

   Adjusted Premium = $50,000 × (68.5% / 65%)
                    = $50,000 × 1.0538
                    = $52,690
   ```

3. **Risk Selection**:
   - Rank policies by predicted loss ratio
   - Focus on policies with LR < 65%
   - Avoid or reprice policies with LR > 75%

---

## 3. Severity Prediction

### Purpose
Predict the expected average claim amount (severity) if a loss occurs, based on policy characteristics.

### Formula (ML Model)

**Prediction Function**:
```
Predicted Severity = g(X)

Where:
  g = Trained LightGBM model
  X = Feature vector [Geography, Industry, PolicySize, RiskRating, ExposureUnits, AnnualPremium]
```

**Model Type**: LightGBM Gradient Boosting Regressor

### Code Reference
[backend/services/prediction.py:132-186](backend/services/prediction.py#L132-L186)
[frontend/pages/3_Risk_Prediction.py:126-141](frontend/pages/3_Risk_Prediction.py#L126-L141)

### Example Prediction

**Input Features**:
```
Same as loss ratio example:
  Geography: Northeast
  Industry: Manufacturing
  Policy Size: Large
  Risk Rating: 6.5
  Exposure Units: 75.0
  Annual Premium: $50,000
```

**Model Prediction**:
```
Feature Vector X = [0, 0, 2, 6.5, 75.0, 50000.0]

Predicted Severity = LightGBM_Model.predict(X)
                   = $125,000
```

### Interpretation

**Predicted Severity of $125,000**:
- If a claim occurs, expect average cost of $125,000
- Reflects building value, risk quality, and industry hazards
- Used for reserve setting and pricing adequacy
- Influences deductible recommendations

### Severity by Risk Factors

**Typical Severity Drivers**:

**By Policy Size**:
```
Policy Size    Typical Severity Range
──────────────────────────────────────
Small         $20,000 - $75,000
Medium        $50,000 - $150,000
Large         $100,000 - $300,000
Enterprise    $200,000 - $750,000
```

**By Industry**:
```
Industry          Typical Severity
────────────────────────────────────
Office            $30,000 - $80,000
Retail            $40,000 - $120,000
Warehouse         $60,000 - $180,000
Manufacturing     $80,000 - $250,000
Healthcare        $100,000 - $300,000
Hospitality       $90,000 - $275,000
```

**By Risk Rating**:
```
Risk Rating    Severity Multiplier
─────────────────────────────────
1-3 (Low)         0.7x - 0.9x
4-6 (Medium)      0.9x - 1.1x
7-10 (High)       1.1x - 1.5x
```

### Business Applications

1. **Reserve Setting**:
   ```
   Expected Claim Count = Premium × Expected Frequency
   Expected Severity = $125,000
   Total Reserve = Claim Count × Severity
   ```

2. **Pricing Verification**:
   ```
   Pure Premium = Frequency × Severity / 100

   If Frequency = 2.0 per 100 units:
   Pure Premium = (2.0 × $125,000) / 100
                = $2,500 per exposure unit
   ```

3. **Deductible Recommendation**:
   ```
   Predicted Severity: $125,000

   Recommended Deductible Options:
   - $5,000 (4% of severity)
   - $10,000 (8% of severity)
   - $25,000 (20% of severity)
   ```

4. **Reinsurance Attachment**:
   ```
   If Predicted Severity = $125,000
   Consider excess of loss reinsurance:
   Attachment Point = $250,000 (2x predicted severity)
   ```

---

## 4. Confidence Interval (Loss Ratio)

### Purpose
Provide a range of plausible values for the predicted loss ratio, reflecting prediction uncertainty.

### Formula

**95% Confidence Interval**:
```
Lower Bound = max(0, Predicted LR - 15)
Upper Bound = min(100, Predicted LR + 15)

Confidence Interval = [Lower Bound, Upper Bound]
```

**Note**: This is a simplified approach. Production models should use proper statistical confidence intervals.

### Code Reference
[backend/services/prediction.py:113-116](backend/services/prediction.py#L113-L116)
[frontend/pages/3_Risk_Prediction.py:186](frontend/pages/3_Risk_Prediction.py#L186)

### Example Calculation

**Scenario**:
```
Predicted Loss Ratio = 68.5%
```

**Calculation**:
```
Lower Bound = max(0, 68.5 - 15)
            = max(0, 53.5)
            = 53.5%

Upper Bound = min(100, 68.5 + 15)
            = min(100, 83.5)
            = 83.5%

Confidence Interval = [53.5%, 83.5%]
```

### Interpretation

**95% Confidence Interval of [53.5%, 83.5%]**:
- There's a 95% probability the actual loss ratio will fall between 53.5% and 83.5%
- Wide interval indicates higher uncertainty
- Range span = 30 percentage points
- Uncertainty = ±15 percentage points

### Interval Width Analysis

**Narrow Interval** (< 20 percentage points):
```
Example: [60%, 75%]
Indicates:
  • High model confidence
  • Stable risk profile
  • Consistent historical data
  • Mature segment
```

**Medium Interval** (20-40 percentage points):
```
Example: [53.5%, 83.5%]
Indicates:
  • Moderate uncertainty
  • Some variability expected
  • Standard risk assessment
  • Typical for most policies
```

**Wide Interval** (> 40 percentage points):
```
Example: [40%, 90%]
Indicates:
  • High uncertainty
  • Volatile segment
  • Limited historical data
  • High-risk or unusual policy
```

### Business Applications

1. **Underwriting Decision**:
   ```
   Predicted LR = 68.5%
   CI = [53.5%, 83.5%]
   Target LR = 65%

   Decision Logic:
   - Best case (53.5%): Profitable - APPROVE
   - Expected (68.5%): Slightly high - ADJUST PREMIUM
   - Worst case (83.5%): Unprofitable - DECLINE or MAJOR INCREASE

   Action: Request premium increase to account for uncertainty
   ```

2. **Risk Assessment**:
   ```
   If Upper Bound > 100%:
     • Extreme risk
     • Possible total loss scenario
     • Decline or refer to reinsurance

   If Lower Bound < 50%:
     • Potentially profitable
     • Verify for quote accuracy
     • Consider competitive pricing
   ```

3. **Pricing Buffer**:
   ```
   Price for Upper Bound scenario:

   Required Premium = Expected Loss / Target LR
                    = ($50,000 × 83.5%) / 65%
                    = $41,750 / 0.65
                    = $64,231

   vs. Expected Case:
   Required Premium = ($50,000 × 68.5%) / 65%
                    = $52,692

   Safety Buffer = $64,231 - $52,692 = $11,539
   ```

### Statistical Interpretation

**Proper Confidence Intervals** (Production Enhancement):

In a production environment, confidence intervals should be derived from:

1. **Prediction Intervals from Model**:
   ```
   Using quantile regression:
   Lower Bound = Model.predict(X, quantile=0.025)
   Upper Bound = Model.predict(X, quantile=0.975)
   ```

2. **Bootstrap Methods**:
   ```
   1. Resample training data 1000 times
   2. Train model on each sample
   3. Generate 1000 predictions
   4. Calculate 2.5th and 97.5th percentiles
   ```

3. **Bayesian Credible Intervals**:
   ```
   Use Bayesian models to generate posterior distributions
   Extract 95% credible interval from posterior
   ```

---

## 5. Confidence Interval (Severity)

### Purpose
Provide a range of plausible values for the predicted claim severity, reflecting prediction uncertainty.

### Formula

**95% Confidence Interval**:
```
Lower Bound = max(0, Predicted Severity × 0.7)
Upper Bound = Predicted Severity × 1.3

Confidence Interval = [Lower Bound, Upper Bound]
```

**Relative Uncertainty**: ±30% from predicted value

### Code Reference
[backend/services/prediction.py:168-171](backend/services/prediction.py#L168-L171)
[frontend/pages/3_Risk_Prediction.py:211](frontend/pages/3_Risk_Prediction.py#L211)

### Example Calculation

**Scenario**:
```
Predicted Severity = $125,000
```

**Calculation**:
```
Lower Bound = max(0, $125,000 × 0.7)
            = max(0, $87,500)
            = $87,500

Upper Bound = $125,000 × 1.3
            = $162,500

Confidence Interval = [$87,500, $162,500]
```

### Interpretation

**95% Confidence Interval of [$87,500, $162,500]**:
- There's a 95% probability the actual claim severity will fall in this range
- Low estimate: $87,500 (30% below prediction)
- Expected: $125,000 (central prediction)
- High estimate: $162,500 (30% above prediction)
- Range span: $75,000
- Relative uncertainty: ±30%

### Uncertainty Percentage

**Calculation** (as shown in UI):
```
Range Percentage = ((Upper - Lower) / Predicted) × 100%
                 = (($162,500 - $87,500) / $125,000) × 100%
                 = ($75,000 / $125,000) × 100%
                 = 60%

Half-Range Uncertainty = 60% / 2 = ±30%
```

### Code Reference (UI Display)
[frontend/pages/3_Risk_Prediction.py:238-240](frontend/pages/3_Risk_Prediction.py#L238-L240)

### Business Applications

1. **Reserve Range**:
   ```
   Expected Claims = 10
   Severity Range = [$87,500, $162,500]

   Minimum Reserve = 10 × $87,500 = $875,000
   Expected Reserve = 10 × $125,000 = $1,250,000
   Maximum Reserve = 10 × $162,500 = $1,625,000

   Reserve Variability = $750,000 (±30%)
   ```

2. **Policy Limit Adequacy**:
   ```
   Predicted Severity = $125,000
   Upper CI = $162,500

   Recommended Limits:
   - Minimum: $150,000 (covers expected)
   - Preferred: $200,000 (covers 95% CI with buffer)
   - Optimal: $250,000 (2x expected, comfortable margin)
   ```

3. **Deductible Options**:
   ```
   Low Estimate: $87,500
   High Estimate: $162,500

   Deductible Options to Offer:
   - $5,000 (3-6% of severity range)
   - $10,000 (6-11% of severity range)
   - $25,000 (15-29% of severity range)
   - $50,000 (31-57% of severity range)
   ```

4. **Reinsurance Treaty Design**:
   ```
   Expected Severity: $125,000
   95% CI Upper Bound: $162,500

   Excess of Loss Treaty:
   Retention = $200,000 (above CI upper bound)
   Limit = $1,000,000

   Covers catastrophic claims above normal expectations
   ```

### Severity Volatility

**Narrow Interval** (< 40% range):
```
Example: [$100,000, $140,000]
Relative Range = 40%
Uncertainty = ±20%

Indicates:
  • Predictable claim sizes
  • Homogeneous risks
  • Stable building values
  • Standard construction
```

**Medium Interval** (40-80% range):
```
Example: [$87,500, $162,500]
Relative Range = 60%
Uncertainty = ±30%

Indicates:
  • Moderate variability
  • Mixed building types
  • Standard uncertainty
  • Typical commercial property
```

**Wide Interval** (> 80% range):
```
Example: [$50,000, $200,000]
Relative Range = 100%
Uncertainty = ±50%

Indicates:
  • High variability
  • Diverse risk exposures
  • Uncertain valuations
  • Special risks or unique properties
```

---

## 6. Expected Loss

### Purpose
Calculate the expected dollar amount of losses based on the predicted loss ratio and annual premium.

### Formula
```
Expected Loss = Annual Premium × (Predicted Loss Ratio / 100)
```

### Code Reference
[frontend/pages/3_Risk_Prediction.py:254](frontend/pages/3_Risk_Prediction.py#L254)

### Example Calculation

**Scenario**:
```
Annual Premium = $50,000
Predicted Loss Ratio = 68.5%
```

**Calculation**:
```
Expected Loss = $50,000 × (68.5 / 100)
              = $50,000 × 0.685
              = $34,250
```

### Interpretation
- Out of $50,000 in premium, expect to pay $34,250 in losses
- Remaining $15,750 must cover expenses and profit
- If expenses are 30% of premium ($15,000), leaves only $750 profit
- Indicates thin margin or potential underwriting loss

### Expected Loss Range

**Using Confidence Intervals**:
```
Predicted LR: 68.5%
CI: [53.5%, 83.5%]
Premium: $50,000

Best Case Expected Loss = $50,000 × 0.535 = $26,750
Expected Case = $50,000 × 0.685 = $34,250
Worst Case Expected Loss = $50,000 × 0.835 = $41,750

Loss Variability = $41,750 - $26,750 = $15,000
```

### Business Applications

1. **Profitability Assessment**:
   ```
   Premium: $50,000
   Expected Loss: $34,250
   Expected Expenses (30%): $15,000

   Expected Underwriting Profit = $50,000 - $34,250 - $15,000
                                = $750

   Profit Margin = $750 / $50,000 = 1.5% (very thin)
   ```

2. **Reserve Allocation**:
   ```
   Expected Loss = $34,250

   Reserve Components:
   - Initial Case Reserve: $10,000 (29%)
   - IBNR Reserve: $24,250 (71%)
   Total Reserve: $34,250
   ```

3. **Cash Flow Planning**:
   ```
   Annual Expected Loss = $34,250

   Monthly Cash Flow:
   Premium Received: $50,000 / 12 = $4,167/month
   Expected Claims: $34,250 / 12 = $2,854/month
   Net Cash Flow: $1,313/month (before expenses)
   ```

4. **Pricing Adequacy**:
   ```
   Current Premium: $50,000
   Expected Loss: $34,250
   Target Loss Ratio: 65%

   Indicated Premium = $34,250 / 0.65
                     = $52,692

   Rate Increase Needed = ($52,692 - $50,000) / $50,000
                        = 5.4%
   ```

---

## 7. Expected Profit

### Purpose
Calculate the expected underwriting profit (premium minus expected losses), excluding expenses.

### Formula
```
Expected Profit = Annual Premium - Expected Loss
```

Or equivalently:
```
Expected Profit = Annual Premium × (1 - Predicted Loss Ratio / 100)
```

### Code Reference
[frontend/pages/3_Risk_Prediction.py:262](frontend/pages/3_Risk_Prediction.py#L262)

### Example Calculation

**Method 1 - Direct**:
```
Annual Premium = $50,000
Expected Loss = $34,250
```

**Calculation**:
```
Expected Profit = $50,000 - $34,250
                = $15,750
```

**Method 2 - Using Loss Ratio** (Verification):
```
Annual Premium = $50,000
Predicted Loss Ratio = 68.5%

Expected Profit = $50,000 × (1 - 68.5/100)
                = $50,000 × (1 - 0.685)
                = $50,000 × 0.315
                = $15,750 ✓
```

### Interpretation

**Expected Profit of $15,750**:
- Represents funds available for expenses and profit
- Must cover underwriting expenses, commissions, overhead
- If expenses = 30% of premium ($15,000), leaves $750 for profit
- Indicates marginally profitable policy

### Profit Scenarios

**By Loss Ratio Ranges**:
```
Premium = $50,000

Loss Ratio    Expected Loss    Expected Profit    Status
──────────────────────────────────────────────────────────
50%          $25,000          $25,000            Excellent
60%          $30,000          $20,000            Good
68.5%        $34,250          $15,750            Marginal
75%          $37,500          $12,500            Poor
85%          $42,500          $7,500             Very Poor
100%         $50,000          $0                 Break-even
```

### Profit Range (Using Confidence Intervals)

**With Uncertainty**:
```
Premium: $50,000
Loss Ratio CI: [53.5%, 83.5%]

Best Case Profit = $50,000 × (1 - 0.535)
                 = $50,000 × 0.465
                 = $23,250

Expected Profit = $50,000 × (1 - 0.685)
                = $15,750

Worst Case Profit = $50,000 × (1 - 0.835)
                  = $50,000 × 0.165
                  = $8,250

Profit Range = [$8,250, $23,250]
Variability = $15,000
```

### Business Applications

1. **Underwriting Decision**:
   ```
   Expected Profit: $15,750
   Target Expense Ratio: 30%
   Expected Expenses: $15,000

   Net Profit = $15,750 - $15,000 = $750

   Decision: Marginally acceptable, request higher premium
   ```

2. **Minimum Premium Calculation**:
   ```
   Expected Loss: $34,250
   Required Profit: $5,000 (10% of premium)
   Expense Ratio: 30%

   Let P = Required Premium
   P - 0.30P - $34,250 = $5,000
   0.70P = $39,250
   P = $56,071

   Minimum Premium = $56,071 (vs. current $50,000)
   Increase Needed = 12.1%
   ```

3. **Profit Target Achievement**:
   ```
   Current Premium: $50,000
   Expected Profit: $15,750
   Target Profit Margin: 10% ($5,000)
   Expenses: 30% ($15,000)

   Total Needed = $34,250 + $15,000 + $5,000 = $54,250
   Current Premium: $50,000
   Shortfall: $4,250

   Either: Increase premium by 8.5%
   Or: Reduce expenses by $4,250
   ```

4. **Portfolio Contribution**:
   ```
   Policy Expected Profit: $15,750
   Expenses (30%): $15,000
   Net Contribution: $750

   For 100 similar policies:
   Total Premium: $5,000,000
   Total Expected Profit: $1,575,000
   Total Expenses: $1,500,000
   Total Net Profit: $75,000 (1.5% profit margin)
   ```

---

## 8. Profit Margin

### Purpose
Calculate the expected profit as a percentage of premium, indicating the profitability rate.

### Formula
```
Profit Margin (%) = (Expected Profit / Annual Premium) × 100%
```

Or equivalently:
```
Profit Margin (%) = (1 - Predicted Loss Ratio / 100) × 100%
                  = 100% - Predicted Loss Ratio
```

### Code Reference
[frontend/pages/3_Risk_Prediction.py:266](frontend/pages/3_Risk_Prediction.py#L266)

### Example Calculation

**Method 1 - Using Expected Profit**:
```
Expected Profit = $15,750
Annual Premium = $50,000
```

**Calculation**:
```
Profit Margin = ($15,750 / $50,000) × 100%
              = 0.315 × 100%
              = 31.5%
```

**Method 2 - Using Loss Ratio** (Verification):
```
Predicted Loss Ratio = 68.5%

Profit Margin = (1 - 68.5/100) × 100%
              = (1 - 0.685) × 100%
              = 0.315 × 100%
              = 31.5% ✓
```

**Method 3 - Direct** (Simplest):
```
Predicted Loss Ratio = 68.5%

Profit Margin = 100% - 68.5%
              = 31.5% ✓
```

### Interpretation

**Profit Margin of 31.5%**:
- 31.5% of premium is available for expenses and profit
- Must cover ~30% in expenses, leaving ~1.5% for net profit
- Marginally profitable after expenses
- Typical target: 35-40% for 5-10% net profit

### Profit Margin Targets

**Industry Benchmarks**:
```
Margin Range    Net After 30% Expenses    Assessment
──────────────────────────────────────────────────────
> 40%           > 10%                     Excellent
35-40%          5-10%                     Good
30-35%          0-5%                      Acceptable
25-30%          -5-0%                     Poor
< 25%           < -5%                     Unprofitable
```

**Example Analysis**:
```
Profit Margin: 31.5%
Expected Expenses: 30.0%
Net Margin: 1.5%

Status: Marginally acceptable
```

### Relationship to Loss Ratio

**Direct Inverse Relationship**:
```
Loss Ratio    Profit Margin    Net Profit (30% exp)
────────────────────────────────────────────────────
50%           50%              20%
55%           45%              15%
60%           40%              10%
65%           35%              5%
68.5%         31.5%            1.5%  ← Current
70%           30%              0%
75%           25%              -5%
80%           20%              -10%
```

### Margin Range (With Uncertainty)

**Using Loss Ratio Confidence Intervals**:
```
Loss Ratio CI: [53.5%, 83.5%]

Best Case Margin = 100% - 53.5% = 46.5%
Expected Margin = 100% - 68.5% = 31.5%
Worst Case Margin = 100% - 83.5% = 16.5%

Margin Range = [16.5%, 46.5%]
Uncertainty = ±15 percentage points
```

### Business Applications

1. **Profitability Assessment**:
   ```
   Profit Margin: 31.5%
   Expense Ratio: 30.0%

   Combined Ratio = 68.5% + 30.0% = 98.5%

   Underwriting Profit = 100% - 98.5% = 1.5%

   Assessment: Marginally profitable, acceptable
   ```

2. **Pricing Adjustment**:
   ```
   Current Margin: 31.5%
   Target Margin: 35.0% (for 5% net profit)
   Gap: 3.5 percentage points

   Required Loss Ratio = 100% - 35% = 65%
   Current Loss Ratio = 68.5%

   Rate Increase = 68.5% / 65% - 1
                 = 1.0538 - 1
                 = 5.38%
   ```

3. **Risk Tolerance**:
   ```
   Worst Case Margin (using CI): 16.5%
   Expense Ratio: 30%

   Worst Case Combined = 83.5% + 30% = 113.5%
   Worst Case Loss = -13.5%

   Decision: Risk too high for current premium
   Action: Increase premium or decline
   ```

4. **Portfolio Optimization**:
   ```
   Target: Average 35% profit margin
   Current Policy: 31.5%

   To maintain portfolio average:
   - Accept with higher volume
   - Mix with higher margin policies (> 40%)
   - Or increase premium to reach 35%
   ```

---

## 9. Composite Risk Score

### Purpose
Create a unified risk score combining the COPE risk rating with the predicted loss ratio to provide an overall risk assessment.

### Formula
```
Composite Risk Score = min(10, Risk Rating × (Predicted Loss Ratio / 65))
```

**Where**:
- Risk Rating: COPE-based score (1-10)
- 65: Target loss ratio benchmark
- min(10, ...): Caps the score at maximum of 10

### Code Reference
[frontend/pages/3_Risk_Prediction.py:270](frontend/pages/3_Risk_Prediction.py#L270)

### Example Calculation

**Scenario**:
```
Risk Rating (COPE): 6.5
Predicted Loss Ratio: 68.5%
```

**Calculation**:
```
Composite Risk Score = min(10, 6.5 × (68.5 / 65))
                     = min(10, 6.5 × 1.0538)
                     = min(10, 6.85)
                     = 6.85 / 10
```

**Result**: 6.85 out of 10 (medium-high risk)

### Interpretation

**Composite Score Scale**:
```
Score Range    Risk Level       Interpretation
─────────────────────────────────────────────────
1.0 - 3.0      Low Risk         Excellent risk quality
3.0 - 5.0      Medium-Low       Good risk, acceptable
5.0 - 7.0      Medium           Standard risk, monitor
7.0 - 8.5      Medium-High      Elevated risk, caution
8.5 - 10.0     High Risk        Decline or major premium increase
```

**Current Score (6.85)**:
- Medium-high risk level
- Approaching concerning territory
- Requires careful underwriting
- Consider premium adjustment

### Score Components Analysis

**Risk Rating Contribution**:
```
Base COPE Rating: 6.5 (medium-high construction/occupancy risk)

Contributes:
  • Building quality assessment
  • Occupancy hazard level
  • Protection systems quality
  • External exposure factors
```

**Loss Ratio Contribution**:
```
LR Multiplier: 68.5 / 65 = 1.0538 (5.38% above target)

Contributes:
  • Expected financial performance
  • Pricing adequacy
  • Predicted profitability
```

### Example Scenarios

**Scenario 1 - Low Risk, Low Loss Ratio**:
```
Risk Rating: 3.0
Loss Ratio: 55%

Composite = min(10, 3.0 × (55/65))
          = min(10, 3.0 × 0.846)
          = min(10, 2.54)
          = 2.54 (Low Risk)
```

**Scenario 2 - High Risk, High Loss Ratio**:
```
Risk Rating: 8.5
Loss Ratio: 85%

Composite = min(10, 8.5 × (85/65))
          = min(10, 8.5 × 1.308)
          = min(10, 11.12)
          = 10.0 (Maximum Risk - Capped)
```

**Scenario 3 - Low Risk, High Loss Ratio**:
```
Risk Rating: 3.0
Loss Ratio: 82%

Composite = min(10, 3.0 × (82/65))
          = min(10, 3.0 × 1.262)
          = min(10, 3.79)
          = 3.79 (Medium-Low Risk)

Note: Poor pricing but good physical risk
```

**Scenario 4 - High Risk, Low Loss Ratio**:
```
Risk Rating: 8.0
Loss Ratio: 58%

Composite = min(10, 8.0 × (58/65))
          = min(10, 8.0 × 0.892)
          = min(10, 7.14)
          = 7.14 (Medium-High Risk)

Note: Good pricing but concerning physical risk
```

### Business Applications

1. **Underwriting Tiers**:
   ```
   Score < 4.0: Preferred tier, standard rates
   Score 4.0-7.0: Standard tier, normal underwriting
   Score 7.0-8.5: Substandard tier, higher rates
   Score > 8.5: Decline or refer to senior underwriter

   Current Score (6.85): Standard tier, upper end
   ```

2. **Premium Adjustment**:
   ```
   Base Premium: $50,000
   Composite Score: 6.85

   Adjustment Factor = Composite Score / 5.0 (neutral point)
                     = 6.85 / 5.0
                     = 1.37

   Adjusted Premium = $50,000 × 1.37
                    = $68,500
   ```

3. **Risk Monitoring**:
   ```
   Threshold: Score > 7.0 triggers review
   Current: 6.85

   Status: Close to threshold
   Action: Flag for renewal review
           Monitor claims closely
           Consider rate increase at renewal
   ```

4. **Portfolio Management**:
   ```
   Target Portfolio Average Score: 5.0
   Current Policy Score: 6.85

   To maintain average:
   - Need policies with scores < 3.15 to balance
   - Or decline this policy
   - Or increase to reduce loss ratio component
   ```

### Mathematical Properties

**Sensitivity to Loss Ratio**:
```
For Risk Rating = 6.5:

LR 60% → Score = 6.0
LR 65% → Score = 6.5 (baseline)
LR 70% → Score = 7.0
LR 75% → Score = 7.5
LR 80% → Score = 8.0

Each 5% increase in LR increases score by ~0.5
```

**Sensitivity to Risk Rating**:
```
For Loss Ratio = 68.5%:

RR 5.0 → Score = 5.27
RR 6.0 → Score = 6.32
RR 6.5 → Score = 6.85 (current)
RR 7.0 → Score = 7.38
RR 8.0 → Score = 8.43

Each 1.0 increase in RR increases score by ~1.05
```

---

## 10. Prediction Uncertainty

### Purpose
Quantify the uncertainty in the severity prediction as a percentage of the predicted value, helping assess prediction reliability.

### Formula
```
Uncertainty (%) = ((Upper CI - Lower CI) / Predicted Severity × 100%) / 2

Or equivalently:
Uncertainty (%) = (Range / Predicted Value × 100%) / 2
```

**Where**:
- Upper CI: Upper bound of confidence interval
- Lower CI: Lower bound of confidence interval
- The division by 2 converts full range to ±uncertainty

### Code Reference
[frontend/pages/3_Risk_Prediction.py:238-240](frontend/pages/3_Risk_Prediction.py#L238-L240)

### Example Calculation

**Scenario**:
```
Predicted Severity = $125,000
Confidence Interval = [$87,500, $162,500]
```

**Calculation**:
```
Range = Upper CI - Lower CI
      = $162,500 - $87,500
      = $75,000

Range Percentage = ($75,000 / $125,000) × 100%
                 = 0.60 × 100%
                 = 60%

Uncertainty = 60% / 2
            = ±30%
```

### Interpretation

**Uncertainty of ±30%**:
- Prediction could vary by 30% above or below the expected value
- Relatively high uncertainty (typical for claim severity)
- Indicates moderate confidence in point estimate
- Suggests need for conservative reserving

### Uncertainty Levels

**Low Uncertainty** (< ±15%):
```
Example: ±10%
Predicted: $100,000
Range: [$90,000, $110,000]

Indicates:
  • High confidence prediction
  • Homogeneous risk group
  • Stable severity patterns
  • Well-understood exposures
```

**Medium Uncertainty** (±15% to ±35%):
```
Example: ±30% (current)
Predicted: $125,000
Range: [$87,500, $162,500]

Indicates:
  • Moderate confidence
  • Typical severity variation
  • Standard commercial property
  • Normal prediction quality
```

**High Uncertainty** (> ±35%):
```
Example: ±50%
Predicted: $150,000
Range: [$75,000, $225,000]

Indicates:
  • Low confidence
  • Heterogeneous exposures
  • Volatile severity patterns
  • Unusual or high-risk properties
  • Limited historical data
```

### Relationship to Confidence Interval Width

**Mathematical Equivalence**:
```
For CI = [Lower, Upper] around prediction P:

If Lower = P × 0.7 and Upper = P × 1.3:

Range = P × 1.3 - P × 0.7
      = P × (1.3 - 0.7)
      = P × 0.6
      = 60% of P

Uncertainty = (60% of P) / P / 2
            = 60% / 2
            = ±30%
```

### Business Applications

1. **Reserve Setting**:
   ```
   Predicted Severity: $125,000
   Uncertainty: ±30%

   Conservative Reserve = $125,000 × 1.30
                        = $162,500

   Expected Reserve = $125,000

   Optimistic Reserve = $125,000 × 0.70
                      = $87,500

   Recommended: Use conservative estimate for reserving
   ```

2. **Credibility Assessment**:
   ```
   Uncertainty ±30%:

   Credibility Factor = 1 / (1 + Uncertainty)
                      = 1 / (1 + 0.30)
                      = 1 / 1.30
                      = 77%

   Blend with external benchmark:
   Final Estimate = 77% × $125,000 + 23% × Industry_Average
   ```

3. **Risk Classification**:
   ```
   If Uncertainty > 40%: High Risk Class
   If Uncertainty 20-40%: Standard Class
   If Uncertainty < 20%: Preferred Class

   Current (30%): Standard Class
   ```

4. **Pricing Margin**:
   ```
   Predicted Severity: $125,000
   Uncertainty: ±30%

   Safety Loading = Uncertainty × Predicted
                  = 0.30 × $125,000
                  = $37,500

   Conservative Pricing Basis = $125,000 + $37,500
                              = $162,500

   Or: Use Upper CI directly ($162,500)
   ```

### Uncertainty vs. Confidence Level

**95% Confidence Interval**:
```
Uncertainty ±30% implies:
  • 95% probability actual value within [$87,500, $162,500]
  • 5% probability outside this range
  • 2.5% chance below $87,500
  • 2.5% chance above $162,500
```

**Other Confidence Levels**:
```
90% CI: Narrower interval, lower uncertainty
  Example: ±25% instead of ±30%

99% CI: Wider interval, higher uncertainty
  Example: ±40% instead of ±30%
```

---

## 11. Default Prediction (Loss Ratio)

### Purpose
Provide a reasonable loss ratio estimate when the trained ML model is not available, using industry averages.

### Formula
```
Default Loss Ratio = 65.0%
Default Confidence Interval = [50.0%, 80.0%]
```

### Code Reference
[backend/services/prediction.py:98-104](backend/services/prediction.py#L98-L104)

### Rationale

**Why 65%?**
- Industry standard target for commercial property
- Balanced between profitability and competitiveness
- Represents typical expected losses for standard risks
- Allows for ~35% expense ratio and profit margin

**Why [50%, 80%] Interval?**
- 50%: Represents excellent performance (low losses)
- 80%: Represents acceptable ceiling (still profitable with lean expenses)
- 30-point range reflects typical portfolio variability
- Conservative bounds for model-free estimation

### Business Context

**Target Loss Ratio Ranges by Line**:
```
Line of Business           Target LR    Acceptable Range
─────────────────────────────────────────────────────────
Commercial Property         65%         55% - 75%
General Liability           70%         60% - 80%
Commercial Auto Physical    70%         60% - 80%
Workers Compensation        65%         55% - 75%
Professional Liability      60%         50% - 70%
```

### When Default Is Used

**Trigger Conditions**:
1. Model files not found in `models/` directory
2. Model failed to load due to corruption
3. Development/testing environment without trained models
4. First-time deployment before model training

**User Notification**:
```
Message: "Model not loaded - using default estimate"
Flag: model_loaded = False
```

### Example Usage

**Scenario**: New deployment without trained models
```
Input:
  Geography: Northeast
  Industry: Manufacturing
  Risk Rating: 6.5
  Premium: $50,000

Output:
  Predicted Loss Ratio: 65.0%
  Confidence Interval: [50.0%, 80.0%]
  Model Loaded: False
  Message: "Model not loaded - using default estimate"
```

**Interpretation**:
- Use as rough estimate only
- Plan to train and deploy actual model
- Consider as conservative baseline
- Don't rely on this for production underwriting decisions

### Limitations

**Default Prediction Limitations**:
1. **No Risk Differentiation**:
   - Same 65% for low-risk and high-risk accounts
   - Ignores geography, industry, and other factors
   - Not suitable for accurate pricing

2. **No Learning**:
   - Doesn't improve with more data
   - Doesn't capture portfolio-specific patterns
   - Generic across all insurers

3. **Wide Confidence Interval**:
   - 30-point range indicates high uncertainty
   - Not useful for precise risk assessment
   - Reflects lack of specific information

4. **Business Impact**:
   - Cannot support sophisticated pricing
   - Inadequate for competitive quoting
   - May lead to adverse selection

### Recommended Actions

**When Default Is Triggered**:

1. **Immediate**:
   - Flag the prediction as preliminary
   - Use additional underwriting judgment
   - Consider manual risk assessment

2. **Short-term**:
   - Train model on historical data
   - Validate model performance
   - Deploy trained model files

3. **Long-term**:
   - Implement model monitoring
   - Regular model retraining
   - A/B testing for improvements

---

## 12. Default Prediction (Severity)

### Purpose
Provide a reasonable severity estimate when the trained ML model is not available, using policy size as a proxy.

### Formula

**Base Severity by Policy Size**:
```
Policy Size    Base Severity
─────────────────────────────
Small          $50,000
Medium         $100,000
Large          $250,000
Enterprise     $500,000
```

**Confidence Interval**:
```
Lower Bound = Base Severity × 0.7
Upper Bound = Base Severity × 1.3
```

### Code Reference
[backend/services/prediction.py:142-160](backend/services/prediction.py#L142-L160)

### Rationale

**Policy Size as Proxy**:
- Larger policies generally have higher building values
- Higher values correlate with higher claim amounts
- Provides basic risk differentiation
- Simple, intuitive relationship

**Multiplier Selection**:
- ×1 baseline for Small ($50K)
- ×2 for Medium ($100K)
- ×5 for Large ($250K)
- ×10 for Enterprise ($500K)
- Reflects typical building value distributions

**Confidence Interval (±30%)**:
- Same relative uncertainty as model-based predictions
- Consistent with typical severity variability
- Conservative for model-free estimation

### Example Calculations

**Example 1: Medium Policy**:
```
Policy Size: Medium

Base Severity = $100,000

Lower Bound = $100,000 × 0.7 = $70,000
Upper Bound = $100,000 × 1.3 = $130,000

Confidence Interval = [$70,000, $130,000]
```

**Example 2: Large Policy**:
```
Policy Size: Large

Base Severity = $250,000

Lower Bound = $250,000 × 0.7 = $175,000
Upper Bound = $250,000 × 1.3 = $325,000

Confidence Interval = [$175,000, $325,000]
```

### Policy Size Definitions

**Typical Classifications**:
```
Size          Premium Range    Building Value      Exposure Units
───────────────────────────────────────────────────────────────────
Small         < $10,000        < $1M               < 10 units
Medium        $10K - $50K      $1M - $5M           10 - 50 units
Large         $50K - $250K     $5M - $25M          50 - 250 units
Enterprise    > $250K          > $25M              > 250 units
```

### Business Context

**Severity by Property Type**:
```
Property Type        Small      Medium     Large       Enterprise
────────────────────────────────────────────────────────────────
Retail Strip        $35K       $85K       $200K       $450K
Office Building     $45K       $110K      $275K       $550K
Warehouse          $40K       $95K       $235K       $480K
Manufacturing      $55K       $125K      $290K       $575K
```

### Limitations

**Default Severity Limitations**:

1. **Oversimplification**:
   - Ignores industry risk differences
   - Doesn't account for geography/catastrophe exposure
   - No consideration of construction quality
   - Risk rating not incorporated

2. **Broad Generalizations**:
   - Wide ranges within each policy size
   - Same estimate for all industries
   - Doesn't reflect individual building characteristics

3. **Business Impact**:
   - Inadequate for precise reserve setting
   - May underestimate high-hazard industries
   - May overestimate low-hazard industries

### Example Usage

**Scenario**: Model not available, Large manufacturing policy
```
Input:
  Policy Size: Large
  Industry: Manufacturing (ignored in default)
  Risk Rating: 7.5 (ignored in default)
  Premium: $150,000

Output:
  Predicted Severity: $250,000
  Confidence Interval: [$175,000, $325,000]
  Model Loaded: False
  Message: "Model not loaded - using policy size-based estimate"
```

**Reality Check**:
- Large manufacturing typically has higher severity
- Model would likely predict $275K - $300K
- Default ($250K) is conservative baseline
- Acceptable as placeholder, not for final decisions

### Comparison: Default vs. Model-Based

**Example: Medium Policy, Manufacturing, High Risk**:

```
Default Prediction:
  Severity: $100,000
  Basis: Policy size only

Model-Based Prediction:
  Severity: $135,000
  Basis: Policy size + industry + risk rating + geography

Difference: $35,000 (35% higher)
Reason: Model captures industry hazard and risk quality
```

---

## 13. Feature Importance

### Purpose
Identify which input features have the greatest influence on model predictions, guiding underwriting focus and data quality efforts.

### Formula

**Feature Importance (LightGBM)**:
```
Importance Score = Number of times feature is used for splitting × average gain

Normalized Importance = Feature Score / Sum of all scores
```

**Ranking**:
```
Features ranked by normalized importance score (descending)
```

### Code Reference
[backend/services/prediction.py:206-237](backend/services/prediction.py#L206-L237)
[frontend/pages/3_Risk_Prediction.py:278-291](frontend/pages/3_Risk_Prediction.py#L278-291)

### Feature List

**All Features in Order of Typical Importance**:

1. **Risk Rating (COPE)** - Primary driver
   - Construction quality
   - Occupancy hazard
   - Protection systems
   - External exposures

2. **Geography** - Regional patterns
   - Catastrophe exposure
   - Climate factors
   - Local building codes
   - Regional loss trends

3. **Industry** - Business-specific hazards
   - Operational risks
   - Equipment types
   - Process hazards
   - Fire load

4. **Policy Size** - Exposure magnitude
   - Building values
   - Limit selections
   - Account significance

5. **Exposure Units** - Risk volume
   - Number of buildings
   - Total insured value
   - Portfolio concentration

6. **Annual Premium** - Pricing signal
   - Rate adequacy
   - Underwriting judgment
   - Competitive position

### Example Feature Importance Output

**Typical Importance Distribution**:
```
Feature           Importance    % of Total
────────────────────────────────────────────
RiskRating        0.3850        38.5%
Geography         0.2100        21.0%
Industry          0.1900        19.0%
PolicySize        0.1200        12.0%
ExposureUnits     0.0550        5.5%
AnnualPremium     0.0400        4.0%
────────────────────────────────────────────
Total             1.0000        100.0%
```

### Interpretation

**High Importance (> 20%)**:
- Primary drivers of prediction
- Focus data quality efforts here
- Most impactful for risk differentiation
- Critical for underwriting decisions

**Medium Importance (10-20%)**:
- Significant contributors
- Worthwhile to capture accurately
- Support primary drivers
- Useful for segmentation

**Low Importance (< 10%)**:
- Minor contributors
- May be redundant with other features
- Consider removing if costly to collect
- Or engineer into better features

### Business Applications

1. **Data Quality Priorities**:
   ```
   RiskRating (38.5% importance):
   → Ensure consistent COPE scoring
   → Train underwriters on rating methodology
   → Implement quality controls
   → Invest in assessment tools

   Geography (21.0% importance):
   → Verify accurate geocoding
   → Maintain current territory definitions
   → Monitor for catastrophe exposure
   ```

2. **Underwriting Focus**:
   ```
   Most Important: RiskRating, Geography, Industry

   Underwriter Checklist:
   ☑ Comprehensive COPE assessment
   ☑ Verify correct territory assignment
   ☑ Understand industry-specific hazards
   ☐ Review policy size (less critical)
   ☐ Validate exposure units (secondary)
   ```

3. **Model Improvement**:
   ```
   Low importance (AnnualPremium 4.0%):
   Potential issues:
   - May indicate circular logic (premium depends on risk)
   - Could be redundant with other features
   - Consider removing from future models

   Action: Test model without this feature
   ```

4. **Pricing Strategy**:
   ```
   High importance features → Bigger rate differentials

   RiskRating (38.5%):
   Rating Factor Range: 0.65 - 1.50 (wide range)

   ExposureUnits (5.5%):
   Rating Factor Range: 0.95 - 1.10 (narrow range)
   ```

### Feature Importance by Model

**Loss Ratio Model** (typical):
```
1. RiskRating (40%) - Drives expected losses directly
2. Geography (22%) - Regional loss patterns
3. Industry (18%) - Business hazards
4. PolicySize (12%) - Scale effects
5. ExposureUnits (5%) - Correlation with size
6. AnnualPremium (3%) - Pricing signal
```

**Severity Model** (typical):
```
1. PolicySize (35%) - Larger policies = larger claims
2. RiskRating (25%) - Risk quality affects severity
3. Industry (20%) - Industry affects claim types
4. ExposureUnits (12%) - Building values
5. Geography (5%) - Less important for severity
6. AnnualPremium (3%) - Weak signal
```

### Statistical Interpretation

**Gain-Based Importance**:
- Measures quality of splits
- Higher gain = better predictive power
- Accumulated across all trees
- Normalized to sum to 1.0

**Split-Based Importance**:
- Counts how often feature is used
- Measures frequency of use
- May overweight multi-valued features
- LightGBM uses gain-based by default

---

## 14. ML Model Architecture Overview

### Purpose
Understand the complete machine learning pipeline from input to prediction, including model selection, training, and deployment.

### Model Selection

**Algorithm**: LightGBM (Light Gradient Boosting Machine)

**Why LightGBM?**
1. **Efficiency**:
   - Faster training than traditional GBDT
   - Lower memory usage
   - Handles large datasets well

2. **Accuracy**:
   - State-of-the-art performance
   - Captures complex non-linear relationships
   - Handles feature interactions

3. **Robustness**:
   - Works with mixed data types
   - Resistant to overfitting
   - Handles missing values
   - No need for feature scaling

4. **Interpretability**:
   - Feature importance available
   - SHAP value support
   - Tree visualization possible

### Architecture Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. DATA INPUT                                       │
├─────────────────────────────────────────────────────┤
│ Raw Features:                                       │
│   • Geography (categorical)                         │
│   • Industry (categorical)                          │
│   • Policy Size (ordinal)                           │
│   • Risk Rating (continuous: 1-10)                  │
│   • Exposure Units (continuous)                     │
│   • Annual Premium (continuous)                     │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 2. FEATURE ENGINEERING                              │
├─────────────────────────────────────────────────────┤
│ Transformations:                                    │
│   • Label encoding: Geography, Industry             │
│   • Ordinal encoding: Policy Size                   │
│   • No scaling (tree-based model)                   │
│   • No missing value imputation needed              │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 3. MODEL ARCHITECTURE                               │
├─────────────────────────────────────────────────────┤
│ LightGBM Parameters (typical):                      │
│   • objective: 'regression'                         │
│   • metric: 'rmse' (root mean squared error)        │
│   • num_leaves: 31                                  │
│   • learning_rate: 0.05                             │
│   • n_estimators: 100-500 trees                     │
│   • max_depth: -1 (no limit, leaf-wise growth)      │
│   • min_child_samples: 20                           │
│   • subsample: 0.8 (row sampling)                   │
│   • colsample_bytree: 0.8 (feature sampling)        │
│   • reg_alpha: 0.1 (L1 regularization)              │
│   • reg_lambda: 0.1 (L2 regularization)             │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 4. ENSEMBLE PREDICTION                              │
├─────────────────────────────────────────────────────┤
│ Process:                                            │
│   • Each tree makes a prediction                    │
│   • Predictions are weighted by learning rate       │
│   • Final = sum of all tree predictions             │
│   • For regression: direct output                   │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 5. PREDICTION OUTPUT                                │
├─────────────────────────────────────────────────────┤
│ Loss Ratio Model → Predicted LR (%)                 │
│ Severity Model → Predicted Severity ($)             │
│                                                      │
│ Post-processing:                                    │
│   • Round to appropriate precision                  │
│   • Calculate confidence intervals                  │
│   • Apply business rules/caps                       │
└─────────────────────────────────────────────────────┘
```

### Training Process

**Historical Data Requirements**:
```
Minimum:
  • 1,000+ policies with claims experience
  • 2+ years of data
  • Representative distribution of features

Optimal:
  • 10,000+ policies
  • 5+ years of data
  • Balanced across all segments
```

**Training Steps**:
```
1. Data Preparation:
   ├── Extract policy and claims data
   ├── Calculate actual loss ratios and severities
   ├── Encode categorical features
   └── Split train/validation/test (70/15/15)

2. Model Training:
   ├── Initialize LightGBM regressor
   ├── Fit on training data
   ├── Validate on validation set
   └── Tune hyperparameters

3. Model Evaluation:
   ├── Predict on test set
   ├── Calculate RMSE, MAE, R²
   ├── Check for overfitting
   └── Validate business logic

4. Model Deployment:
   ├── Save model to disk (.pkl file)
   ├── Version control
   ├── Deploy to production
   └── Monitor performance
```

### Performance Metrics

**Loss Ratio Model Metrics**:
```
Metric                  Target       Interpretation
───────────────────────────────────────────────────────
RMSE (Root MSE)        < 15%        Avg error in loss ratio
MAE (Mean Abs Error)   < 10%        Typical error magnitude
R² (R-squared)         > 0.60       Variance explained
MAPE (Mean Abs %)      < 20%        Relative error
```

**Example Evaluation**:
```
Test Set Results:
  RMSE: 12.5%          ✓ Good (< 15%)
  MAE: 9.2%            ✓ Good (< 10%)
  R²: 0.68             ✓ Good (> 0.60)
  MAPE: 18.3%          ✓ Acceptable (< 20%)

Conclusion: Model ready for production
```

**Severity Model Metrics**:
```
Metric                  Target       Interpretation
───────────────────────────────────────────────────────
RMSE                   < $50K       Avg error in severity
MAE                    < $30K       Typical error magnitude
R²                     > 0.50       Variance explained
MAPE                   < 30%        Relative error
```

### Prediction Pipeline

**Real-Time Prediction Flow**:
```
1. User Input (Web Form)
   ↓
2. API Request
   ↓
3. Feature Preparation
   ├── Encode categorical variables
   ├── Validate input ranges
   └── Create feature vector
   ↓
4. Model Prediction
   ├── Load model from disk (if not cached)
   ├── Call model.predict(features)
   └── Post-process output
   ↓
5. Confidence Intervals
   ├── Calculate bounds
   ├── Apply caps/floors
   └── Round to precision
   ↓
6. API Response
   ├── Format JSON response
   ├── Include metadata
   └── Return to frontend
   ↓
7. UI Display
   ├── Render predictions
   ├── Show confidence intervals
   └── Provide interpretations
```

### Model Maintenance

**Retraining Schedule**:
```
Frequency          Trigger                  Action
────────────────────────────────────────────────────────
Quarterly          Calendar                 Routine retrain
Ad-hoc             Performance degradation  Investigate & retrain
Annual             Model refresh            Full review & rebuild
As-needed          Major portfolio changes  Immediate retrain
```

**Performance Monitoring**:
```
Track:
  • Prediction vs. Actual (ongoing)
  • RMSE drift over time
  • Prediction distribution shifts
  • Feature importance changes

Alert if:
  • RMSE increases > 20%
  • Bias > ±5% loss ratio points
  • Predictions outside historical range
  • Missing feature importance
```

### Model Limitations

**Known Limitations**:

1. **Historical Bias**:
   - Model learns from past data
   - May not capture emerging trends
   - Assumes future similar to past

2. **Feature Limitations**:
   - Limited to 6 input features
   - May miss important risk factors
   - External data not incorporated

3. **Extrapolation Risk**:
   - Less reliable for unusual combinations
   - Wide confidence intervals for edge cases
   - Defaults to conservative estimates

4. **Calibration**:
   - May over/under-predict in some segments
   - Requires periodic recalibration
   - Business rules may override

### Future Enhancements

**Potential Improvements**:

1. **Additional Features**:
   - Claims history
   - Credit scores
   - External data (weather, crime)
   - Property characteristics (age, square footage)

2. **Advanced Models**:
   - Neural networks for complex patterns
   - Ensemble of multiple models
   - Quantile regression for better CI
   - Bayesian models for uncertainty

3. **Real-Time Learning**:
   - Online learning as new data arrives
   - Adaptive models
   - A/B testing framework

4. **Interpretability**:
   - SHAP values for predictions
   - Individual feature contributions
   - Counterfactual explanations

---

## Summary Table: All Formulas

| # | Formula/Calculation | Purpose | Code Location |
|---|---------------------|---------|---------------|
| 1 | Feature Encoding | Transform categorical inputs | prediction.py:61-85 |
| 2 | Loss Ratio Prediction | ML model prediction of LR | prediction.py:87-131 |
| 3 | Severity Prediction | ML model prediction of severity | prediction.py:132-186 |
| 4 | CI (Loss Ratio) | `[LR-15, LR+15]` | prediction.py:113-116 |
| 5 | CI (Severity) | `[Sev×0.7, Sev×1.3]` | prediction.py:168-171 |
| 6 | Expected Loss | `Premium × (LR/100)` | 3_Risk_Prediction.py:254 |
| 7 | Expected Profit | `Premium - Expected Loss` | 3_Risk_Prediction.py:262 |
| 8 | Profit Margin | `(Profit/Premium) × 100%` | 3_Risk_Prediction.py:266 |
| 9 | Composite Risk Score | `min(10, RR × LR/65)` | 3_Risk_Prediction.py:270 |
| 10 | Uncertainty | `(Range/Pred) × 50%` | 3_Risk_Prediction.py:238-240 |
| 11 | Default LR | `65%` when model N/A | prediction.py:100 |
| 12 | Default Severity | Policy size-based | prediction.py:145-150 |
| 13 | Feature Importance | LightGBM gain scores | prediction.py:222-230 |

---

## Glossary

**Confidence Interval (CI)**: Range of plausible values reflecting prediction uncertainty

**Composite Risk Score**: Combined metric incorporating COPE rating and predicted loss ratio

**COPE Rating**: Construction, Occupancy, Protection, Exposure risk assessment (1-10 scale)

**Expected Loss**: Predicted dollar amount of losses based on premium and loss ratio

**Expected Profit**: Premium minus expected losses (before expenses)

**Feature Encoding**: Converting categorical variables to numeric format for ML models

**Feature Importance**: Measure of each variable's contribution to model predictions

**LightGBM**: Gradient boosting machine learning algorithm for predictions

**Loss Ratio Prediction**: ML model output estimating expected loss ratio percentage

**Profit Margin**: Expected profit as percentage of premium

**Severity Prediction**: ML model output estimating average claim amount

**Uncertainty**: Measure of prediction variability expressed as ±percentage

---

## References and Resources

### Machine Learning

- **LightGBM Documentation**: https://lightgbm.readthedocs.io/
- **Gradient Boosting Theory**: Friedman (2001) "Greedy Function Approximation"
- **Feature Importance**: Lundberg & Lee (2017) "SHAP Values"

### Actuarial Standards

- **ASOP No. 12**: Risk Classification
- **ASOP No. 23**: Data Quality
- **ASOP No. 56**: Modeling

### Industry Benchmarks

- **CAS Predictive Modeling Seminar**: Materials and papers
- **Actuarial Review**: Articles on ML in insurance
- **ISO**: Industry loss data and trends

---

## Document Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-23 | Initial comprehensive documentation | Actuarial Insights Workbench Team |

---

**End of Document**
