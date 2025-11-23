# Loss Development Tab - Formula Reference Guide

**Version**: 1.0
**Last Updated**: November 22, 2024
**Purpose**: Complete mathematical reference for all formulas used in the Loss Development Dashboard

---

## Table of Contents

1. [Development Months Calculation](#1-development-months-calculation)
2. [Incremental Triangle](#2-incremental-triangle)
3. [Cumulative Triangle](#3-cumulative-triangle)
4. [Age-to-Age Development Factors (Volume-Weighted)](#4-age-to-age-development-factors-volume-weighted)
5. [Age-to-Age Development Factors (Simple Average)](#5-age-to-age-development-factors-simple-average)
6. [Cumulative Development Factor](#6-cumulative-development-factor-cdf)
7. [Ultimate Loss Projection](#7-ultimate-loss-projection)
8. [IBNR Reserve](#8-ibnr-incurred-but-not-reported-reserve)
9. [Percent Developed](#9-percent-developed)
10. [Total Reported Losses](#10-total-reported-losses)
11. [Total Ultimate Losses](#11-total-ultimate-losses)
12. [Total IBNR](#12-total-ibnr)
13. [Average Development Factor](#13-average-development-factor)
14. [Implied % Development](#14-implied--development)
15. [Chain-Ladder Method Overview](#chain-ladder-method-overview)

---

## 1. Development Months Calculation

### Purpose
Calculate how many months have elapsed from the loss occurrence date to the loss report date.

### Formula
```
Development Months = (Report Year - Loss Year) × 12 + (Report Month - Loss Month)
```

### Code Reference
[backend/services/loss_triangle.py:45-48](backend/services/loss_triangle.py#L45-L48)

### Example
**Scenario**:
- Loss Date: January 15, 2023
- Report Date: April 20, 2023

**Calculation**:
```
Development Months = (2023 - 2023) × 12 + (4 - 1)
                   = 0 × 12 + 3
                   = 3 months
```

### Notes
- The result is always clipped to be non-negative (minimum value is 0)
- Day of month is not considered, only year and month
- This represents the lag time between when the loss occurred and when it was reported to the insurer

---

## 2. Incremental Triangle

### Purpose
Display losses reported in each specific development period, showing the incremental loss emergence.

### Formula
```
Incremental Loss(AY, Dev) = Σ Loss Amount for all claims where:
                             - Accident Year = AY
                             - Development Month = Dev
```

### Code Reference
[backend/services/loss_triangle.py:72-79](backend/services/loss_triangle.py#L72-L79)

### Example Matrix
```
                 Dev 0      Dev 1      Dev 2      Dev 3
AY 2021         $50,000    $30,000    $15,000    $5,000
AY 2022         $45,000    $25,000    $12,000       -
AY 2023         $48,000    $28,000       -          -
```

### Interpretation
- **Dev 0**: Losses reported in the same month as the accident
- **Dev 1**: New losses reported 1 month after the accident
- Each cell shows only the new losses reported at that specific development age
- Blank cells (or dashes) indicate the development period hasn't been reached yet

### Business Use
- Identify patterns in loss reporting behavior
- Detect unusual spikes in claim reporting
- Monitor how quickly claims are being reported

---

## 3. Cumulative Triangle

### Purpose
Show the total accumulated losses reported to date for each accident year at each development stage.

### Formula

**Method 1 - Direct Summation**:
```
Cumulative Loss(AY, Dev) = Σ Incremental Loss(AY, i)
                           i=0 to Dev
```

**Method 2 - Recursive**:
```
Cumulative Loss(AY, Dev) = Cumulative Loss(AY, Dev-1) + Incremental Loss(AY, Dev)
```

### Code Reference
[backend/services/loss_triangle.py:82-83](backend/services/loss_triangle.py#L82-L83)

### Example Matrix
```
                 Dev 0      Dev 1      Dev 2      Dev 3
AY 2021         $50,000    $80,000    $95,000   $100,000
AY 2022         $45,000    $70,000    $82,000       -
AY 2023         $48,000    $76,000       -          -
```

### Relationship to Incremental Triangle
Using the incremental triangle from section 2:
- AY 2021, Dev 1: $50,000 + $30,000 = $80,000
- AY 2021, Dev 2: $80,000 + $15,000 = $95,000
- AY 2021, Dev 3: $95,000 + $5,000 = $100,000

### Interpretation
- Each cell shows the total losses reported from Dev 0 through that development month
- Values always increase (or stay the same) as you move right across development periods
- This is the primary triangle used for development factor calculations

---

## 4. Age-to-Age Development Factors (Volume-Weighted)

### Purpose
Calculate how much losses develop from one period to the next using industry-standard volume-weighted methodology.

### Formula
```
                         Σ Cumulative Loss(all AY, Dev+1)
LDF(Dev→Dev+1) = ──────────────────────────────────────────
                         Σ Cumulative Loss(all AY, Dev)
```

**Where**: Only accident years with positive values in both periods are included in the calculation.

### Code Reference
[backend/services/loss_triangle.py:166-170](backend/services/loss_triangle.py#L166-L170)

### Example Calculation

**Cumulative Triangle**:
```
                Dev 0      Dev 1
AY 2021        $50,000    $80,000
AY 2022        $45,000    $70,000
AY 2023        $48,000    $76,000
─────────────────────────────────
Total         $143,000   $226,000
```

**Calculation**:
```
LDF(0→1) = $226,000 / $143,000
         = 1.5804
```

### Interpretation
- A factor of 1.5804 means losses increase by 58.04% from Dev 0 to Dev 1
- Volume-weighted method gives more weight to larger accident years
- This is the industry-preferred method because it's more stable for smaller datasets

### Advantages
- Less volatile than simple average method
- More appropriate when accident years have varying exposures
- Widely accepted by regulators and auditors

---

## 5. Age-to-Age Development Factors (Simple Average)

### Purpose
Alternative method for calculating development factors using arithmetic mean of individual ratios.

### Formula
```
                         1    n    Cumulative Loss(AYᵢ, Dev+1)
LDF(Dev→Dev+1) = ─── Σ  ─────────────────────────────────
                         n   i=1   Cumulative Loss(AYᵢ, Dev)
```

**Where**:
- n = number of accident years with valid data
- Valid data means both Dev and Dev+1 have positive values

### Code Reference
[backend/services/loss_triangle.py:172-174](backend/services/loss_triangle.py#L172-L174)

### Example Calculation

**Individual Ratios**:
```
AY 2021: $80,000 / $50,000 = 1.6000
AY 2022: $70,000 / $45,000 = 1.5556
AY 2023: $76,000 / $48,000 = 1.5833
```

**Average**:
```
LDF(0→1) = (1.6000 + 1.5556 + 1.5833) / 3
         = 4.7389 / 3
         = 1.5796
```

### Comparison to Volume-Weighted
- Simple Average: 1.5796
- Volume-Weighted: 1.5804
- Difference is usually small but can be significant with heterogeneous data

### When to Use
- When accident years have similar exposure levels
- When specific accident years shouldn't dominate the factor
- For sensitivity analysis and validation

---

## 6. Cumulative Development Factor (CDF)

### Purpose
Calculate the total development from current maturity to ultimate losses.

### Formula
```
CDF(Dev→Ultimate) = LDF(Dev→Dev+1) × LDF(Dev+1→Dev+2) × ... × LDF(N-1→N)
```

Or using product notation:
```
                     N-1
CDF(Dev→Ultimate) = Π LDF(i→i+1)
                    i=Dev
```

### Code Reference
[backend/services/loss_triangle.py:204-208](backend/services/loss_triangle.py#L204-L208)

### Example Calculation

**Given Link Ratios**:
```
LDF(2→3)  = 1.1500
LDF(3→4)  = 1.0800
LDF(4→5)  = 1.0300
LDF(5→36) = 1.0100
```

**Calculation**:
```
CDF(2→Ultimate) = 1.1500 × 1.0800 × 1.0300 × 1.0100
                = 1.2876
```

### Interpretation
- A CDF of 1.2876 means losses at Dev 2 will develop to 128.76% of their current value
- Equivalently, there's still 28.76% more development to occur
- This is the key factor used for ultimate loss projection

### Tail Factor
The final LDF (e.g., LDF(5→36)) is often called the "tail factor" and represents:
- Development beyond the observable data
- Selected based on industry benchmarks or judgment
- Critical for long-tail lines like liability insurance

---

## 7. Ultimate Loss Projection

### Purpose
Estimate the final total loss amount for each accident year, including both reported and unreported losses.

### Formula
```
Ultimate Loss(AY) = Reported Loss(AY) × CDF(Latest Dev→Ultimate)
```

**Where**:
- `Reported Loss(AY)` = Latest cumulative loss value for the accident year
- `Latest Dev` = Most recent development month with reported losses
- `CDF(Latest Dev→Ultimate)` = Cumulative development factor from latest point to ultimate

### Code Reference
[backend/services/loss_triangle.py:204-208](backend/services/loss_triangle.py#L204-L208)

### Example Calculation

**Scenario**:
```
Accident Year 2022:
  - Reported Loss at Dev 24 = $850,000
  - CDF(24→Ultimate) = 1.1500
```

**Calculation**:
```
Ultimate Loss(AY 2022) = $850,000 × 1.1500
                       = $977,500
```

### Interpretation
- The $850,000 currently reported will grow to $977,500 by the time all claims are settled
- The difference ($127,500) is the IBNR reserve needed
- This assumes past development patterns will continue in the future

### Key Assumptions
1. **Stability**: Historical development patterns will continue
2. **Homogeneity**: All accident years develop similarly
3. **No External Changes**: No major changes in claims handling, legal environment, etc.

### Actuarial Judgment
Actuaries may adjust this formula-based projection for:
- Known changes in claims environment
- One-time events (e.g., catastrophes)
- Changes in case reserving practices
- Regulatory or legal developments

---

## 8. IBNR (Incurred But Not Reported) Reserve

### Purpose
Estimate the amount of losses that have occurred but have not yet been reported to the insurer.

### Formula
```
IBNR(AY) = Ultimate Loss(AY) - Reported Loss(AY)
```

### Code Reference
[backend/services/loss_triangle.py:215](backend/services/loss_triangle.py#L215)

### Example Calculation

**Scenario**:
```
Accident Year 2022:
  - Ultimate Loss = $977,500
  - Reported Loss = $850,000
```

**Calculation**:
```
IBNR(AY 2022) = $977,500 - $850,000
              = $127,500
```

### Components of IBNR

The IBNR reserve technically includes two components:

1. **Pure IBNR**: Claims that have occurred but haven't been reported at all
2. **Development on Known Claims**: Additional development on already-reported claims

### Interpretation
- The company needs to set aside $127,500 in reserves for AY 2022
- This represents 15.0% of the current reported losses ($127,500 / $850,000)
- As more claims are reported, IBNR will decrease and reported losses will increase

### Regulatory Importance
- Required for financial statement accuracy (GAAP/SAP)
- Critical for rate adequacy analysis
- Key component of pricing and underwriting decisions
- Must be disclosed in Statement of Actuarial Opinion (SAO)

### Business Implications
- Affects company profitability and surplus
- Influences pricing decisions for future business
- Important for assessing underwriting year performance
- Key metric for reinsurance treaty negotiations

---

## 9. Percent Developed

### Purpose
Show the maturity of losses by measuring what percentage of ultimate losses have been reported.

### Formula
```
                                   Reported Loss(AY)
Percent Developed(AY) = ───────────────────────────── × 100%
                                  Ultimate Loss(AY)
```

### Code Reference
[backend/services/loss_triangle.py:216](backend/services/loss_triangle.py#L216)

### Example Calculation

**Scenario**:
```
Accident Year 2022:
  - Reported Loss = $850,000
  - Ultimate Loss = $977,500
```

**Calculation**:
```
Percent Developed = ($850,000 / $977,500) × 100%
                  = 0.8696 × 100%
                  = 86.96%
```

### Interpretation
- 86.96% of ultimate losses have already been reported
- 13.04% of ultimate losses are still unreported (in IBNR)
- This accident year is relatively mature

### Maturity Guidelines

**General Industry Benchmarks**:
- **0-25% Developed**: Very immature, high uncertainty
- **25-50% Developed**: Developing, significant IBNR remaining
- **50-75% Developed**: Maturing, moderate IBNR
- **75-90% Developed**: Mature, relatively stable
- **90%+ Developed**: Very mature, low IBNR uncertainty

### Factors Affecting Development Speed

**Faster Development**:
- Short-tail lines (e.g., property)
- Efficient claims handling
- Simple claim types
- Rapid reporting requirements

**Slower Development**:
- Long-tail lines (e.g., liability, workers comp)
- Complex claims
- Legal disputes
- Latent injuries (e.g., asbestos)

### Business Use
- Assess reliability of ultimate loss estimates
- Prioritize reserve review efforts
- Guide investment strategy (cash flow planning)
- Evaluate underwriting year profitability timing

---

## 10. Total Reported Losses

### Purpose
Sum all reported losses across all accident years to date.

### Formula
```
Total Reported = Σ max(Cumulative Loss(AY, all Dev))
                AY
```

Or more explicitly:
```
Total Reported = Σ Cumulative Loss(AY, Latest Dev for AY)
                AY
```

### Code Reference
[backend/services/loss_triangle.py:247](backend/services/loss_triangle.py#L247)

### Example Calculation

**Latest Cumulative Losses by Accident Year**:
```
AY 2021: $100,000 (at Dev 36 - fully developed)
AY 2022: $850,000 (at Dev 24 - still developing)
AY 2023: $650,000 (at Dev 12 - early stage)
```

**Calculation**:
```
Total Reported = $100,000 + $850,000 + $650,000
               = $1,600,000
```

### Interpretation
- This is the total amount of losses currently on the books
- Represents actual incurred losses reported to date
- Does not include IBNR (unreported losses)
- Used for financial reporting and cash management

### Financial Statement Impact
- Appears on the balance sheet as "Loss and LAE Reserves"
- Affects the income statement when reserves change
- Critical for statutory accounting (SAP) and GAAP

---

## 11. Total Ultimate Losses

### Purpose
Sum the projected final losses across all accident years, including both reported and unreported amounts.

### Formula
```
Total Ultimate = Σ Ultimate Loss(AY)
                AY
```

### Code Reference
[backend/services/loss_triangle.py:248](backend/services/loss_triangle.py#L248)

### Example Calculation

**Ultimate Losses by Accident Year**:
```
AY 2021: $115,000 (mature - small tail development)
AY 2022: $977,500 (still developing significantly)
AY 2023: $845,000 (very immature - large development ahead)
```

**Calculation**:
```
Total Ultimate = $115,000 + $977,500 + $845,000
               = $1,937,500
```

### Interpretation
- This is the expected final cost of all accident years in the portfolio
- Includes both reported losses and IBNR
- Used for pricing, rate adequacy, and profitability analysis

### Comparison to Premiums
Ultimate losses should be compared to earned premiums to calculate:
```
Loss Ratio = Total Ultimate / Earned Premium
```

For example:
```
If Earned Premium = $3,000,000
Loss Ratio = $1,937,500 / $3,000,000 = 64.6%
```

### Business Applications
- **Pricing**: Ensure rates are adequate for expected losses
- **Reserving**: Set appropriate IBNR reserves
- **Profitability**: Measure underwriting year performance
- **Reinsurance**: Determine reinsurance needs and cost

---

## 12. Total IBNR

### Purpose
Calculate the total reserve needed across all accident years for unreported losses.

### Formula

**Method 1 - Sum of Individual IBNRs**:
```
Total IBNR = Σ IBNR(AY)
            AY
```

**Method 2 - Difference**:
```
Total IBNR = Total Ultimate - Total Reported
```

### Code Reference
[backend/services/loss_triangle.py:249](backend/services/loss_triangle.py#L249)

### Example Calculation

**Using Method 1**:
```
AY 2021 IBNR: $15,000
AY 2022 IBNR: $127,500
AY 2023 IBNR: $195,000

Total IBNR = $15,000 + $127,500 + $195,000
           = $337,500
```

**Using Method 2 (verification)**:
```
Total Ultimate = $1,937,500
Total Reported = $1,600,000

Total IBNR = $1,937,500 - $1,600,000
           = $337,500 ✓
```

### Interpretation
- The company must hold $337,500 in reserves for unreported losses
- This represents 21.1% of reported losses ($337,500 / $1,600,000)
- As claims develop, IBNR will gradually convert to reported losses

### Reserve Adequacy
The IBNR percentage can indicate reserve adequacy:

- **High IBNR %**: May indicate immature years or long-tail business
- **Low IBNR %**: May indicate mature years or short-tail business
- **Declining IBNR %**: Expected as portfolio matures
- **Increasing IBNR %**: May signal deteriorating claims or reserve deficiency

### Financial Impact
- Appears on balance sheet as part of total reserves
- Changes in IBNR affect current period income
- Critical for:
  - Statutory surplus requirements
  - Investment strategy and cash flow planning
  - Management performance evaluation
  - Rate filing justification

---

## 13. Average Development Factor

### Purpose
Calculate the arithmetic mean of all age-to-age development factors to understand overall development pattern.

### Formula
```
                         1    n
Avg Dev Factor = ─── Σ  LDF(Devᵢ → Devᵢ₊₁)
                         n   i=1
```

**Where**:
- n = number of age-to-age development factors
- Typically includes all development periods (e.g., 0→1, 1→2, ..., 35→36)

### Code Reference
[backend/services/loss_triangle.py:250](backend/services/loss_triangle.py#L250)

### Example Calculation

**Development Factors**:
```
LDF(0→1)  = 1.5804
LDF(1→2)  = 1.3200
LDF(2→3)  = 1.1500
LDF(3→4)  = 1.0800
```

**Calculation**:
```
Avg Dev Factor = (1.5804 + 1.3200 + 1.1500 + 1.0800) / 4
               = 5.1304 / 4
               = 1.2826
```

### Interpretation
- On average, losses develop by a factor of 1.2826 from one period to the next
- Equivalent to average growth of 28.26% per development period
- Higher averages indicate longer-tail business

### Line of Business Comparisons

**Typical Average Development Factors**:
- **Property**: 1.05 - 1.15 (short-tail, fast development)
- **Auto Physical Damage**: 1.10 - 1.20
- **Workers Compensation**: 1.20 - 1.40 (long-tail)
- **General Liability**: 1.30 - 1.60 (very long-tail)
- **Medical Malpractice**: 1.40 - 1.80 (extremely long-tail)

### Business Applications
- Quick assessment of development pattern
- Comparison across different portfolios
- Validation of reasonableness
- Communication with non-technical stakeholders

### Limitations
- Oversimplifies complex development patterns
- Early development factors are typically much higher than late factors
- Should not be used for actual reserving calculations
- Useful primarily as a summary metric

---

## 14. Implied % Development

### Purpose
Express development factors as percentage increases for easier interpretation and communication.

### Formula
```
Implied % Development = (LDF - 1) × 100%
```

### Code Reference
[frontend/pages/1_Loss_Development.py:171](frontend/pages/1_Loss_Development.py#L171)

### Example Calculations

**Example 1**:
```
LDF(0→1) = 1.5804
Implied % Development = (1.5804 - 1) × 100%
                      = 0.5804 × 100%
                      = 58.04%
```
Interpretation: Losses increase by 58.04% from Dev 0 to Dev 1

**Example 2**:
```
LDF(24→25) = 1.0150
Implied % Development = (1.0150 - 1) × 100%
                      = 0.0150 × 100%
                      = 1.50%
```
Interpretation: Losses increase by only 1.50% from Dev 24 to Dev 25

### Development Pattern Analysis

**Typical Pattern**:
```
Dev Period    LDF      Implied %
0→1          1.5804    58.04%    (Heavy initial reporting)
1→2          1.3200    32.00%    (Still significant development)
2→3          1.1500    15.00%    (Moderate development)
3→6          1.0800     8.00%    (Slower development)
6→12         1.0300     3.00%    (Minimal development)
12→24        1.0150     1.50%    (Tail development)
24→36        1.0050     0.50%    (Very small tail)
```

### Pattern Insights

**Early Development (0-6 months)**:
- High implied % (30-60%)
- Most claims reported quickly
- Large changes period-to-period

**Middle Development (6-24 months)**:
- Moderate implied % (5-15%)
- Case reserves developing
- Some late reporting

**Tail Development (24+ months)**:
- Low implied % (0.5-3%)
- Mostly reserve development
- Rare late claims

### Business Applications
- Easier for non-actuaries to understand
- Better for presentations to management
- Helps identify unusual development patterns
- Simplifies trend analysis

---

## Chain-Ladder Method Overview

### Complete Methodology Flow

```
Step 1: Data Preparation
   ↓
   • Extract claims data (loss date, report date, amounts)
   • Calculate development months
   • Filter to maximum development period
   ↓
Step 2: Build Incremental Triangle
   ↓
   • Aggregate losses by accident year and development month
   • Create matrix with AY in rows, Dev in columns
   ↓
Step 3: Convert to Cumulative Triangle
   ↓
   • Cumsum across development periods
   • Each cell = sum of all incremental losses to date
   ↓
Step 4: Calculate Age-to-Age Factors (LDFs)
   ↓
   • For each development period transition
   • Volume-weighted: Σ(AY, Dev+1) / Σ(AY, Dev)
   • Validate reasonableness and stability
   ↓
Step 5: Calculate Cumulative Development Factors (CDFs)
   ↓
   • Product of all remaining LDFs to ultimate
   • Represents total development from current age
   ↓
Step 6: Project Ultimate Losses
   ↓
   • For each accident year
   • Ultimate = Reported × CDF(current dev to ultimate)
   ↓
Step 7: Calculate IBNR
   ↓
   • IBNR = Ultimate - Reported
   • Sum across all accident years
   ↓
Step 8: Validate and Document
   ↓
   • Review reasonableness
   • Compare to prior estimates
   • Document assumptions and judgments
```

### Mathematical Representation

The complete chain-ladder calculation for a single accident year:

```
Given:
  • R(AY, d) = Reported losses for accident year AY at development month d
  • LDF(i→i+1) = Link ratio from development i to i+1
  • d* = Current development month for AY

Calculate:
  CDF(d*→∞) = LDF(d*→d*+1) × LDF(d*+1→d*+2) × ... × LDF(n-1→n)

Project:
  U(AY) = R(AY, d*) × CDF(d*→∞)

Reserve:
  IBNR(AY) = U(AY) - R(AY, d*)
```

### Key Assumptions

1. **Stability Assumption**: Historical development patterns will continue
2. **Consistency Assumption**: All accident years develop similarly
3. **Homogeneity Assumption**: Mix of business is consistent over time
4. **Independence Assumption**: No external changes affecting development

### Limitations

1. **Past ≠ Future**: Historical patterns may not continue
2. **Mix Changes**: Portfolio composition changes affect development
3. **External Factors**: Claims inflation, legal changes, etc.
4. **Small Data**: Unstable for small claim counts
5. **Catastrophes**: Large events distort normal patterns

### When to Use Alternatives

Consider other methods when:
- **Bornhuetter-Ferguson**: When accident years are very immature
- **Cape Cod**: When exposure varies significantly by year
- **Frequency-Severity**: For more granular analysis
- **Bayesian Methods**: To incorporate external information
- **Stochastic Models**: To quantify uncertainty

### Validation Steps

1. **Diagnostic Tests**:
   - Residual analysis
   - Goodness of fit tests
   - Comparison to expected development

2. **Sensitivity Testing**:
   - Vary tail factor assumptions
   - Test different averaging periods
   - Compare volume vs. simple average

3. **Benchmarking**:
   - Compare to industry patterns
   - Review against prior year estimates
   - Assess reasonableness of growth rates

4. **Actuarial Judgment**:
   - Adjust for known changes
   - Consider qualitative factors
   - Document all adjustments

---

## Summary Table: All Metrics

| # | Metric | Formula | Code Location |
|---|--------|---------|---------------|
| 1 | Development Months | `(RY - LY) × 12 + (RM - LM)` | loss_triangle.py:45-48 |
| 2 | Incremental Triangle | `Σ Losses by (AY, Dev)` | loss_triangle.py:72-79 |
| 3 | Cumulative Triangle | `Cumsum of Incremental` | loss_triangle.py:82-83 |
| 4 | LDF (Volume-Weighted) | `Σ Cum(Dev+1) / Σ Cum(Dev)` | loss_triangle.py:166-170 |
| 5 | LDF (Simple Average) | `Mean(Cum(Dev+1) / Cum(Dev))` | loss_triangle.py:172-174 |
| 6 | CDF | `Π LDF(i→i+1)` | loss_triangle.py:204-208 |
| 7 | Ultimate Loss | `Reported × CDF` | loss_triangle.py:204-208 |
| 8 | IBNR | `Ultimate - Reported` | loss_triangle.py:215 |
| 9 | % Developed | `(Reported / Ultimate) × 100%` | loss_triangle.py:216 |
| 10 | Total Reported | `Σ Max(Cum by AY)` | loss_triangle.py:247 |
| 11 | Total Ultimate | `Σ Ultimate(AY)` | loss_triangle.py:248 |
| 12 | Total IBNR | `Σ IBNR(AY)` | loss_triangle.py:249 |
| 13 | Avg Dev Factor | `Mean(all LDFs)` | loss_triangle.py:250 |
| 14 | Implied % Dev | `(LDF - 1) × 100%` | 1_Loss_Development.py:171 |

---

## Glossary

**Accident Year (AY)**: Calendar year when the loss occurred

**Age-to-Age Factor**: See Link Development Factor

**Bornhuetter-Ferguson Method**: Alternative reserving method combining expected and actual losses

**Cape Cod Method**: Variation of BF method using on-level earned premium

**Chain-Ladder Method**: Actuarial technique using historical development patterns to project ultimate losses

**CDF (Cumulative Development Factor)**: Product of all link ratios from current development to ultimate

**Cumulative Triangle**: Loss triangle showing total losses reported to date

**Development Month**: Number of months from loss occurrence to valuation date

**IBNR (Incurred But Not Reported)**: Estimated losses for claims not yet reported plus development on known claims

**Incremental Triangle**: Loss triangle showing new losses reported in each period

**LDF (Link Development Factor)**: Ratio showing development from one age to next; also called Age-to-Age Factor

**Loss Triangle**: Matrix showing losses by accident period and development age

**Pure IBNR**: Losses for claims that have occurred but not been reported at all

**Reported Losses**: Total losses currently on the books (case reserves + paid)

**Tail Factor**: Development factor for periods beyond the observed data

**Ultimate Losses**: Projected final total losses including both reported and unreported

**Volume-Weighted Average**: Averaging method giving more weight to larger values; industry standard for LDFs

---

## References and Resources

### Actuarial Standards

- **ASOP No. 43**: Property/Casualty Unpaid Claim Estimates
- **ASOP No. 23**: Data Quality
- **ASOP No. 36**: Statements of Actuarial Opinion Regarding Property/Casualty Loss and LAE Reserves

### Industry Publications

- **CAS Exam 5/7 Study Materials**: Loss Reserving
- **Friedland, Jacqueline**: "Estimating Unpaid Claims Using Basic Techniques"
- **Mack, Thomas**: "Distribution-Free Calculation of the Standard Error of Chain Ladder Reserve Estimates"
- **Taylor, Greg**: "Loss Reserving: An Actuarial Perspective"

### Regulatory Guidance

- **NAIC Annual Statement Instructions**: Schedule P
- **SAP (Statutory Accounting Principles)**: SSAP No. 55
- **GAAP**: ASC 944

---

## Document Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-22 | Initial comprehensive documentation | Actuarial Insights Workbench Team |

---

**End of Document**
