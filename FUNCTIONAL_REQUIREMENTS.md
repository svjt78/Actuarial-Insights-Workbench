# Functional Requirements Specification
# Actuarial Insights Workbench

**Document Version:** 1.0
**Date:** November 22, 2025
**Application:** Actuarial Insights Workbench
**Line of Business:** Commercial Property Insurance
**Audience:** Developers, Stakeholders, QA Team, Product Management

---

## Table of Contents

1. [Document Overview](#document-overview)
2. [Tab 1: Loss Development Dashboard](#tab-1-loss-development-dashboard)
3. [Tab 2: Pricing & Portfolio KPIs](#tab-2-pricing--portfolio-kpis)
4. [Tab 3: Risk Prediction & Scoring](#tab-3-risk-prediction--scoring)
5. [Tab 4: GenAI Insights & Explanations](#tab-4-genai-insights--explanations)
6. [Data Models & Schemas](#data-models--schemas)
7. [Non-Functional Requirements](#non-functional-requirements)
8. [Glossary](#glossary)

---

## Document Overview

### Purpose
This document specifies the functional requirements for the Actuarial Insights Workbench, a web-based analytics platform designed for commercial property insurance actuaries, underwriters, and portfolio managers.

### Scope
This specification covers the four primary dashboard tabs:
- Loss Development Dashboard
- Pricing & Portfolio KPIs
- Risk Prediction & Scoring
- GenAI Insights & Explanations

### Technology Stack
- **Frontend:** Streamlit (Python web framework)
- **Backend:** FastAPI (Python REST API)
- **ML Models:** LightGBM (gradient boosting)
- **GenAI:** OpenAI GPT-3.5-turbo
- **Data Visualization:** Plotly
- **Deployment:** Docker containers

---

## Tab 1: Loss Development Dashboard

### 1.1 Functional Overview

The Loss Development Dashboard shall provide actuaries with comprehensive loss triangle analysis capabilities, including cumulative and incremental loss views, development factor calculations, and IBNR (Incurred But Not Reported) reserve projections.

### 1.2 User Requirements

#### 1.2.1 Loss Triangle Display

**REQ-LD-001:** The system SHALL allow users to select between Incurred Losses and Paid Losses for analysis.

**REQ-LD-002:** The system SHALL allow users to select between cumulative and incremental triangle views.

**REQ-LD-003:** The system SHALL allow users to specify development months with the following constraints:
- Minimum: 12 months
- Maximum: 36 months
- Step increment: 6 months
- Default: 36 months

**REQ-LD-004:** The system SHALL display a "Load Triangle Data" button that retrieves data from the backend API when clicked.

**REQ-LD-005:** The system SHALL display a loading spinner with the text "Fetching loss triangle data..." while data is being retrieved.

**REQ-LD-006:** The system SHALL display a success message "Data loaded successfully!" upon successful data retrieval.

**REQ-LD-007:** The system SHALL display an error message indicating the error code and description if data retrieval fails.

**REQ-LD-008:** The system SHALL display a connection error message "Cannot connect to backend API. Make sure the backend service is running." if the backend is unreachable.

#### 1.2.2 Summary Statistics

**REQ-LD-009:** The system SHALL display the following summary statistics:
- **Total Reported:** Total reported losses to date (formatted as currency)
- **Projected Ultimate:** Projected ultimate losses (formatted as currency)
- **Total IBNR:** Incurred But Not Reported reserves (formatted as currency)
- **Avg Dev Factor:** Average development factor (formatted to 3 decimal places)

**REQ-LD-010:** Each summary metric SHALL include a help tooltip explaining the metric.

#### 1.2.3 Loss Triangle Heatmap

**REQ-LD-011:** The system SHALL display the loss triangle as an interactive heatmap with:
- X-axis: Development months (0 to max_dev_months)
- Y-axis: Accident years
- Color scale: Blues gradient (lighter = lower values, darker = higher values)
- Cell values: Loss amounts formatted with thousand separators

**REQ-LD-012:** The heatmap SHALL display either cumulative or incremental values based on user selection.

**REQ-LD-013:** The heatmap SHALL be titled "{Cumulative/Incremental} Loss Triangle by Accident Year".

**REQ-LD-014:** The system SHALL display cell values within each heatmap cell formatted as whole numbers with commas.

#### 1.2.4 Development Factors

**REQ-LD-015:** The system SHALL display age-to-age development factors in a table with the following columns:
- **Period:** Development period range (e.g., "0-1", "1-2")
- **Factor:** Development factor (formatted to 4 decimal places)
- **Implied % Development:** Percentage development calculated as (Factor - 1) × 100

**REQ-LD-016:** The system SHALL display a line chart visualizing development factors with:
- X-axis: Development period
- Y-axis: Factor value
- Markers at each data point

#### 1.2.5 Ultimate Loss Projections

**REQ-LD-017:** The system SHALL display ultimate loss projections in a table with the following columns:
- **AccidentYear:** The accident year
- **ReportedLoss:** Reported loss to date (formatted as currency)
- **UltimateLoss:** Projected ultimate loss (formatted as currency)
- **IBNR:** IBNR reserve amount (formatted as currency)
- **PercentDeveloped:** Percentage of losses developed (formatted to 1 decimal place)

**REQ-LD-018:** The system SHALL display a bar chart showing "Loss Development Maturity by Accident Year" with:
- X-axis: Accident year
- Y-axis: Percent developed
- Color gradient: Red-Yellow-Green (red = low maturity, green = high maturity)

#### 1.2.6 Methodology Information

**REQ-LD-019:** The system SHALL provide an expandable "About Loss Development Triangles" section explaining:
- What is a loss development triangle
- Key concepts (Accident Year, Development Month, Cumulative/Incremental triangles, Development Factors, IBNR)
- Methodology (chain-ladder method with volume-weighted development factors)

### 1.3 Technical Specifications

#### 1.3.1 API Endpoint

**REQ-LD-TECH-001:** The system SHALL call the backend API endpoint `GET /loss_triangle` with the following query parameters:
- `value_col`: String ("IncurredAmount" or "PaidAmount")
- `triangle_type`: String ("cumulative" or "incremental")
- `max_dev_months`: Integer (12-36)

**REQ-LD-TECH-002:** The API call SHALL have a timeout of 10 seconds.

#### 1.3.2 Response Format

**REQ-LD-TECH-003:** The API SHALL return a JSON response with the following structure:

```json
{
  "cumulative_triangle": {
    "accident_year": {
      "dev_month": loss_amount
    }
  },
  "incremental_triangle": {
    "accident_year": {
      "dev_month": loss_amount
    }
  },
  "development_factors": {
    "period_range": factor_value
  },
  "ultimate_projections": [
    {
      "AccidentYear": year,
      "ReportedLoss": amount,
      "LatestDevMonth": month,
      "UltimateLoss": amount,
      "IBNR": amount,
      "PercentDeveloped": percentage
    }
  ],
  "summary_stats": {
    "total_reported": amount,
    "total_ultimate": amount,
    "total_ibnr": amount,
    "avg_dev_factor": factor
  }
}
```

#### 1.3.3 Algorithms

**REQ-LD-TECH-004:** The system SHALL calculate development factors using the **volume-weighted average** method:
- For each development period transition (e.g., month 0→1, 1→2):
  - Sum all cumulative losses at the earlier period
  - Sum all cumulative losses at the later period
  - Factor = Later Sum / Earlier Sum

**REQ-LD-TECH-005:** The system SHALL project ultimate losses using the **chain-ladder method**:
- Start with the latest reported loss for each accident year
- Multiply by all remaining development factors
- Ultimate Loss = Reported Loss × (Product of remaining factors)

**REQ-LD-TECH-006:** The system SHALL calculate IBNR as:
- IBNR = Ultimate Loss - Reported Loss

**REQ-LD-TECH-007:** The system SHALL calculate percent developed as:
- Percent Developed = (Reported Loss / Ultimate Loss) × 100

### 1.4 Data Requirements

**REQ-LD-DATA-001:** The system SHALL use claims data with the following required fields:
- `ClaimID`: Unique claim identifier
- `PolicyID`: Associated policy identifier
- `LossDate`: Date of loss occurrence
- `ReportDate`: Date claim was reported
- `IncurredAmount`: Total incurred loss amount
- `PaidAmount`: Total paid loss amount

**REQ-LD-DATA-002:** All date fields SHALL be in datetime format.

**REQ-LD-DATA-003:** Loss amounts SHALL be numeric (float) values representing dollars.

### 1.5 Acceptance Criteria

**Test Case LD-TC-001: Load Cumulative Incurred Triangle**
- GIVEN the user is on the Loss Development Dashboard
- WHEN the user selects "Incurred Losses", "Cumulative", "36 months" and clicks "Load Triangle Data"
- THEN the system SHALL display:
  - Summary statistics with non-zero values
  - A cumulative loss triangle heatmap
  - Development factors table and chart
  - Ultimate projections table and maturity chart
- AND all values SHALL be properly formatted

**Test Case LD-TC-002: Load Incremental Paid Triangle**
- GIVEN the user is on the Loss Development Dashboard
- WHEN the user selects "Paid Losses", "Incremental", "24 months" and clicks "Load Triangle Data"
- THEN the system SHALL display an incremental triangle
- AND development factors SHALL be calculated correctly

**Test Case LD-TC-003: API Connection Failure**
- GIVEN the backend API is not running
- WHEN the user clicks "Load Triangle Data"
- THEN the system SHALL display "Cannot connect to backend API. Make sure the backend service is running."
- AND no data SHALL be displayed

**Test Case LD-TC-004: Development Factor Calculation**
- GIVEN a cumulative triangle with known values
- WHEN development factors are calculated
- THEN the factors SHALL use volume-weighted average methodology
- AND factors SHALL be displayed to 4 decimal places

**Test Case LD-TC-005: IBNR Calculation**
- GIVEN ultimate projections are calculated
- WHEN IBNR is computed
- THEN IBNR SHALL equal Ultimate Loss - Reported Loss for each accident year
- AND total IBNR SHALL equal sum of all individual IBNR amounts

---

## Tab 2: Pricing & Portfolio KPIs

### 2.1 Functional Overview

The Pricing & Portfolio KPIs dashboard shall provide underwriters and portfolio managers with segment-level performance metrics, including loss ratios, frequency, severity, and premium distribution across different dimensions.

### 2.2 User Requirements

#### 2.2.1 Segmentation Controls

**REQ-PK-001:** The system SHALL allow users to segment data by the following dimensions:
- **Geography** (displayed as "Geography (Region)")
- **Industry** (displayed as "Industry Sector")
- **PolicySize** (displayed as "Policy Size")
- **RiskRating** (displayed as "Risk Rating (COPE)")

**REQ-PK-002:** The system SHALL allow users to filter segments by minimum premium with:
- Minimum value: $0
- Default value: $0
- Step increment: $10,000
- Input type: Numeric

**REQ-PK-003:** The minimum premium filter SHALL exclude segments with earned premium below the specified threshold.

#### 2.2.2 Data Loading

**REQ-PK-004:** The system SHALL display a "Load KPI Data" button that retrieves segment KPIs when clicked.

**REQ-PK-005:** The system SHALL display a loading spinner with the text "Fetching segment KPIs..." during data retrieval.

**REQ-PK-006:** The system SHALL display appropriate success or error messages similar to REQ-LD-006 through REQ-LD-008.

#### 2.2.3 Overall Portfolio Performance

**REQ-PK-007:** The system SHALL display overall portfolio metrics with the following KPIs:
- **Total Premium:** Total earned premium (in millions, formatted as "$X.XM")
- **Loss Ratio:** Incurred loss ratio as percentage with delta vs 65% target
- **Frequency:** Claims per 100 exposure units (2 decimal places)
- **Severity:** Average claim amount (in thousands, formatted as "$XK")
- **Claim Count:** Total number of claims (with thousand separators)

**REQ-PK-008:** The Loss Ratio metric SHALL display a delta indicator:
- Show difference from 65% target
- Use inverse color (red for above target, green for below target)
- Format as "±X.X% vs 65% target"

**REQ-PK-009:** Each overall metric SHALL include a help tooltip explaining the metric.

#### 2.2.4 Segment KPIs Table

**REQ-PK-010:** The system SHALL display segment KPIs in a tabular format with the following columns:
- **Segment Name** (Geography/Industry/PolicySize/RiskRating)
- **EarnedPremium:** Formatted as currency with no decimals
- **IncurredLoss:** Formatted as currency with no decimals
- **PaidLoss:** Formatted as currency with no decimals
- **LossRatio:** Formatted as percentage with 2 decimals
- **PaidLossRatio:** Formatted as percentage with 2 decimals
- **Frequency:** Formatted with 4 decimal places
- **Severity:** Formatted as currency with no decimals
- **PurePremium:** Formatted as currency with 2 decimals
- **AvgPremium:** Formatted as currency with no decimals
- **TotalExposure:** Formatted with thousand separators, no decimals
- **PolicyCount:** Formatted with thousand separators, no decimals
- **ClaimCount:** Formatted with thousand separators, no decimals

**REQ-PK-011:** The LossRatio column SHALL have a background gradient:
- Color map: Red-Yellow-Green (inverted)
- Minimum value: 40%
- Maximum value: 100%
- Red = high loss ratio, Green = low loss ratio

#### 2.2.5 Visualizations

**REQ-PK-012:** The system SHALL display a bar chart titled "Loss Ratio by {Segment}" with:
- X-axis: Segment values
- Y-axis: Loss Ratio percentage
- Color gradient: Red-Yellow-Green inverted (matching loss ratio scale)
- Horizontal reference line at 65% marked as "Target 65%"

**REQ-PK-013:** The system SHALL display a pie/donut chart titled "Premium Distribution by {Segment}" with:
- Values: Earned premium by segment
- Labels: Segment names
- Hole size: 40% (donut chart)

**REQ-PK-014:** The system SHALL display a scatter plot titled "Frequency vs Severity by {Segment}" with:
- X-axis: Claim frequency (per 100 units)
- Y-axis: Average severity ($)
- Bubble size: Earned premium
- Color: Loss ratio (Red-Yellow-Green inverted scale)
- Hover labels: Segment name

#### 2.2.6 Top/Bottom Performers

**REQ-PK-015:** The system SHALL display "Top Performing Segments" showing:
- 5 segments with lowest loss ratios
- Columns: Segment name, Loss Ratio, Earned Premium
- Caption: "Lowest loss ratios"

**REQ-PK-016:** The system SHALL display "Segments Needing Attention" showing:
- 5 segments with highest loss ratios
- Columns: Segment name, Loss Ratio, Claim Count
- Caption: "Highest loss ratios"

#### 2.2.7 KPI Definitions

**REQ-PK-017:** The system SHALL provide an expandable "KPI Definitions" section explaining:
- Definition of each KPI metric
- Industry benchmarks for commercial property
- COPE risk rating framework

#### 2.2.8 Data Export

**REQ-PK-018:** The system SHALL provide a "Download KPI Data (CSV)" button that:
- Exports all segment KPI data to CSV format
- Names the file "segment_kpis_{segment_by}.csv"
- Includes all KPI columns
- Is only visible when KPI data is loaded

### 2.3 Technical Specifications

#### 2.3.1 API Endpoint

**REQ-PK-TECH-001:** The system SHALL call the backend API endpoint `GET /segment_insights` with query parameters:
- `segment_by`: String (Geography/Industry/PolicySize/RiskRating)
- `min_premium`: Float (minimum earned premium filter)

**REQ-PK-TECH-002:** The API call SHALL have a timeout of 10 seconds.

#### 2.3.2 Response Format

**REQ-PK-TECH-003:** The API SHALL return a JSON response with the following structure:

```json
{
  "segment_kpis": [
    {
      "Geography|Industry|PolicySize|RiskRating": "segment_value",
      "EarnedPremium": amount,
      "IncurredLoss": amount,
      "PaidLoss": amount,
      "LossRatio": percentage,
      "PaidLossRatio": percentage,
      "Frequency": rate,
      "Severity": amount,
      "PurePremium": amount,
      "AvgPremium": amount,
      "TotalExposure": units,
      "PolicyCount": count,
      "ClaimCount": count
    }
  ],
  "overall_kpis": {
    "total_earned_premium": amount,
    "total_incurred_loss": amount,
    "total_paid_loss": amount,
    "total_exposure": units,
    "policy_count": count,
    "claim_count": count,
    "loss_ratio": percentage,
    "paid_loss_ratio": percentage,
    "frequency": rate,
    "severity": amount,
    "pure_premium": amount,
    "avg_premium_per_policy": amount
  }
}
```

#### 2.3.3 KPI Calculation Formulas

**REQ-PK-TECH-004:** The system SHALL calculate Loss Ratio as:
```
Loss Ratio = (Incurred Loss / Earned Premium) × 100
```

**REQ-PK-TECH-005:** The system SHALL calculate Paid Loss Ratio as:
```
Paid Loss Ratio = (Paid Loss / Earned Premium) × 100
```

**REQ-PK-TECH-006:** The system SHALL calculate Frequency as:
```
Frequency = (Claim Count / Total Exposure) × 100
```
*Note: Frequency represents claims per 100 exposure units*

**REQ-PK-TECH-007:** The system SHALL calculate Severity as:
```
Severity = Incurred Loss / Claim Count
```

**REQ-PK-TECH-008:** The system SHALL calculate Pure Premium as:
```
Pure Premium = Incurred Loss / Total Exposure
```

**REQ-PK-TECH-009:** The system SHALL calculate Average Premium as:
```
Average Premium = Earned Premium / Policy Count
```

**REQ-PK-TECH-010:** All KPI calculations SHALL handle division by zero by returning 0.

**REQ-PK-TECH-011:** Segments with no claims SHALL have:
- Incurred Loss = 0
- Paid Loss = 0
- Claim Count = 0
- Loss Ratio = 0%
- Frequency = 0

### 2.4 Data Requirements

**REQ-PK-DATA-001:** The system SHALL use policies data with required fields:
- `PolicyID`: Unique policy identifier
- `Geography`: Geographic region
- `Industry`: Industry sector
- `PolicySize`: Policy size category
- `RiskRating`: COPE-based risk rating
- `AnnualPremium`: Annual premium amount
- `ExposureUnits`: Building value in $100K units

**REQ-PK-DATA-002:** The system SHALL use exposure data with required fields:
- `PolicyID`: Policy identifier
- `Period`: Time period (month)
- `EarnedPremium`: Earned premium for period
- `ExposureUnits`: Exposure units for period
- `Geography`, `Industry`, `PolicySize`, `RiskRating`: Segmentation fields

**REQ-PK-DATA-003:** The system SHALL use claims data as defined in REQ-LD-DATA-001.

### 2.5 Acceptance Criteria

**Test Case PK-TC-001: Load KPIs by Geography**
- GIVEN the user is on the Pricing & KPIs Dashboard
- WHEN the user selects "Geography" and clicks "Load KPI Data"
- THEN the system SHALL display:
  - Overall portfolio metrics
  - Segment KPI table with Geography as the segment column
  - Loss ratio bar chart by geography
  - Premium distribution pie chart
  - Frequency vs Severity scatter plot
  - Top/Bottom performers

**Test Case PK-TC-002: Apply Minimum Premium Filter**
- GIVEN KPI data is loaded for Geography
- WHEN the user sets minimum premium to $100,000 and reloads
- THEN the system SHALL exclude segments with earned premium < $100,000
- AND all visualizations SHALL update accordingly

**Test Case PK-TC-003: Loss Ratio Calculation**
- GIVEN a segment with $1,000,000 earned premium and $650,000 incurred loss
- WHEN KPIs are calculated
- THEN Loss Ratio SHALL equal 65.00%

**Test Case PK-TC-004: Frequency Calculation**
- GIVEN a segment with 5 claims and 250 exposure units
- WHEN frequency is calculated
- THEN Frequency SHALL equal 2.0000 (5/250 × 100)

**Test Case PK-TC-005: CSV Export**
- GIVEN KPI data is loaded
- WHEN the user clicks "Download KPI Data (CSV)"
- THEN a CSV file SHALL be downloaded
- AND the file SHALL contain all segment KPI columns
- AND the filename SHALL be "segment_kpis_{segment_by}.csv"

**Test Case PK-TC-006: Top Performers Display**
- GIVEN segments are loaded with varying loss ratios
- WHEN the dashboard displays top performers
- THEN the 5 segments with lowest loss ratios SHALL be shown
- AND they SHALL be sorted by loss ratio ascending

**Test Case PK-TC-007: Zero Claims Segment**
- GIVEN a segment with policies but no claims
- WHEN KPIs are calculated
- THEN Loss Ratio SHALL be 0%
- AND Frequency SHALL be 0.0000
- AND Severity SHALL be $0

---

## Tab 3: Risk Prediction & Scoring

### 3.1 Functional Overview

The Risk Prediction & Scoring dashboard shall provide ML-powered predictions for expected loss ratio and claim severity based on policy characteristics, enabling data-driven underwriting and pricing decisions.

### 3.2 User Requirements

#### 3.2.1 Input Form

**REQ-RP-001:** The system SHALL provide input fields for the following policy characteristics:

**Geographic Controls:**
- **Geography:** Dropdown with options: Northeast, Southeast, Midwest, Southwest, West, Northwest
- **Industry:** Dropdown with options: Manufacturing, Retail, Office, Warehouse, Healthcare, Education, Hospitality, Technology

**Risk Controls:**
- **Policy Size:** Dropdown with options: Small, Medium, Large, Enterprise
- **Risk Rating (COPE):** Slider with:
  - Minimum: 1.0
  - Maximum: 10.0
  - Default: 5.0
  - Step: 0.5
  - Help text: "Composite COPE-based risk score (1=low risk, 10=high risk)"

**Financial Controls:**
- **Exposure Units:** Number input with:
  - Minimum: 1.0
  - Maximum: 10,000.0
  - Default: 50.0
  - Step: 10.0
  - Help text: "Building value in $100K units"

- **Annual Premium:** Number input with:
  - Minimum: $1,000
  - Maximum: $10,000,000
  - Default: $25,000
  - Step: $1,000
  - Help text: "Annual premium amount"

**REQ-RP-002:** All input fields SHALL have descriptive labels and help tooltips.

#### 3.2.2 Prediction Buttons

**REQ-RP-003:** The system SHALL provide three prediction buttons:
- **"Predict Loss Ratio"** (primary button): Generates loss ratio prediction only
- **"Predict Severity"** (secondary button): Generates severity prediction only
- **"Predict Both"** (secondary button): Generates both predictions

**REQ-RP-004:** Each button SHALL be full-width within its column.

**REQ-RP-005:** The system SHALL display a loading spinner with appropriate text while generating predictions.

#### 3.2.3 Loss Ratio Prediction Display

**REQ-RP-006:** When loss ratio prediction is generated, the system SHALL display:
- **Gauge Chart:** Visual indicator showing:
  - Predicted loss ratio value
  - Range: 0-150%
  - Color zones:
    - 0-50%: Light green (favorable)
    - 50-70%: Yellow (acceptable)
    - 70-150%: Light coral (elevated)
  - Target threshold line at 65% (red)
  - Delta vs 65% target
  - Title: "Predicted Loss Ratio (%)"

**REQ-RP-007:** The system SHALL display metrics:
- **Predicted LR:** Loss ratio formatted to 2 decimals with "%" suffix
- **Confidence Interval:** Range formatted as "X.X% - X.X%" (95% confidence)

**REQ-RP-008:** The system SHALL display an interpretation message:
- **If LR < 55%:** Green success box: "Favorable Risk - Loss ratio well below target"
- **If 55% ≤ LR < 70%:** Blue info box: "Acceptable Risk - Loss ratio near target range"
- **If LR ≥ 70%:** Yellow warning box: "Elevated Risk - Loss ratio above target, consider higher premium or declining"

**REQ-RP-009:** If the model is not loaded, the system SHALL display an info message indicating that default estimates are being used.

#### 3.2.4 Severity Prediction Display

**REQ-RP-010:** When severity prediction is generated, the system SHALL display:
- **Bar Chart:** Three bars showing:
  - Low Estimate (light blue)
  - Predicted (dark blue)
  - High Estimate (light coral)
  - Values displayed above each bar
  - Y-axis: Amount in dollars
  - Title: "Expected Claim Severity"

**REQ-RP-011:** The system SHALL display metrics:
- **Predicted Severity:** Amount formatted as currency with no decimals
- **Uncertainty:** Displayed as "±X.X%" representing half the confidence range

**REQ-RP-012:** If the model is not loaded, the system SHALL display an info message.

#### 3.2.5 Risk Summary

**REQ-RP-013:** When both predictions are available, the system SHALL display a Risk Summary with:
- **Expected Loss:** Calculated as Annual Premium × (Predicted LR / 100)
- **Expected Profit:** Calculated as Annual Premium - Expected Loss
- **Profit Margin:** Calculated as (Expected Profit / Annual Premium) × 100
- **Composite Risk Score:** Calculated as min(10, Risk Rating × (Predicted LR / 65)), scale 1-10

**REQ-RP-014:** All Risk Summary metrics SHALL be formatted appropriately:
- Dollar amounts: Currency format with thousand separators
- Percentages: One decimal place with "%" suffix
- Risk score: One decimal with "/10" suffix

#### 3.2.6 Additional Information

**REQ-RP-015:** The system SHALL provide an expandable "View Input Summary" section displaying all input parameters in JSON format.

**REQ-RP-016:** The system SHALL provide an expandable "Model Feature Importance" section explaining:
- Key factors influencing predictions (ranked by importance)
- Model type: LightGBM gradient boosting
- Training data source

**REQ-RP-017:** The system SHALL provide an expandable "About the Prediction Models" section explaining:
- Loss ratio model details
- Severity model details
- Usage notes and confidence interval interpretation

### 3.3 Technical Specifications

#### 3.3.1 API Endpoints

**REQ-RP-TECH-001:** The system SHALL call `POST /predict/loss_ratio` for loss ratio predictions with JSON body:

```json
{
  "geography": "string",
  "industry": "string",
  "policy_size": "string",
  "risk_rating": float,
  "exposure_units": float,
  "annual_premium": float
}
```

**REQ-RP-TECH-002:** The system SHALL call `POST /predict/severity` for severity predictions with the same JSON body format.

**REQ-RP-TECH-003:** Both API calls SHALL have a timeout of 10 seconds.

#### 3.3.2 Feature Encoding

**REQ-RP-TECH-004:** The system SHALL encode categorical features as follows:

**Geography Encoding:**
```
Northeast: 0, Southeast: 1, Midwest: 2, Southwest: 3, West: 4, Northwest: 5
```

**Industry Encoding:**
```
Manufacturing: 0, Retail: 1, Office: 2, Warehouse: 3,
Healthcare: 4, Education: 5, Hospitality: 6, Technology: 7
```

**Policy Size Encoding:**
```
Small: 0, Medium: 1, Large: 2, Enterprise: 3
```

**REQ-RP-TECH-005:** The feature vector SHALL contain the following fields in order:
1. RiskRating (float)
2. Geography (integer)
3. Industry (integer)
4. PolicySize (integer)
5. ExposureUnits (float)
6. AnnualPremium (float)

#### 3.3.3 Model Specifications

**REQ-RP-TECH-006:** The system SHALL use LightGBM gradient boosting models for predictions.

**REQ-RP-TECH-007:** Models SHALL be loaded from the `/models` directory:
- Loss Ratio model: `models/lr_model.pkl`
- Severity model: `models/severity_model.pkl`

**REQ-RP-TECH-008:** If models are not available, the system SHALL use fallback logic:

**Loss Ratio Fallback:**
- Return default: 65.0%
- Confidence interval: [50.0%, 80.0%]
- Set `model_loaded: false`

**Severity Fallback:**
- Base on policy size:
  - Small: $50,000
  - Medium: $100,000
  - Large: $250,000
  - Enterprise: $500,000
- Confidence interval: [Base × 0.7, Base × 1.3]
- Set `model_loaded: false`

#### 3.3.4 Confidence Intervals

**REQ-RP-TECH-009:** Loss Ratio confidence interval SHALL be calculated as:
```
Lower Bound = max(0, prediction - 15)
Upper Bound = min(100, prediction + 15)
```

**REQ-RP-TECH-010:** Severity confidence interval SHALL be calculated as:
```
Lower Bound = max(0, prediction × 0.7)
Upper Bound = prediction × 1.3
```

#### 3.3.5 Response Format

**REQ-RP-TECH-011:** Loss ratio prediction response SHALL have the format:

```json
{
  "predicted_loss_ratio": float,
  "confidence_interval": [lower, upper],
  "model_loaded": boolean,
  "input_features": {input_dict},
  "message": "string (optional)"
}
```

**REQ-RP-TECH-012:** Severity prediction response SHALL have the same format with `predicted_severity` instead of `predicted_loss_ratio`.

### 3.4 Data Requirements

**REQ-RP-DATA-001:** Model training data SHALL include historical policy and claims data with the fields specified in REQ-PK-DATA-001 and REQ-LD-DATA-001.

**REQ-RP-DATA-002:** Models SHALL be retrained periodically (recommended: quarterly) using updated historical data.

### 3.5 Acceptance Criteria

**Test Case RP-TC-001: Predict Loss Ratio**
- GIVEN the user enters valid policy characteristics
- WHEN the user clicks "Predict Loss Ratio"
- THEN the system SHALL display:
  - Gauge chart with predicted value
  - Predicted LR metric
  - Confidence interval metric
  - Interpretation message based on predicted value
- AND the prediction SHALL complete within 10 seconds

**Test Case RP-TC-002: Predict Severity**
- GIVEN the user enters valid policy characteristics
- WHEN the user clicks "Predict Severity"
- THEN the system SHALL display:
  - Bar chart with low/predicted/high estimates
  - Predicted severity metric
  - Uncertainty metric
- AND the prediction SHALL complete within 10 seconds

**Test Case RP-TC-003: Predict Both**
- GIVEN the user enters valid policy characteristics
- WHEN the user clicks "Predict Both"
- THEN the system SHALL display both loss ratio and severity predictions
- AND a Risk Summary section with 4 calculated metrics

**Test Case RP-TC-004: Model Not Loaded**
- GIVEN the ML models are not available in the models directory
- WHEN the user requests a prediction
- THEN the system SHALL return fallback predictions
- AND display a message indicating "Model not loaded - using default estimate"
- AND NOT throw an error

**Test Case RP-TC-005: High Risk Policy**
- GIVEN a policy with Risk Rating = 8.0 in Manufacturing, West region
- WHEN loss ratio is predicted
- THEN the predicted LR SHALL likely be > 70%
- AND the interpretation SHALL show "Elevated Risk"
- AND the recommendation SHALL mention higher premium or declining

**Test Case RP-TC-006: Feature Encoding**
- GIVEN Geography = "Northeast", Industry = "Healthcare", PolicySize = "Large"
- WHEN features are prepared for prediction
- THEN Geography SHALL encode to 0
- AND Industry SHALL encode to 4
- AND PolicySize SHALL encode to 2

**Test Case RP-TC-007: Risk Summary Calculation**
- GIVEN Annual Premium = $100,000, Predicted LR = 60%, Risk Rating = 5.0
- WHEN Risk Summary is calculated
- THEN Expected Loss SHALL equal $60,000
- AND Expected Profit SHALL equal $40,000
- AND Profit Margin SHALL equal 40.0%
- AND Composite Risk Score SHALL equal min(10, 5.0 × (60/65)) = 4.6

---

## Tab 4: GenAI Insights & Explanations

### 4.1 Functional Overview

The GenAI Insights & Explanations dashboard shall provide natural language explanations and insights for actuarial data using OpenAI's GPT-3.5-turbo model, enabling users to ask questions and receive expert-level explanations.

### 4.2 User Requirements

#### 4.2.1 Analysis Mode Selection

**REQ-GI-001:** The system SHALL provide four analysis modes selectable via radio buttons:
- Question & Answer
- Loss Ratio Analysis
- Trend Explanation
- Risk Rating Explanation

**REQ-GI-002:** Mode selection SHALL be displayed horizontally.

**REQ-GI-003:** Changing the mode SHALL update the input form and controls.

#### 4.2.2 Question & Answer Mode

**REQ-GI-004:** In Q&A mode, the system SHALL provide:
- **Question Text Area:**
  - Multi-line input (height: 100px)
  - Placeholder: "Example: What factors are driving the high loss ratio in the Manufacturing sector?"
  - Help text: "Ask any question about actuarial metrics, trends, or insights"

**REQ-GI-005:** The system SHALL display sample questions:
- What is causing the loss ratio trend?
- Which segments should we focus on?
- How does geography impact severity?
- Should we adjust pricing in the West region?
- What drives claim frequency in Manufacturing?

**REQ-GI-006:** The system SHALL provide a "Get Answer" button (primary).

**REQ-GI-007:** When the user clicks "Get Answer":
- IF question is empty, display warning "Please enter a question"
- ELSE submit question to backend with context data
- Display loading spinner: "Analyzing your question..."

**REQ-GI-008:** Upon successful response, the system SHALL:
- Display success message: "Analysis complete!"
- Display answer in an info box under "Answer:" heading
- Add question and answer to chat history

#### 4.2.3 Loss Ratio Analysis Mode

**REQ-GI-009:** In Loss Ratio Analysis mode, the system SHALL provide inputs:
- **Segment Name:** Text input, default "Northeast"
- **Actual Loss Ratio (%):** Number input, default 75.0, range 0-200, step 5.0
- **Benchmark/Target (%):** Number input, default 65.0, range 0-200, step 5.0

**REQ-GI-010:** The system SHALL provide an expandable "Add Additional Context" section with:
- **Number of Claims:** Number input, default 25, min 0
- **Earned Premium ($):** Number input, default $1,000,000, min $0
- **Time Period:** Dropdown (Current Year, YTD, Last 12 Months, All Time)

**REQ-GI-011:** The system SHALL provide an "Explain Loss Ratio" button (primary).

**REQ-GI-012:** Upon receiving explanation, the system SHALL:
- Calculate variance = Actual LR - Benchmark
- IF variance > 0: Display error box "Loss ratio is **X.X points above** benchmark"
- IF variance ≤ 0: Display success box "Loss ratio is **X.X points below** benchmark"
- Display explanation in info box under "Analysis:" heading

#### 4.2.4 Trend Explanation Mode

**REQ-GI-013:** In Trend Explanation mode, the system SHALL provide:
- **Metric Selector:** Dropdown with options:
  - Loss Ratio
  - Claim Frequency
  - Severity
  - Premium Growth
  - Claim Count

- **Trend Direction:** Radio buttons (horizontal):
  - Increasing
  - Decreasing
  - Neutral

**REQ-GI-014:** The system SHALL provide 4 number inputs for trend data:
- **Period 1:** Default 60.0, help "Oldest period"
- **Period 2:** Default 65.0
- **Period 3:** Default 70.0
- **Period 4 (Latest):** Default 75.0, help "Most recent"

**REQ-GI-015:** The system SHALL provide an "Explain Trend" button (primary).

**REQ-GI-016:** The system SHALL calculate and include in the request:
- Change: Period 4 - Period 1
- Average: (Period 1 + Period 2 + Period 3 + Period 4) / 4

**REQ-GI-017:** Upon receiving explanation, the system SHALL:
- Display explanation under "Trend Analysis:" heading
- Provide expandable "View Trend Data" section showing the calculated trend_data object in JSON format

#### 4.2.5 Risk Rating Explanation Mode

**REQ-GI-018:** In Risk Rating Explanation mode, the system SHALL provide:
- **Risk Rating:** Slider, range 1.0-10.0, default 6.5, step 0.5
- **Geography:** Dropdown (same options as REQ-RP-001)
- **Industry:** Dropdown (same options as REQ-RP-001)

**REQ-GI-019:** The system SHALL provide an "Explain Rating" button (primary).

**REQ-GI-020:** Upon receiving explanation, the system SHALL:
- Display risk level indicator based on rating:
  - Rating ≤ 3.5: Green success "Low Risk (Rating: X/10)"
  - 3.5 < Rating ≤ 6.5: Blue info "Moderate Risk (Rating: X/10)"
  - Rating > 6.5: Yellow warning "High Risk (Rating: X/10)"
- Display explanation under "Risk Assessment:" heading
- Provide expandable "COPE Framework Reference" with framework details

#### 4.2.6 Chat History

**REQ-GI-021:** The system SHALL maintain a conversation history for Q&A mode.

**REQ-GI-022:** The system SHALL display the last 5 Q&A exchanges in expandable sections.

**REQ-GI-023:** Each history item SHALL show:
- Question (truncated to 80 characters in header)
- Full question and answer when expanded

**REQ-GI-024:** The most recent exchange SHALL be expanded by default.

**REQ-GI-025:** The system SHALL provide a "Clear History" button that:
- Empties the chat history
- Refreshes the page

#### 4.2.7 Information Sections

**REQ-GI-026:** The system SHALL provide an expandable "About GenAI Insights" section explaining:
- How the feature works
- Capabilities of each mode
- Model information (GPT-3.5-turbo, temperature, max tokens)
- Privacy & security considerations
- Best practices

**REQ-GI-027:** The system SHALL provide an expandable "Sample Use Cases" section with examples for:
- Underwriting decisions
- Pricing adjustments
- Portfolio management
- Claims analysis

### 4.3 Technical Specifications

#### 4.3.1 API Endpoint

**REQ-GI-TECH-001:** The system SHALL call `POST /explain` for all explanation types with JSON body:

```json
{
  "explanation_type": "question|loss_ratio|trend|cope_rating",
  "data": {
    // Type-specific fields
  }
}
```

**REQ-GI-TECH-002:** API calls SHALL have a timeout of 30 seconds (longer than other endpoints due to LLM latency).

#### 4.3.2 Request Formats

**REQ-GI-TECH-003:** Question & Answer request data:

```json
{
  "explanation_type": "question",
  "data": {
    "question": "string",
    "context_data": {
      "portfolio": "Commercial Property",
      "policies": 1000,
      "overall_lr": 12.0
    }
  }
}
```

**REQ-GI-TECH-004:** Loss Ratio Analysis request data:

```json
{
  "explanation_type": "loss_ratio",
  "data": {
    "segment": "string",
    "loss_ratio": float,
    "benchmark": float,
    "context": {
      "claim_count": int,
      "earned_premium": float,
      "time_period": "string"
    }
  }
}
```

**REQ-GI-TECH-005:** Trend Explanation request data:

```json
{
  "explanation_type": "trend",
  "data": {
    "metric_name": "string",
    "trend_data": {
      "Period_1": float,
      "Period_2": float,
      "Period_3": float,
      "Period_4_Latest": float,
      "change": float,
      "avg": float
    },
    "trend_direction": "increasing|decreasing|neutral"
  }
}
```

**REQ-GI-TECH-006:** Risk Rating Explanation request data:

```json
{
  "explanation_type": "cope_rating",
  "data": {
    "risk_rating": float,
    "geography": "string",
    "industry": "string"
  }
}
```

#### 4.3.3 OpenAI Integration

**REQ-GI-TECH-007:** The system SHALL use OpenAI GPT-3.5-turbo model.

**REQ-GI-TECH-008:** All prompts SHALL:
- Use system role: "You are an expert actuarial analyst"
- Use temperature: 0.7
- Limit max tokens based on explanation type:
  - Question & Answer: 400 tokens
  - Loss Ratio, Trend, COPE: 300 tokens

**REQ-GI-TECH-009:** The system SHALL read the OpenAI API key from the environment variable `OPENAI_API_KEY`.

**REQ-GI-TECH-010:** Prompts SHALL instruct the model to:
- Provide concise explanations (2-4 sentences)
- Use professional but accessible tone
- Focus on actionable insights
- Reference specific data points when available

#### 4.3.4 Response Format

**REQ-GI-TECH-011:** The API SHALL return:

```json
{
  "explanation": "string (generated explanation)",
  "model": "gpt-3.5-turbo",
  "tokens_used": int (optional)
}
```

#### 4.3.5 Error Handling

**REQ-GI-TECH-012:** If OpenAI API key is not configured, the system SHALL return an error message.

**REQ-GI-TECH-013:** If OpenAI API call fails, the system SHALL:
- Display error message to user
- NOT crash or freeze the application
- Log error details for debugging

**REQ-GI-TECH-014:** If API timeout occurs (30 seconds), display message "Request timed out. Please try again."

### 4.4 Data Requirements

**REQ-GI-DATA-001:** Context data for questions MAY include portfolio-level metrics from other tabs.

**REQ-GI-DATA-002:** No personally identifiable information (PII) or sensitive policy data SHALL be sent to OpenAI.

**REQ-GI-DATA-003:** Only aggregated metrics and non-sensitive segment names SHALL be included in prompts.

### 4.5 Acceptance Criteria

**Test Case GI-TC-001: Ask Question**
- GIVEN the user is in Question & Answer mode
- WHEN the user enters "What factors drive loss ratio?" and clicks "Get Answer"
- THEN the system SHALL send the question to OpenAI
- AND display the generated answer within 30 seconds
- AND add the Q&A to chat history

**Test Case GI-TC-002: Empty Question Validation**
- GIVEN the user is in Question & Answer mode
- WHEN the user clicks "Get Answer" with an empty question
- THEN the system SHALL display warning "Please enter a question"
- AND NOT call the API

**Test Case GI-TC-003: Loss Ratio Above Benchmark**
- GIVEN the user enters Actual LR = 80%, Benchmark = 65%
- WHEN the user clicks "Explain Loss Ratio"
- THEN the system SHALL display error box "Loss ratio is **15.0 points above** benchmark"
- AND provide an explanation of the variance

**Test Case GI-TC-004: Loss Ratio Below Benchmark**
- GIVEN the user enters Actual LR = 55%, Benchmark = 65%
- WHEN the user clicks "Explain Loss Ratio"
- THEN the system SHALL display success box "Loss ratio is **10.0 points below** benchmark"

**Test Case GI-TC-005: Trend Calculation**
- GIVEN Period 1 = 60, Period 2 = 65, Period 3 = 70, Period 4 = 75
- WHEN "Explain Trend" is clicked
- THEN the request SHALL include:
  - change = 15.0 (75 - 60)
  - avg = 67.5 ((60+65+70+75)/4)

**Test Case GI-TC-006: Risk Rating Interpretation**
- GIVEN Risk Rating = 2.5
- WHEN explanation is received
- THEN the system SHALL display green "Low Risk (Rating: 2.5/10)"

**Test Case GI-TC-007: Chat History Limit**
- GIVEN the user has asked 10 questions
- WHEN chat history is displayed
- THEN only the last 5 Q&A exchanges SHALL be shown

**Test Case GI-TC-008: Clear History**
- GIVEN chat history contains 3 items
- WHEN the user clicks "Clear History"
- THEN chat history SHALL be empty
- AND the page SHALL refresh

**Test Case GI-TC-009: API Error Handling**
- GIVEN the OpenAI API returns an error
- WHEN a user requests an explanation
- THEN the system SHALL display "Error: {error message}"
- AND NOT crash the application

**Test Case GI-TC-010: Explanation Quality**
- GIVEN any valid explanation request
- WHEN explanation is generated
- THEN it SHALL be 2-4 sentences
- AND use professional language
- AND provide actionable insights
- AND reference specific data when available

---

## Data Models & Schemas

### 5.1 Claims Data Schema

**Table:** `claims.csv`

| Field | Type | Description | Constraints | Example |
|-------|------|-------------|-------------|---------|
| ClaimID | String | Unique claim identifier | Primary key, not null | CLM000001 |
| PolicyID | String | Associated policy ID | Foreign key to policies, not null | POL000370 |
| LossDate | DateTime | Date loss occurred | Not null, ≤ ReportDate | 2024-10-06 |
| ReportDate | DateTime | Date claim reported | Not null, ≥ LossDate | 2024-12-30 |
| Geography | String | Geographic region | Enum: Northeast, Southeast, Midwest, Southwest, West, Northwest | Midwest |
| Industry | String | Industry sector | Enum: Manufacturing, Retail, Office, Warehouse, Healthcare, Education, Hospitality, Technology | Warehouse |
| PolicySize | String | Policy size category | Enum: Small, Medium, Large, Enterprise | Large |
| RiskRating | Float | COPE-based risk rating | Range: 1.0-10.0 | 3.88 |
| IncurredAmount | Float | Total incurred loss | ≥ 0, ≥ PaidAmount | 133881.81 |
| PaidAmount | Float | Total paid loss | ≥ 0, ≤ IncurredAmount | 99281.70 |
| ClaimStatus | String | Current claim status | Open - Developing, Open - Developed, Closed | Open - Developing |

**Data Integrity Rules:**
- `LossDate` ≤ `ReportDate`
- `PaidAmount` ≤ `IncurredAmount`
- `ClaimID` must be unique
- All monetary amounts must be ≥ 0

### 5.2 Policies Data Schema

**Table:** `policies.csv`

| Field | Type | Description | Constraints | Example |
|-------|------|-------------|-------------|---------|
| PolicyID | String | Unique policy identifier | Primary key, not null | POL000001 |
| EffectiveDate | DateTime | Policy effective date | Not null | 2024-05-10 |
| Geography | String | Geographic region | Same enum as claims | Northeast |
| Industry | String | Industry sector | Same enum as claims | Education |
| PolicySize | String | Policy size category | Same enum as claims | Medium |
| RiskRating | Float | COPE-based risk rating | Range: 1.0-10.0 | 4.25 |
| AnnualPremium | Float | Annual premium amount | > 0 | 30384.37 |
| ExposureUnits | Float | Building value in $100K units | > 0 | 53.02 |

**Data Integrity Rules:**
- `PolicyID` must be unique
- `AnnualPremium` > 0
- `ExposureUnits` > 0
- `RiskRating` between 1.0 and 10.0

### 5.3 Exposure Data Schema

**Table:** `exposure.csv`

| Field | Type | Description | Constraints | Example |
|-------|------|-------------|-------------|---------|
| PolicyID | String | Policy identifier | Foreign key to policies, not null | POL000001 |
| Period | String | Time period (YYYY-MM format) | Not null, valid date format | 2024-05 |
| EarnedPremium | Float | Earned premium for period | ≥ 0 | 2532.03 |
| ExposureUnits | Float | Exposure units for period | ≥ 0 | 51.21 |
| Geography | String | Geographic region | Same enum as claims | Northeast |
| Industry | String | Industry sector | Same enum as claims | Education |
| PolicySize | String | Policy size category | Same enum as claims | Medium |
| RiskRating | Float | COPE-based risk rating | Range: 1.0-10.0 | 4.25 |

**Data Integrity Rules:**
- `(PolicyID, Period)` combination should be unique
- All monetary amounts and units ≥ 0
- Period must be valid YYYY-MM format
- Dimension fields (Geography, Industry, etc.) must match the associated policy

### 5.4 Data Relationships

```
policies (1) ----< (many) exposure
   |
   |
   +----< (many) claims
```

**REQ-DATA-001:** Each claim MUST reference a valid PolicyID in the policies table.

**REQ-DATA-002:** Each exposure record MUST reference a valid PolicyID in the policies table.

**REQ-DATA-003:** A policy MAY have zero or more claims.

**REQ-DATA-004:** A policy SHOULD have at least one exposure record.

### 5.5 Enumeration Values

**Geography:**
```
Northeast, Southeast, Midwest, Southwest, West, Northwest
```

**Industry:**
```
Manufacturing, Retail, Office, Warehouse, Healthcare, Education, Hospitality, Technology
```

**Policy Size:**
```
Small, Medium, Large, Enterprise
```

**Claim Status:**
```
Open - Developing, Open - Developed, Closed
```

### 5.6 Calculated Fields

The following fields are calculated and not stored:

**Development Months:**
```
DevMonths = (ReportDate.Year - LossDate.Year) × 12 + (ReportDate.Month - LossDate.Month)
```

**Accident Year:**
```
AccidentYear = LossDate.Year
```

**Loss Ratio:**
```
LossRatio = (IncurredAmount / EarnedPremium) × 100
```

**Frequency:**
```
Frequency = (ClaimCount / ExposureUnits) × 100
```

**Severity:**
```
Severity = IncurredAmount / ClaimCount
```

---

## Non-Functional Requirements

### 6.1 Performance Requirements

**REQ-NFR-001:** The system SHALL load triangle data within 10 seconds for up to 10,000 claims.

**REQ-NFR-002:** The system SHALL load segment KPIs within 10 seconds for up to 1,000 policies.

**REQ-NFR-003:** ML predictions SHALL complete within 10 seconds.

**REQ-NFR-004:** GenAI explanations SHALL complete within 30 seconds.

**REQ-NFR-005:** Dashboard visualizations SHALL render within 2 seconds after data is loaded.

**REQ-NFR-006:** The system SHALL support concurrent usage by up to 10 users without performance degradation.

### 6.2 Usability Requirements

**REQ-NFR-007:** The user interface SHALL be responsive and work on desktop browsers with minimum resolution 1280×720.

**REQ-NFR-008:** All interactive elements (buttons, dropdowns, sliders) SHALL provide visual feedback on hover and click.

**REQ-NFR-009:** Error messages SHALL be clear, specific, and actionable.

**REQ-NFR-010:** All input fields SHALL have descriptive labels and help text.

**REQ-NFR-011:** Monetary values SHALL be formatted with thousand separators and appropriate currency symbols.

**REQ-NFR-012:** Percentages SHALL be formatted with "%" suffix and appropriate decimal places.

### 6.3 Reliability Requirements

**REQ-NFR-013:** The system SHALL handle API connection failures gracefully without crashing.

**REQ-NFR-014:** The system SHALL validate all user inputs before submitting to backend.

**REQ-NFR-015:** If backend services are unavailable, the system SHALL display appropriate error messages and allow users to retry.

**REQ-NFR-016:** Session state SHALL persist across page refreshes for loaded data.

### 6.4 Security Requirements

**REQ-NFR-017:** The OpenAI API key SHALL be stored as an environment variable and NOT hardcoded.

**REQ-NFR-018:** No personally identifiable information (PII) SHALL be sent to external APIs (OpenAI).

**REQ-NFR-019:** API endpoints SHALL validate input parameters to prevent injection attacks.

**REQ-NFR-020:** Sensitive data (API keys, credentials) SHALL NOT be logged or displayed in error messages.

### 6.5 Maintainability Requirements

**REQ-NFR-021:** The system SHALL use modular service architecture with separate services for:
- Loss triangle calculations
- Segment KPI calculations
- ML predictions
- GenAI explanations

**REQ-NFR-022:** All backend services SHALL have unit tests with minimum 70% code coverage.

**REQ-NFR-023:** API endpoints SHALL follow RESTful conventions.

**REQ-NFR-024:** Code SHALL follow PEP 8 style guidelines for Python.

### 6.6 Scalability Requirements

**REQ-NFR-025:** The system SHALL be deployable via Docker containers for easy scaling.

**REQ-NFR-026:** Backend and frontend SHALL run in separate containers for independent scaling.

**REQ-NFR-027:** The system architecture SHALL support horizontal scaling by adding container instances.

### 6.7 Compatibility Requirements

**REQ-NFR-028:** The system SHALL run on the following platforms:
- macOS (Darwin)
- Linux
- Windows (via Docker)

**REQ-NFR-029:** The system SHALL be compatible with modern browsers:
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

### 6.8 Documentation Requirements

**REQ-NFR-030:** All API endpoints SHALL be documented with:
- Endpoint URL and HTTP method
- Request parameters and body schema
- Response schema
- Example requests and responses
- Possible error codes

**REQ-NFR-031:** All Python functions SHALL have docstrings explaining:
- Purpose
- Parameters
- Return values
- Exceptions raised

**REQ-NFR-032:** User documentation SHALL be provided for:
- Setup and installation
- Using each dashboard tab
- Interpreting results
- Troubleshooting common issues

---

## Glossary

### Actuarial Terms

**Accident Year:** The calendar year in which a loss occurred.

**Age-to-Age Factor (Development Factor):** Ratio of cumulative losses at one development age to cumulative losses at an earlier age.

**Chain-Ladder Method:** Actuarial technique for projecting ultimate losses by applying age-to-age development factors.

**Claim Frequency:** Number of claims per unit of exposure, typically expressed per 100 exposure units.

**Claim Severity:** Average cost per claim, calculated as total incurred losses divided by claim count.

**COPE Rating:** Risk assessment framework evaluating Construction, Occupancy, Protection, and Exposure factors.

**Cumulative Triangle:** Loss triangle showing total losses reported to date for each accident year and development period.

**Development Month:** Number of months elapsed since the accident date.

**Earned Premium:** Portion of written premium that has been "earned" through the passage of time.

**Exposure Units:** Measure of risk exposure, typically building value in $100,000 units for commercial property.

**IBNR (Incurred But Not Reported):** Estimated losses that have occurred but not yet been reported to the insurer.

**Incremental Triangle:** Loss triangle showing losses reported during each development period (not cumulative).

**Loss Ratio:** Incurred losses divided by earned premium, expressed as a percentage.

**Loss Triangle:** Tabular arrangement of loss data organized by accident year (rows) and development period (columns).

**Paid Loss Ratio:** Paid losses divided by earned premium, expressed as a percentage.

**Pure Premium:** Loss cost per exposure unit, calculated as incurred losses divided by exposure units.

**Ultimate Loss:** Projected total losses for an accident year when fully developed.

**Volume-Weighted Average:** Average calculated by weighting each value by its volume (e.g., premium or loss amount).

### Technical Terms

**API (Application Programming Interface):** Set of protocols for building and integrating application software.

**Confidence Interval:** Range of values within which the true value is expected to fall with a certain probability (e.g., 95%).

**Docker:** Platform for developing, shipping, and running applications in containers.

**FastAPI:** Modern Python web framework for building APIs.

**Feature Encoding:** Converting categorical variables into numeric format for machine learning models.

**GenAI:** Generative Artificial Intelligence, systems that can generate text, images, or other content.

**Heatmap:** Data visualization technique using colors to represent values in a matrix.

**LightGBM:** Gradient boosting framework for machine learning using tree-based algorithms.

**OpenAI GPT-3.5-turbo:** Large language model developed by OpenAI for natural language processing.

**Plotly:** Interactive graphing library for creating visualizations.

**RESTful API:** Web API that follows REST (Representational State Transfer) architectural principles.

**Streamlit:** Python framework for building data science web applications.

**Timeout:** Maximum time allowed for an operation to complete before being terminated.

---

**End of Functional Requirements Specification**

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-22 | Actuarial Insights Workbench Team | Initial release |

**Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Technical Lead | | | |
| QA Lead | | | |
| Stakeholder | | | |
