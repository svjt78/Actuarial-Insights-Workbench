# Pricing & Portfolio KPIs Tab - Formula Reference Guide

**Version**: 1.0
**Last Updated**: November 23, 2024
**Purpose**: Complete mathematical reference for all formulas used in the Pricing & Portfolio KPIs Dashboard

---

## Table of Contents

1. [Loss Ratio](#1-loss-ratio)
2. [Paid Loss Ratio](#2-paid-loss-ratio)
3. [Frequency (Claim Frequency)](#3-frequency-claim-frequency)
4. [Severity (Average Claim Amount)](#4-severity-average-claim-amount)
5. [Pure Premium](#5-pure-premium)
6. [Average Premium per Policy](#6-average-premium-per-policy)
7. [Total Earned Premium](#7-total-earned-premium)
8. [Total Incurred Loss](#8-total-incurred-loss)
9. [Total Paid Loss](#9-total-paid-loss)
10. [Total Exposure Units](#10-total-exposure-units)
11. [Policy Count](#11-policy-count)
12. [Claim Count](#12-claim-count)
13. [Frequency-Severity Relationship](#13-frequency-severity-relationship)
14. [Combined Ratio (Conceptual)](#14-combined-ratio-conceptual)
15. [Segment KPI Analysis Overview](#15-segment-kpi-analysis-overview)

---

## 1. Loss Ratio

### Purpose
Measure the percentage of premium dollars paid out as incurred losses. This is the primary profitability metric for insurance underwriting.

### Formula
```
Loss Ratio = (Incurred Loss / Earned Premium) × 100%
```

### Code Reference
[backend/services/segment_kpis.py:86](backend/services/segment_kpis.py#L86)

### Example Calculation

**Scenario - Geography Segment: "Northeast"**:
```
Incurred Loss = $650,000
Earned Premium = $1,000,000
```

**Calculation**:
```
Loss Ratio = ($650,000 / $1,000,000) × 100%
           = 0.65 × 100%
           = 65.0%
```

### Interpretation
- A loss ratio of 65% means that for every dollar of premium earned, $0.65 was paid out in losses
- The remaining $0.35 must cover expenses, commissions, and profit
- **Target Range**: 60-70% for most commercial property lines
- **Below 60%**: May indicate underpricing concerns or opportunity for competitive pricing
- **Above 70%**: May signal inadequate pricing or adverse selection

### Industry Benchmarks by Line

**Commercial Property**:
- **Target**: 60-70%
- **Excellent**: <60%
- **Acceptable**: 60-75%
- **Concerning**: >75%

**Casualty/Liability**:
- **Target**: 65-75%
- **Development**: Often increases over time as claims develop

### Business Applications
- **Pricing**: Adjust rates for segments with loss ratios outside target range
- **Underwriting**: Focus on segments with favorable loss ratios
- **Reinsurance**: High loss ratios may trigger reinsurance considerations
- **Portfolio Management**: Monitor trends to identify emerging issues

### Factors Affecting Loss Ratio
**Increases Loss Ratio**:
- Inadequate pricing/rating
- Catastrophic events
- Claims inflation
- Adverse selection
- Poor risk quality

**Decreases Loss Ratio**:
- Rate increases
- Improved underwriting
- Better risk selection
- Favorable claims experience
- Effective loss control

---

## 2. Paid Loss Ratio

### Purpose
Measure the percentage of premium dollars paid out in cash for claims, excluding reserves. Useful for cash flow analysis.

### Formula
```
Paid Loss Ratio = (Paid Loss / Earned Premium) × 100%
```

### Code Reference
[backend/services/segment_kpis.py:87](backend/services/segment_kpis.py#L87)

### Example Calculation

**Scenario**:
```
Paid Loss = $520,000
Earned Premium = $1,000,000
```

**Calculation**:
```
Paid Loss Ratio = ($520,000 / $1,000,000) × 100%
                = 0.52 × 100%
                = 52.0%
```

### Relationship to Loss Ratio

**Given**:
- Loss Ratio = 65.0%
- Paid Loss Ratio = 52.0%

**Implied Reserve Ratio**:
```
Reserve Ratio = Loss Ratio - Paid Loss Ratio
              = 65.0% - 52.0%
              = 13.0%
```

This means 13% of premium is held in case reserves for unpaid claims.

### Interpretation
- Paid loss ratio represents actual cash outflows
- Always lower than incurred loss ratio (unless negative reserve development)
- Difference represents outstanding case reserves and IBNR
- More relevant for cash flow management than profitability analysis

### Business Applications
- **Cash Flow Planning**: Predict future claim payment patterns
- **Investment Strategy**: Understand available funds for investment
- **Reinsurance Settlements**: Calculate cash calls on reinsurance treaties
- **Liquidity Management**: Ensure adequate liquid assets for claim payments

### Maturity Analysis

**Immature Accident Years** (0-12 months):
```
Paid Loss Ratio ≈ 30-50% of Loss Ratio
Example: Loss Ratio 65%, Paid Loss Ratio 35%
```

**Mature Accident Years** (24+ months):
```
Paid Loss Ratio ≈ 80-95% of Loss Ratio
Example: Loss Ratio 65%, Paid Loss Ratio 58%
```

---

## 3. Frequency (Claim Frequency)

### Purpose
Measure how often claims occur relative to the exposure base. One of two primary loss drivers (along with severity).

### Formula
```
Frequency = (Claim Count / Total Exposure Units) × 100
```

**Note**: Result is expressed as claims per 100 exposure units.

### Code Reference
[backend/services/segment_kpis.py:90](backend/services/segment_kpis.py#L90)

### Example Calculation

**Scenario - Industry Segment: "Manufacturing"**:
```
Claim Count = 45 claims
Total Exposure Units = 2,500 units
(Exposure typically measured in $100K of building value)
```

**Calculation**:
```
Frequency = (45 / 2,500) × 100
          = 0.018 × 100
          = 1.80 claims per 100 exposure units
```

### Interpretation
- A frequency of 1.80 means approximately 1.8 claims occur for every 100 units of exposure
- Equivalently: 1.8% of exposure units experience a claim
- Lower frequency is generally better (fewer claims)
- Must be considered alongside severity for full loss cost picture

### Industry Benchmarks

**Commercial Property**:
- **Low Hazard**: 0.5 - 1.0 claims per 100 units
- **Medium Hazard**: 1.0 - 2.0 claims per 100 units
- **High Hazard**: 2.0 - 4.0 claims per 100 units

**By Occupancy**:
- **Office Buildings**: 0.3 - 0.8
- **Retail**: 1.0 - 2.0
- **Manufacturing**: 1.5 - 3.0
- **Restaurants**: 2.5 - 5.0

### Factors Affecting Frequency

**Increases Frequency**:
- High-hazard occupancies
- Poor loss control
- Inadequate protection systems
- High-traffic locations
- Older buildings
- Complex operations

**Decreases Frequency**:
- Modern construction
- Sprinkler systems
- Security measures
- Loss control programs
- Lower-hazard occupancies
- Proper maintenance

### Exposure Unit Definition

Exposure units vary by line of business:
- **Property**: Building value in $100K units
- **Auto**: Number of vehicles
- **Workers Comp**: Payroll in $100 units
- **General Liability**: Sales in $1,000 units

**Example**:
```
Building valued at $2,500,000
Exposure Units = $2,500,000 / $100,000 = 25 units
```

---

## 4. Severity (Average Claim Amount)

### Purpose
Measure the average dollar amount of each claim. The second primary loss driver (along with frequency).

### Formula
```
Severity = Incurred Loss / Claim Count
```

### Code Reference
[backend/services/segment_kpis.py:93](backend/services/segment_kpis.py#L93)

### Example Calculation

**Scenario**:
```
Incurred Loss = $650,000
Claim Count = 45 claims
```

**Calculation**:
```
Severity = $650,000 / 45
         = $14,444.44 per claim
```

### Interpretation
- Average claim amount is $14,444
- Half of all claims may be above this amount, half below (approximately)
- Highly influenced by large losses
- Must be monitored for trends indicating claims inflation or risk deterioration

### Distribution Analysis

Claim severity typically follows a **skewed distribution**:

```
Typical Distribution:
  50% of claims: < $5,000 (small claims)
  40% of claims: $5,000 - $50,000 (medium claims)
  10% of claims: > $50,000 (large claims)

But large claims may account for:
  60-80% of total incurred losses
```

**Example**:
```
45 total claims with average severity $14,444:

Small claims:  23 claims × $3,000 = $69,000 (11%)
Medium claims: 20 claims × $8,000 = $160,000 (25%)
Large claims:  2 claims × $210,500 = $421,000 (65%)
                                    ─────────
Total:         45 claims            $650,000
Average:                            $14,444
```

### Industry Benchmarks

**Commercial Property - Severity Ranges**:
- **Minor**: $2,000 - $10,000 (water damage, small fires)
- **Moderate**: $10,000 - $50,000 (significant fire, equipment)
- **Major**: $50,000 - $500,000 (partial building loss)
- **Catastrophic**: >$500,000 (total loss)

**By Cause of Loss**:
- **Water Damage**: $5,000 - $25,000
- **Fire**: $30,000 - $150,000
- **Wind/Hail**: $15,000 - $75,000
- **Theft**: $3,000 - $20,000

### Trend Analysis

**Severity Trends** to monitor:
1. **Claims Inflation**: 3-5% annual increase typical
2. **Construction Cost Inflation**: Affects building claims
3. **Parts/Equipment Costs**: Impacts business property claims
4. **Legal Environment**: Can increase settlement amounts

**Example Severity Trend**:
```
Year 1: $12,500 average severity
Year 2: $13,000 average severity (4.0% increase)
Year 3: $14,444 average severity (11.1% increase) ← Investigate!
```

### Factors Affecting Severity

**Increases Severity**:
- Higher building values
- Complex/expensive equipment
- Inflation
- Broader coverage terms
- Generous claim settlements
- Litigation trends

**Decreases Severity**:
- Deductibles
- Loss mitigation measures
- Quick claims response
- Effective salvage
- Repair vs. replace strategies

---

## 5. Pure Premium

### Purpose
Calculate the expected loss cost per unit of exposure. This is the risk-based component of the premium before expenses and profit loads.

### Formula
```
Pure Premium = Incurred Loss / Total Exposure Units
```

### Alternative Formula
```
Pure Premium = Frequency × Severity / 100
```
(Since Frequency is per 100 units)

### Code Reference
[backend/services/segment_kpis.py:96](backend/services/segment_kpis.py#L96)

### Example Calculation

**Method 1 - Direct Calculation**:
```
Incurred Loss = $650,000
Total Exposure Units = 2,500 units
```

**Calculation**:
```
Pure Premium = $650,000 / 2,500
             = $260.00 per exposure unit
```

**Method 2 - Frequency × Severity** (Verification):
```
Frequency = 1.80 per 100 units
Severity = $14,444.44

Pure Premium = (1.80 / 100) × $14,444.44
             = 0.018 × $14,444.44
             = $260.00 per exposure unit ✓
```

### Interpretation
- The expected loss cost is $260 per $100,000 of building value
- This represents only the claims cost, not the full premium
- Must add expense loads and profit margin to get final premium rate

### Relationship to Premium

**Premium Construction**:
```
Premium Rate = Pure Premium / (1 - Expense Ratio - Profit Margin)
```

**Example**:
```
Pure Premium = $260
Expense Ratio = 30%
Profit Margin = 10%
Target Loss Ratio = 60%

Premium Rate = $260 / 0.60
             = $433.33 per $100K of building value

Or expressed as a rate per $100 of value:
$433.33 / 1,000 = $0.433 per $100
```

### Verification

**Check the Loss Ratio**:
```
For a $2,500,000 building (25 exposure units):

Premium = 25 × $433.33 = $10,833
Expected Loss = 25 × $260 = $6,500

Loss Ratio = $6,500 / $10,833 × 100% = 60.0% ✓
```

### Pure Premium by Risk Segment

**Example Portfolio Analysis**:
```
Segment          Frequency  Severity    Pure Premium
────────────────────────────────────────────────────
Low Risk           0.50     $8,000        $40.00
Medium Risk        1.50     $12,000       $180.00
High Risk          3.00     $18,000       $540.00
```

### Business Applications

1. **Pricing**:
   - Base rate development
   - Risk differentiation
   - Rate indications

2. **Underwriting**:
   - Risk selection criteria
   - Account evaluation
   - Renewal pricing

3. **Actuarial**:
   - Expected loss calculations
   - Reserve adequacy testing
   - Reinsurance pricing

4. **Portfolio Management**:
   - Segment profitability
   - Mix management
   - Growth strategies

### Pure Premium Trend Analysis

**Annual Trending**:
```
Current Pure Premium: $260.00
Trend Factor: 1.05 (5% annual increase)
Trended Pure Premium: $260.00 × 1.05 = $273.00

For 2-year projection:
Trended Pure Premium: $260.00 × 1.05² = $286.65
```

---

## 6. Average Premium per Policy

### Purpose
Calculate the average premium earned per policy. Useful for understanding policy size distribution and pricing adequacy.

### Formula

**By Segment**:
```
Average Premium per Policy = Earned Premium / Policy Count
```

**Overall Portfolio**:
```
Average Premium per Policy = Total Earned Premium / Total Policy Count
```

### Code Reference
[backend/services/segment_kpis.py:99](backend/services/segment_kpis.py#L99) (segment)
[backend/services/segment_kpis.py:142](backend/services/segment_kpis.py#L142) (overall)

### Example Calculation

**Scenario - Policy Size Segment: "Medium"**:
```
Earned Premium = $1,000,000
Policy Count = 150 policies
```

**Calculation**:
```
Average Premium = $1,000,000 / 150
                = $6,666.67 per policy
```

### Interpretation
- The typical policy in this segment generates $6,667 in annual premium
- Can identify premium concentration and account size distribution
- Helps in portfolio management and growth planning

### Segmentation Analysis

**By Policy Size Segment**:
```
Segment      Policy Count   Earned Premium    Avg Premium
──────────────────────────────────────────────────────────
Small             200         $400,000          $2,000
Medium            150       $1,000,000          $6,667
Large              50       $1,500,000         $30,000
──────────────────────────────────────────────────────────
Total             400       $2,900,000          $7,250
```

### Premium Concentration

**Measure concentration risk**:
```
Top 10% of policies (40 policies):
Premium = $1,600,000
Concentration = $1,600,000 / $2,900,000 = 55.2%
```

Interpretation: 10% of policies generate 55% of premium (high concentration).

### Distribution Metrics

**Coefficient of Variation** (Premium Distribution):
```
CV = Standard Deviation / Mean

Low CV (<0.5): Homogeneous portfolio
Medium CV (0.5-1.0): Moderate variation
High CV (>1.0): Heterogeneous portfolio
```

### Business Applications

1. **Growth Planning**:
   - Target account size
   - Sales force compensation
   - Marketing strategy

2. **Underwriting**:
   - Small account minimum premiums
   - Large account special handling
   - Declination thresholds

3. **Financial Planning**:
   - Premium volume projections
   - Renewal retention targets
   - New business goals

4. **Risk Management**:
   - Premium concentration limits
   - Single risk retention
   - Reinsurance attachment points

### Average Premium Trends

**Year-over-Year Analysis**:
```
Year 1: 400 policies, $2,600,000 premium = $6,500 avg
Year 2: 420 policies, $2,900,000 premium = $6,905 avg

Change: +6.2% average premium increase
        (combination of rate increase and mix shift)
```

**Decomposition**:
```
Rate Change Effect: +4.0%
Mix Shift Effect: +2.2% (more large policies)
Total Change: +6.2%
```

---

## 7. Total Earned Premium

### Purpose
Sum all earned premium across the portfolio or segment. This represents the revenue recognized for insurance coverage provided.

### Formula

**By Segment**:
```
Total Earned Premium (Segment) = Σ Earned Premium for all policies in segment
```

**Overall Portfolio**:
```
Total Earned Premium (Overall) = Σ Earned Premium for all policies
```

### Code Reference
[backend/services/segment_kpis.py:62](backend/services/segment_kpis.py#L62) (segment aggregation)
[backend/services/segment_kpis.py:116](backend/services/segment_kpis.py#L116) (overall)

### Example Calculation

**Scenario - All Geographies**:
```
Northeast:    $1,000,000
Southeast:      $750,000
Midwest:        $800,000
West:           $350,000
```

**Calculation**:
```
Total Earned Premium = $1,000,000 + $750,000 + $800,000 + $350,000
                     = $2,900,000
```

### Earned vs. Written Premium

**Key Concepts**:

**Written Premium**: Premium for policies written/sold
**Earned Premium**: Premium recognized as revenue for coverage provided

**Earning Pattern**:
```
Annual Policy: $12,000 written premium

Month 1: Earned = $12,000 × (1/12) = $1,000
Month 2: Earned = $12,000 × (2/12) = $2,000
...
Month 12: Earned = $12,000 × (12/12) = $12,000
```

### Unearned Premium Reserve

**Calculation**:
```
Unearned Premium Reserve = Written Premium - Earned Premium
```

**Example**:
```
Written Premium (year): $3,200,000
Earned Premium (6 months): $1,450,000
Unearned Premium Reserve: $1,750,000
```

This $1,750,000 represents future coverage obligations.

### Business Applications

1. **Financial Reporting**:
   - Income statement revenue
   - Premium growth metrics
   - Market share analysis

2. **Loss Ratio Calculation**:
   - Always use earned (not written) premium
   - Matches premium to exposure period
   - Ensures proper period matching

3. **Reinsurance**:
   - Ceding commission calculation
   - Premium allocation
   - Treaty settlement

4. **Pricing**:
   - Rate adequacy analysis
   - Premium volume projections
   - Renewal pricing

### Premium Volume Trends

**Growth Analysis**:
```
Year 1: $2,600,000
Year 2: $2,900,000

Growth Rate = ($2,900,000 - $2,600,000) / $2,600,000
            = $300,000 / $2,600,000
            = 11.5% growth
```

**Decomposition**:
```
Rate Change: +5.0% = $130,000
Exposure Growth: +6.5% = $170,000
Total Growth: +11.5% = $300,000
```

---

## 8. Total Incurred Loss

### Purpose
Sum all incurred losses (paid + reserved) across the portfolio or segment. Represents total estimated cost of claims.

### Formula

**By Segment**:
```
Total Incurred Loss (Segment) = Σ Incurred Amount for all claims in segment
```

**Overall Portfolio**:
```
Total Incurred Loss (Overall) = Σ Incurred Amount for all claims
```

**Components**:
```
Incurred Amount = Paid Amount + Case Reserve
```

### Code Reference
[backend/services/segment_kpis.py:71](backend/services/segment_kpis.py#L71) (segment aggregation)
[backend/services/segment_kpis.py:120](backend/services/segment_kpis.py#L120) (overall)

### Example Calculation

**Scenario - All Industry Segments**:
```
Manufacturing:    $650,000
Retail:           $425,000
Office:           $180,000
Hospitality:      $285,000
```

**Calculation**:
```
Total Incurred Loss = $650,000 + $425,000 + $180,000 + $285,000
                    = $1,540,000
```

### Components Detail

**Claim-Level Calculation**:
```
Claim 1: Paid $10,000 + Reserve $5,000 = $15,000 Incurred
Claim 2: Paid $8,000 + Reserve $0 = $8,000 Incurred (closed)
Claim 3: Paid $0 + Reserve $50,000 = $50,000 Incurred (reported, not paid)
───────────────────────────────────────────────────────
Total:   Paid $18,000 + Reserve $55,000 = $73,000 Incurred
```

### Incurred vs. Paid Losses

**Key Difference**:
- **Paid Loss**: Actual cash disbursed
- **Incurred Loss**: Paid + Estimated future payments (reserves)

**Example Portfolio**:
```
Total Incurred Loss:  $1,540,000
Total Paid Loss:      $1,235,000
Outstanding Reserves: $305,000

Reserve Ratio = $305,000 / $1,540,000 = 19.8%
```

### Reserve Development

**Tracking Over Time**:
```
Initial Report:
  Incurred = $50,000 (Paid $0 + Reserve $50,000)

After 6 months:
  Incurred = $48,000 (Paid $30,000 + Reserve $18,000)
  Development = -$2,000 (favorable)

At Closure:
  Incurred = $45,000 (Paid $45,000 + Reserve $0)
  Total Development = -$5,000 (10% favorable)
```

### Business Applications

1. **Loss Ratio Calculation**:
   ```
   Loss Ratio = Total Incurred Loss / Total Earned Premium
   ```

2. **Reserve Adequacy**:
   - Monitor reserve development
   - Validate actuarial estimates
   - Identify systematic bias

3. **Profitability Analysis**:
   - Segment performance
   - Underwriting year results
   - Portfolio management

4. **Reinsurance**:
   - Treaty settlements
   - Loss notifications
   - Commutation negotiations

### Loss Development Pattern

**Typical Pattern** (% of Ultimate):
```
Report:        40% incurred (mostly reserves)
6 months:      70% incurred
12 months:     85% incurred
24 months:     95% incurred
Closure:      100% incurred (all paid)
```

---

## 9. Total Paid Loss

### Purpose
Sum all cash payments made for claims. Represents actual cash outflow for losses.

### Formula

**By Segment**:
```
Total Paid Loss (Segment) = Σ Paid Amount for all claims in segment
```

**Overall Portfolio**:
```
Total Paid Loss (Overall) = Σ Paid Amount for all claims
```

### Code Reference
[backend/services/segment_kpis.py:72](backend/services/segment_kpis.py#L72) (segment aggregation)
[backend/services/segment_kpis.py:121](backend/services/segment_kpis.py#L121) (overall)

### Example Calculation

**Scenario**:
```
Total Incurred Loss: $1,540,000
Outstanding Reserves: $305,000
```

**Calculation**:
```
Total Paid Loss = Total Incurred Loss - Outstanding Reserves
                = $1,540,000 - $305,000
                = $1,235,000
```

### Payment Pattern Analysis

**Cumulative Paid %** (of Ultimate):
```
Time Period    Cumulative Paid %
──────────────────────────────────
At Report            0-10%
1 month              20-30%
3 months             40-50%
6 months             60-70%
12 months            75-85%
24 months            90-95%
36 months            95-98%
Closure             100%
```

### Cash Flow Implications

**Monthly Payment Pattern**:
```
Month 1: $150,000 in payments
Month 2: $125,000 in payments
Month 3: $110,000 in payments
...

Average Monthly Payments = Total Paid / Months
                         = $1,235,000 / 12
                         = $102,917 per month
```

### Relationship to Incurred

**Paid-to-Incurred Ratio**:
```
Paid-to-Incurred Ratio = Total Paid Loss / Total Incurred Loss
                       = $1,235,000 / $1,540,000
                       = 80.2%
```

**Interpretation**:
- 80.2% of estimated losses have been paid
- 19.8% remains in reserves
- Higher ratio = more mature claims

### Business Applications

1. **Cash Flow Management**:
   - Liquidity planning
   - Investment strategy
   - Reserve adequacy

2. **Treasury Operations**:
   - Bank balance requirements
   - Credit line needs
   - Investment duration matching

3. **Reinsurance**:
   - Cash calls on treaties
   - Recoverable collection
   - Commutation valuations

4. **Financial Reporting**:
   - Cash flow statements
   - Reconciliation to reserves
   - Audit support

---

## 10. Total Exposure Units

### Purpose
Measure the aggregate risk exposure across the portfolio. Provides the denominator for frequency and pure premium calculations.

### Formula

**By Segment**:
```
Total Exposure Units (Segment) = Σ Exposure Units for all policies in segment
```

**Overall Portfolio**:
```
Total Exposure Units (Overall) = Σ Exposure Units for all policies
```

**Exposure Unit Calculation** (Property):
```
Exposure Units = Building Value / $100,000
```

### Code Reference
[backend/services/segment_kpis.py:63](backend/services/segment_kpis.py#L63) (segment aggregation)
[backend/services/segment_kpis.py:117](backend/services/segment_kpis.py#L117) (overall)

### Example Calculation

**Scenario - Individual Policies**:
```
Policy 1: Building Value $2,500,000 → 25 units
Policy 2: Building Value $1,200,000 → 12 units
Policy 3: Building Value $750,000 → 7.5 units
Policy 4: Building Value $3,000,000 → 30 units
```

**Calculation**:
```
Total Exposure Units = 25 + 12 + 7.5 + 30
                     = 74.5 units
```

### Exposure Base by Line of Business

**Commercial Property**:
```
Exposure Base = Building Value (in $100K units)
Example: $5,000,000 building = 50 units
```

**Business Personal Property**:
```
Exposure Base = Contents Value (in $100K units)
Example: $500,000 contents = 5 units
```

**Business Income**:
```
Exposure Base = Annual Receipts (in $1M units)
Example: $10,000,000 revenue = 10 units
```

**General Liability**:
```
Exposure Base = Sales (in $1,000 units)
Example: $2,000,000 sales = 2,000 units
```

### Exposure Growth Analysis

**Year-over-Year**:
```
Year 1: 2,400 exposure units
Year 2: 2,500 exposure units

Exposure Growth = (2,500 - 2,400) / 2,400
                = 100 / 2,400
                = 4.2% growth
```

**Sources of Growth**:
```
New Business:        +150 units
Renewals (inflation): +50 units
Lost Business:       -100 units
────────────────────────────────
Net Growth:          +100 units
```

### Business Applications

1. **Frequency Calculation**:
   ```
   Frequency = (Claim Count / Exposure Units) × 100
   ```

2. **Pure Premium Calculation**:
   ```
   Pure Premium = Incurred Loss / Exposure Units
   ```

3. **Pricing**:
   - Rate per unit of exposure
   - Premium calculation
   - Rate filing support

4. **Capacity Management**:
   - PML (Probable Maximum Loss) analysis
   - Catastrophe modeling
   - Reinsurance purchasing

### Exposure Tracking

**By Segment**:
```
Segment          Exposure Units    % of Total
────────────────────────────────────────────
Northeast            750              30%
Southeast            625              25%
Midwest              625              25%
West                 500              20%
────────────────────────────────────────────
Total              2,500             100%
```

---

## 11. Policy Count

### Purpose
Count the number of individual insurance policies in the portfolio or segment. Used for calculating averages and measuring portfolio size.

### Formula

**By Segment**:
```
Policy Count (Segment) = Count of unique PolicyIDs in segment
```

**Overall Portfolio**:
```
Policy Count (Overall) = Count of unique PolicyIDs in portfolio
```

### Code Reference
[backend/services/segment_kpis.py:64](backend/services/segment_kpis.py#L64) (segment - nunique)
[backend/services/segment_kpis.py:118](backend/services/segment_kpis.py#L118) (overall - nunique)

### Example Calculation

**Scenario - Risk Rating Segments**:
```
Low Risk:       150 policies
Medium Risk:    200 policies
High Risk:       50 policies
```

**Calculation**:
```
Total Policy Count = 150 + 200 + 50
                   = 400 policies
```

### Distribution Metrics

**Policies by Segment Size**:
```
Segment         Policy Count    % of Total    Avg Premium
─────────────────────────────────────────────────────────
Small               200           50%           $2,000
Medium              150           37.5%         $6,667
Large                50           12.5%        $30,000
─────────────────────────────────────────────────────────
Total               400          100%           $7,250
```

### Retention Analysis

**Annual Policy Retention**:
```
Beginning Policies: 380
Renewed Policies: 330
Retention Rate = 330 / 380 = 86.8%

Lost Policies: 50 (13.2%)
New Policies: 70
Ending Policies: 400

Net Growth = 70 - 50 = +20 policies (+5.3%)
```

### Business Applications

1. **Average Premium Calculation**:
   ```
   Average Premium = Total Premium / Policy Count
   ```

2. **Market Share**:
   ```
   Market Share = Your Policy Count / Total Market Policies
   ```

3. **Sales Planning**:
   - New business targets
   - Retention goals
   - Growth strategies

4. **Operational Planning**:
   - Staffing requirements
   - System capacity
   - Service levels

### Policy Distribution Analysis

**By Premium Size**:
```
Premium Range    Policy Count    Total Premium    % Premium
──────────────────────────────────────────────────────────
< $2,000              100          $150,000         5.2%
$2,000-$10,000        200        $1,000,000        34.5%
$10,000-$50,000        80        $1,600,000        55.2%
> $50,000              20          $150,000         5.2%
──────────────────────────────────────────────────────────
Total                 400        $2,900,000       100.0%
```

**Concentration Risk**:
- Top 5% of policies (20 policies) = 5.2% of premium (low concentration)
- Top 25% of policies (100 policies) = 60.4% of premium (moderate concentration)

---

## 12. Claim Count

### Purpose
Count the total number of claims reported in the portfolio or segment. Used for frequency calculation and loss trend analysis.

### Formula

**By Segment**:
```
Claim Count (Segment) = Count of ClaimIDs in segment
```

**Overall Portfolio**:
```
Claim Count (Overall) = Count of all ClaimIDs
```

### Code Reference
[backend/services/segment_kpis.py:73](backend/services/segment_kpis.py#L73) (segment)
[backend/services/segment_kpis.py:122](backend/services/segment_kpis.py#L122) (overall)

### Example Calculation

**Scenario - All Industry Segments**:
```
Manufacturing:    45 claims
Retail:           32 claims
Office:            8 claims
Hospitality:      18 claims
```

**Calculation**:
```
Total Claim Count = 45 + 32 + 8 + 18
                  = 103 claims
```

### Claim Count vs. Claimant Count

**Important Distinction**:
- **Claim Count**: Number of individual claim files/incidents
- **Claimant Count**: Number of people/entities making claims (may be multiple per claim)

**Example**:
```
Single fire incident:
  - 1 Claim (one incident)
  - 3 Claimants (building owner, tenant, neighbor)
  - Multiple coverages (building, contents, BI)
```

### Frequency Relationship

**Calculation**:
```
Given:
  Claim Count = 103
  Exposure Units = 2,500

Frequency = (103 / 2,500) × 100
          = 4.12 claims per 100 units
```

### Claims by Size

**Distribution**:
```
Claim Size          Count    % of Count    Avg Amount
───────────────────────────────────────────────────────
< $5,000              52        50%          $2,500
$5,000-$25,000        38        37%         $12,000
$25,000-$100,000      10        10%         $50,000
> $100,000             3         3%        $200,000
───────────────────────────────────────────────────────
Total                103       100%         $14,951
```

### Business Applications

1. **Frequency Calculation**:
   ```
   Frequency = (Claim Count / Exposure Units) × 100
   ```

2. **Claims Management**:
   - Staffing requirements
   - Adjuster allocation
   - Claim system capacity

3. **Loss Prevention**:
   - Identify high-frequency risks
   - Target loss control efforts
   - Monitor improvement programs

4. **Pricing**:
   - Frequency trending
   - Expected claim counts
   - Rate level indications

### Trend Analysis

**Year-over-Year**:
```
Year 1: 95 claims on 2,400 units = 3.96 frequency
Year 2: 103 claims on 2,500 units = 4.12 frequency

Frequency Change: +4.0%
  - Exposure growth: +4.2%
  - Claim count growth: +8.4%
  - Frequency deterioration: +4.0%
```

### Claim Closure Rate

**Tracking**:
```
Total Claims (current year): 103
Closed Claims: 78
Open Claims: 25

Closure Rate = 78 / 103 = 75.7%
```

**Aging of Open Claims**:
```
0-3 months:    15 claims
3-6 months:     6 claims
6-12 months:    3 claims
> 12 months:    1 claim
```

---

## 13. Frequency-Severity Relationship

### Purpose
Understand the fundamental relationship between claim frequency and severity, and how they combine to drive overall loss costs.

### Formula

**Loss Cost Decomposition**:
```
Pure Premium = Frequency × Severity / 100
```

Or equivalently:
```
Incurred Loss = (Frequency × Severity × Exposure Units) / 100
```

### Mathematical Relationship

**Starting from First Principles**:
```
Given:
  Frequency (F) = (Claim Count / Exposure Units) × 100
  Severity (S) = Incurred Loss / Claim Count

Derivation:
  Pure Premium = Incurred Loss / Exposure Units

               = (Claim Count × Severity) / Exposure Units

               = [(Frequency × Exposure Units) / 100] × Severity / Exposure Units

               = (Frequency × Severity) / 100  ✓
```

### Example Calculation

**Scenario**:
```
Frequency = 1.80 per 100 units
Severity = $14,444
Exposure Units = 2,500 units
```

**Method 1 - Using Pure Premium**:
```
Pure Premium = (Frequency × Severity) / 100
             = (1.80 × $14,444) / 100
             = $25,999 / 100
             = $260 per unit

Total Loss = Pure Premium × Exposure Units
           = $260 × 2,500
           = $650,000
```

**Method 2 - Direct Calculation** (Verification):
```
Expected Claim Count = (Frequency × Exposure Units) / 100
                     = (1.80 × 2,500) / 100
                     = 45 claims

Total Loss = Claim Count × Severity
           = 45 × $14,444
           = $650,000 ✓
```

### Frequency-Severity Trade-off

**Portfolio Comparison**:
```
Portfolio A (High Frequency, Low Severity):
  Frequency: 4.0 per 100 units
  Severity: $5,000
  Pure Premium: (4.0 × $5,000) / 100 = $200

Portfolio B (Low Frequency, High Severity):
  Frequency: 1.0 per 100 units
  Severity: $20,000
  Pure Premium: (1.0 × $20,000) / 100 = $200
```

Both have same pure premium but very different risk profiles!

### Risk Characteristics

**High Frequency / Low Severity**:
- More predictable (law of large numbers)
- Lower volatility
- Examples: Small retail, office buildings
- Pricing: More credible, tighter ranges

**Low Frequency / High Severity**:
- Less predictable
- Higher volatility
- Examples: Large manufacturing, catastrophe exposure
- Pricing: Less credible, wider ranges, more reliance on judgment

### Loss Control Impact

**Frequency Reduction Program**:
```
Before:
  Frequency: 2.0, Severity: $15,000
  Pure Premium: (2.0 × $15,000) / 100 = $300

After (20% frequency reduction):
  Frequency: 1.6, Severity: $15,000
  Pure Premium: (1.6 × $15,000) / 100 = $240

Savings: $60 per unit (20% reduction)
```

**Severity Reduction Program** (e.g., sprinklers):
```
Before:
  Frequency: 2.0, Severity: $15,000
  Pure Premium: (2.0 × $15,000) / 100 = $300

After (30% severity reduction):
  Frequency: 2.0, Severity: $10,500
  Pure Premium: (2.0 × $10,500) / 100 = $210

Savings: $90 per unit (30% reduction)
```

### Trend Analysis

**Component Trending**:
```
Current:
  Frequency: 1.80
  Severity: $14,444
  Pure Premium: $260

Trended (1 year):
  Frequency Trend: -2% annually = 1.764
  Severity Trend: +5% annually = $15,166

Trended Pure Premium: (1.764 × $15,166) / 100
                    = $267.53

Overall Trend: +2.9% = (+5% - 2%)
```

### Visualization

**Frequency-Severity Matrix**:
```
                Low Severity    Med Severity    High Severity
                ($5K)          ($15K)          ($50K)
────────────────────────────────────────────────────────────
High Frequency   $200 PP        $600 PP         $2,000 PP
(4.0)            Retail         Restaurant      High Hazard

Med Frequency    $100 PP        $300 PP         $1,000 PP
(2.0)            Office         Warehouse       Manufacturing

Low Frequency    $50 PP         $150 PP         $500 PP
(1.0)            Low Hazard     Standard        Complex Risk
```

### Business Applications

1. **Underwriting**:
   - Risk classification
   - Account selection
   - Terms and conditions

2. **Pricing**:
   - Base rate development
   - Rating plan design
   - Deductible programs

3. **Loss Control**:
   - Program prioritization
   - ROI analysis
   - Risk improvement

4. **Reinsurance**:
   - Treaty structure (frequency vs. severity)
   - Retention determination
   - Premium allocation

---

## 14. Combined Ratio (Conceptual)

### Purpose
Measure total underwriting profitability by combining loss ratio with expense ratio. A combined ratio under 100% indicates underwriting profit.

### Formula
```
Combined Ratio = Loss Ratio + Expense Ratio
```

**Components**:
```
Loss Ratio = (Incurred Loss / Earned Premium) × 100%
Expense Ratio = (Underwriting Expenses / Earned Premium) × 100%
```

### Code Reference
Note: Not directly calculated in current implementation, but conceptually derived from loss ratio.

### Example Calculation

**Scenario**:
```
Earned Premium: $1,000,000
Incurred Loss: $650,000
Underwriting Expenses: $300,000
```

**Calculation**:
```
Loss Ratio = ($650,000 / $1,000,000) × 100%
           = 65.0%

Expense Ratio = ($300,000 / $1,000,000) × 100%
              = 30.0%

Combined Ratio = 65.0% + 30.0%
               = 95.0%
```

### Interpretation

**Combined Ratio Ranges**:
- **< 95%**: Excellent underwriting profit
- **95-100%**: Profitable underwriting
- **100%**: Break-even on underwriting
- **100-110%**: Modest underwriting loss (may be offset by investment income)
- **> 110%**: Significant underwriting loss

**Example Result**:
```
Combined Ratio = 95.0%

Underwriting Profit = (100% - 95%) × Premium
                    = 5% × $1,000,000
                    = $50,000
```

### Expense Ratio Components

**Typical Expense Breakdown** (Property insurance):
```
Commissions:           15-20%
Underwriting Expenses:  5-8%
Premium Taxes:          2-3%
General Overhead:       5-7%
────────────────────────────
Total Expense Ratio:   27-38%
```

**Example**:
```
Premium: $1,000,000

Commissions (17%):      $170,000
UW Expenses (6%):       $60,000
Premium Tax (2.5%):     $25,000
Overhead (6%):          $60,000
──────────────────────────────
Total Expenses (31.5%): $315,000
```

### Target Ratios

**Commercial Property Benchmarks**:
```
Target Loss Ratio:     60-65%
Target Expense Ratio:  30-35%
────────────────────────────────
Target Combined Ratio: 90-100%
```

**Variations by Distribution Channel**:
```
Direct Sales:
  Loss Ratio: 65%
  Expense Ratio: 25% (no commissions)
  Combined: 90%

Agent Channel:
  Loss Ratio: 63%
  Expense Ratio: 32% (includes commissions)
  Combined: 95%
```

### Underwriting Profit Calculation

**Full Income Statement**:
```
Earned Premium:              $1,000,000   100.0%

Incurred Losses:              $650,000    65.0%
Underwriting Expenses:        $300,000    30.0%
────────────────────────────────────────────────
Underwriting Profit:           $50,000     5.0%

Investment Income:             $30,000     3.0%
────────────────────────────────────────────────
Pre-Tax Operating Income:      $80,000     8.0%
```

### Business Applications

1. **Profitability Targets**:
   - Set combined ratio goals
   - Measure performance
   - Bonus calculations

2. **Rate Adequacy**:
   - Determine needed rate changes
   - Support rate filings
   - Competitive positioning

3. **Portfolio Management**:
   - Identify unprofitable segments
   - Resource allocation
   - Strategic planning

4. **Benchmarking**:
   - Industry comparisons
   - Peer analysis
   - Best practice identification

### Rate Change Indication

**Formula for Rate Need**:
```
Indicated Rate Change = (Target Combined Ratio / Current Combined Ratio) - 1
```

**Example**:
```
Current Combined Ratio: 105%
Target Combined Ratio: 95%

Rate Change = (95% / 105%) - 1
            = 0.9048 - 1
            = -9.52%

Wait, this is backwards! Let's fix:

Current Combined Ratio: 105% (losing money)
Target Combined Ratio: 95%

Current Premium produces 105% combined
We need premium to produce 95% combined

Rate Change = (105% / 95%) - 1
            = 1.1053 - 1
            = +10.53% rate increase needed
```

### Verification

**Before Rate Increase**:
```
Premium: $1,000,000
Losses: $650,000 (65%)
Expenses: $400,000 (40%)
Combined: 105%
```

**After +10.53% Rate Increase**:
```
Premium: $1,105,300
Losses: $650,000 (58.8%)
Expenses: $400,000 (36.2%)
Combined: 95.0% ✓
```

---

## 15. Segment KPI Analysis Overview

### Purpose
Comprehensive framework for analyzing insurance portfolio performance across different segmentation dimensions.

### Segmentation Dimensions

The system supports four primary segmentation dimensions:

1. **Geography**: Regional performance analysis
2. **Industry**: Industry sector analysis
3. **PolicySize**: Account size analysis
4. **RiskRating**: Risk quality analysis (COPE-based)

### Complete Analysis Flow

```
Step 1: Data Aggregation
   ↓
   • Aggregate premium and exposure by segment
   • Aggregate claims by segment
   • Link policies to exposures and claims
   ↓
Step 2: Calculate Segment KPIs
   ↓
   • Loss Ratio = (Incurred / Premium) × 100%
   • Frequency = (Claims / Exposure) × 100
   • Severity = Incurred / Claims
   • Pure Premium = Frequency × Severity / 100
   • Average Premium = Premium / Policy Count
   ↓
Step 3: Calculate Overall Portfolio KPIs
   ↓
   • Sum across all segments
   • Weighted averages where appropriate
   • Portfolio-level metrics
   ↓
Step 4: Analysis & Insights
   ↓
   • Identify high/low performing segments
   • Frequency-severity analysis
   • Trend identification
   • Action recommendations
```

### Example: Complete Segment Analysis

**Geography Segment Analysis**:

```
Segment      Premium   Exposure  Claims   Loss    Freq   Severity  Pure
                                          Ratio                    Prem
─────────────────────────────────────────────────────────────────────────
Northeast  $1,000,000   625      32      65.0%   5.12   $20,313   $1,040
Southeast    $750,000   550      18      56.7%   3.27   $23,611     $772
Midwest      $800,000   825      28      68.8%   3.39   $19,686     $668
West         $350,000   500      25      81.4%   5.00   $11,398     $570
─────────────────────────────────────────────────────────────────────────
Total      $2,900,000  2,500    103      65.5%   4.12   $18,447     $760
```

### Interpretation & Insights

**Northeast Region**:
```
Loss Ratio: 65.0% (on target)
Frequency: 5.12 (high - investigate)
Severity: $20,313 (above average)
Pure Premium: $1,040 (highest)

Action: Monitor frequency, consider loss control programs
```

**Southeast Region**:
```
Loss Ratio: 56.7% (excellent)
Frequency: 3.27 (good)
Severity: $23,611 (highest - large risks?)
Pure Premium: $772

Action: Opportunity for growth, competitive advantage
```

**West Region**:
```
Loss Ratio: 81.4% (poor - needs attention!)
Frequency: 5.00 (very high)
Severity: $11,398 (lowest - many small claims)
Pure Premium: $570

Action: Immediate review needed
  • Rate inadequacy?
  • Poor risk selection?
  • Unique hazards?
  • Consider rate increase or underwriting tightening
```

### Multi-Dimensional Analysis

**Example: Geography × Industry Drill-Down**:

```
Region      Industry        Premium   Loss Ratio   Action
─────────────────────────────────────────────────────────
West        Manufacturing   $200,000     95.0%     Review
West        Hospitality     $150,000     75.0%     Monitor

Insight: West region's poor performance driven by
         Manufacturing segment specifically
```

### Actionable Insights Framework

**For Each Segment, Determine**:

1. **Profitability Status**:
   - Excellent (LR < 60%)
   - Good (LR 60-70%)
   - Acceptable (LR 70-80%)
   - Poor (LR > 80%)

2. **Risk Profile**:
   - High Freq / Low Sev (many small claims)
   - Low Freq / High Sev (few large claims)
   - High Freq / High Sev (serious issues)
   - Low Freq / Low Sev (ideal)

3. **Recommended Actions**:
   - Grow (profitable segments)
   - Maintain (on-target segments)
   - Improve (borderline segments)
   - Remediate (poor segments)
   - Exit (unacceptable segments)

### Decision Matrix

```
                  Low Loss Ratio        High Loss Ratio
                  (< 65%)               (> 75%)
────────────────────────────────────────────────────────
High Premium      GROW AGGRESSIVELY     FIX OR EXIT
Volume            • Lower rates?        • Rate increase
(> $500K)         • Increase capacity   • UW review
                  • Marketing focus     • Non-renew worst

Low Premium       SELECTIVE GROWTH      EXIT
Volume            • Stable segment      • Not worth fixing
(< $500K)         • Maintain quality    • Redirect resources
```

### Portfolio Optimization

**Example Strategy**:
```
Current Portfolio:
  Northeast (35% premium, 65% LR): Maintain
  Southeast (26% premium, 57% LR): Grow to 35%
  Midwest (28% premium, 69% LR): Maintain
  West (12% premium, 81% LR): Reduce to 5%

Target Portfolio (in 2 years):
  Northeast: 30% ($1,050,000)
  Southeast: 35% ($1,225,000)
  Midwest: 30% ($1,050,000)
  West: 5% ($175,000)

  Total: $3,500,000 (+21% growth)
  Blended Loss Ratio: Target 63% (from 65.5%)
```

### Monitoring Cadence

**Frequency of Review**:
- **Overall KPIs**: Monthly
- **Segment KPIs**: Quarterly
- **Deep Dive Analysis**: Semi-annually
- **Strategic Review**: Annually

### Key Performance Questions

For each segment, ask:

1. **Is it profitable?** (Loss Ratio vs. Target)
2. **Is it growing?** (Premium trend)
3. **Is it stable?** (Loss ratio volatility)
4. **Is it strategic?** (Fits company objectives)
5. **Can we improve it?** (Actionable levers)

If answers are mostly "no," consider exiting the segment.

---

## Summary Table: All Metrics

| # | Metric | Formula | Code Location |
|---|--------|---------|---------------|
| 1 | Loss Ratio | `(Incurred / Premium) × 100%` | segment_kpis.py:86 |
| 2 | Paid Loss Ratio | `(Paid / Premium) × 100%` | segment_kpis.py:87 |
| 3 | Frequency | `(Claims / Exposure) × 100` | segment_kpis.py:90 |
| 4 | Severity | `Incurred / Claims` | segment_kpis.py:93 |
| 5 | Pure Premium | `Incurred / Exposure` | segment_kpis.py:96 |
| 6 | Avg Premium | `Premium / Policy Count` | segment_kpis.py:99 |
| 7 | Total Earned Premium | `Σ Earned Premium` | segment_kpis.py:116 |
| 8 | Total Incurred Loss | `Σ Incurred Amount` | segment_kpis.py:120 |
| 9 | Total Paid Loss | `Σ Paid Amount` | segment_kpis.py:121 |
| 10 | Total Exposure | `Σ Exposure Units` | segment_kpis.py:117 |
| 11 | Policy Count | `Count unique PolicyIDs` | segment_kpis.py:118 |
| 12 | Claim Count | `Count ClaimIDs` | segment_kpis.py:122 |
| 13 | Freq-Sev Relation | `PP = (F × S) / 100` | (derived) |
| 14 | Combined Ratio | `LR + Expense Ratio` | (conceptual) |

---

## Glossary

**Earned Premium**: Premium recognized as revenue for coverage provided during the period

**Exposure Units**: Standardized measure of risk exposure (e.g., building value in $100K units)

**Frequency**: Number of claims per 100 units of exposure

**Incurred Loss**: Total estimated loss including both paid amounts and outstanding reserves

**Loss Ratio**: Percentage of premium paid out as losses

**Paid Loss**: Actual cash disbursed for claim payments

**Policy Count**: Number of individual insurance policies

**Pure Premium**: Expected loss cost per unit of exposure (before expense loads)

**Segment**: Grouping of policies by a common characteristic (Geography, Industry, etc.)

**Severity**: Average dollar amount per claim

**Total Exposure**: Aggregate measure of risk across all policies

**Underwriting Profit**: Premium minus losses and expenses

---

## References and Resources

### Actuarial Standards

- **ASOP No. 12**: Risk Classification
- **ASOP No. 13**: Trending Procedures
- **ASOP No. 53**: Pricing of Property/Casualty Insurance

### Industry Publications

- **CAS Exam 5 Study Materials**: Basic Ratemaking
- **Werner & Modlin**: "Basic Ratemaking"
- **Friedland**: "Fundamentals of General Insurance Actuarial Analysis"

### Regulatory Guidance

- **NAIC**: Rate Filing Requirements
- **State Regulations**: Varies by jurisdiction
- **ISO**: Industry Statistical Data

### Industry Benchmarks

- **Best's Aggregates & Averages**: Industry data
- **ISO Circulars**: Loss costs and trends
- **NCCI**: Workers compensation benchmarks
- **AAIS**: Property loss cost data

---

## Document Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-23 | Initial comprehensive documentation | Actuarial Insights Workbench Team |

---

**End of Document**
