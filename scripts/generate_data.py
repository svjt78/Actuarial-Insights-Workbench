"""
Data Generation Script for Actuarial Insights Workbench
Generates synthetic Commercial Property insurance data for the MVP.

Author: Actuarial Insights Workbench Team
Date: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
NUM_POLICIES = 1000
NUM_CLAIMS_MIN = 100
NUM_CLAIMS_MAX = 200
ACCIDENT_YEARS = [2022, 2023, 2024]
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Geography options (US regions)
GEOGRAPHIES = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West', 'Northwest']
GEOGRAPHY_WEIGHTS = [0.20, 0.18, 0.22, 0.15, 0.15, 0.10]

# Industry sectors for Commercial Property
INDUSTRIES = [
    'Manufacturing', 'Retail', 'Office', 'Warehouse',
    'Healthcare', 'Education', 'Hospitality', 'Technology'
]
INDUSTRY_WEIGHTS = [0.15, 0.18, 0.20, 0.12, 0.10, 0.08, 0.10, 0.07]

# Policy size categories
POLICY_SIZES = ['Small', 'Medium', 'Large', 'Enterprise']
POLICY_SIZE_WEIGHTS = [0.40, 0.35, 0.20, 0.05]

def generate_risk_rating():
    """
    Generate a composite COPE-based risk rating score (1-10).
    Higher score = higher risk

    COPE factors considered (simplified):
    - Construction: Building materials and fire resistance
    - Occupancy: Type of business and hazard level
    - Protection: Fire protection and security systems
    - Exposure: Proximity to hazards and natural disaster risk
    """
    # Generate individual COPE components (1-10 scale)
    construction_risk = np.random.triangular(2, 5, 8)
    occupancy_risk = np.random.triangular(2, 5, 8)
    protection_risk = np.random.triangular(2, 5, 9)  # Higher variance
    exposure_risk = np.random.triangular(1, 4, 7)

    # Weighted composite score
    composite_score = (
        construction_risk * 0.30 +
        occupancy_risk * 0.25 +
        protection_risk * 0.25 +
        exposure_risk * 0.20
    )

    return round(composite_score, 2)

def generate_premium(policy_size, risk_rating, geography, industry):
    """
    Generate annual premium based on policy characteristics.
    Formula considers size, risk, geography, and industry factors.
    """
    # Base premium by size
    base_premiums = {
        'Small': 5000,
        'Medium': 25000,
        'Large': 100000,
        'Enterprise': 500000
    }

    base = base_premiums[policy_size]

    # Risk multiplier (1.0 to 2.0 based on rating)
    risk_multiplier = 0.7 + (risk_rating / 10) * 1.3

    # Geography factor
    geography_factors = {
        'Northeast': 1.1,  # Higher cost region
        'Southeast': 1.05,  # Hurricane exposure
        'Midwest': 0.95,
        'Southwest': 1.0,
        'West': 1.15,  # Earthquake/wildfire
        'Northwest': 1.0
    }

    # Industry factor
    industry_factors = {
        'Manufacturing': 1.2,  # Higher hazard
        'Retail': 1.0,
        'Office': 0.9,  # Lower hazard
        'Warehouse': 1.1,
        'Healthcare': 1.05,
        'Education': 0.95,
        'Hospitality': 1.1,
        'Technology': 0.95
    }

    premium = (
        base *
        risk_multiplier *
        geography_factors[geography] *
        industry_factors[industry] *
        np.random.uniform(0.9, 1.1)  # Random variation
    )

    return round(premium, 2)

def generate_policies():
    """Generate synthetic policy data."""
    print("Generating policies...")

    policies = []

    for i in range(NUM_POLICIES):
        policy_id = f"POL{str(i+1).zfill(6)}"

        # Random effective date within the date range
        days_offset = np.random.randint(0, (END_DATE - START_DATE).days)
        effective_date = START_DATE + timedelta(days=days_offset)

        # Policy characteristics
        geography = np.random.choice(GEOGRAPHIES, p=GEOGRAPHY_WEIGHTS)
        industry = np.random.choice(INDUSTRIES, p=INDUSTRY_WEIGHTS)
        policy_size = np.random.choice(POLICY_SIZES, p=POLICY_SIZE_WEIGHTS)
        risk_rating = generate_risk_rating()
        premium = generate_premium(policy_size, risk_rating, geography, industry)

        # Exposure units (e.g., building value in $100k units)
        exposure_base = {'Small': 10, 'Medium': 50, 'Large': 200, 'Enterprise': 1000}
        exposure = exposure_base[policy_size] * np.random.uniform(0.8, 1.2)

        policies.append({
            'PolicyID': policy_id,
            'EffectiveDate': effective_date.strftime('%Y-%m-%d'),
            'Geography': geography,
            'Industry': industry,
            'PolicySize': policy_size,
            'RiskRating': risk_rating,
            'AnnualPremium': premium,
            'ExposureUnits': round(exposure, 2)
        })

    df = pd.DataFrame(policies)
    print(f"Generated {len(df)} policies")
    return df

def generate_claims(policies_df):
    """Generate synthetic claims data."""
    print("Generating claims...")

    # Determine number of claims
    num_claims = np.random.randint(NUM_CLAIMS_MIN, NUM_CLAIMS_MAX + 1)

    # Select random policies to have claims (some policies may have multiple claims)
    claim_policies = np.random.choice(
        policies_df['PolicyID'].values,
        size=num_claims,
        replace=True
    )

    claims = []

    for i, policy_id in enumerate(claim_policies):
        claim_id = f"CLM{str(i+1).zfill(6)}"

        # Get policy info
        policy = policies_df[policies_df['PolicyID'] == policy_id].iloc[0]
        effective_date = datetime.strptime(policy['EffectiveDate'], '%Y-%m-%d')

        # Loss date (after effective date, within policy period)
        max_days = min(365, (END_DATE - effective_date).days)
        if max_days > 0:
            loss_date = effective_date + timedelta(days=np.random.randint(0, max_days))
        else:
            loss_date = effective_date

        # Report date (0-90 days after loss)
        report_lag = np.random.randint(0, 91)
        report_date = loss_date + timedelta(days=report_lag)

        # Claim severity based on risk rating and policy size
        risk_factor = policy['RiskRating'] / 5.0  # Normalize
        size_base = {
            'Small': 10000,
            'Medium': 50000,
            'Large': 200000,
            'Enterprise': 1000000
        }

        # Use lognormal distribution for claim amounts
        mean_claim = size_base[policy['PolicySize']] * risk_factor
        std_claim = mean_claim * 0.8

        incurred_amount = np.random.lognormal(
            np.log(mean_claim / np.sqrt(1 + (std_claim/mean_claim)**2)),
            np.sqrt(np.log(1 + (std_claim/mean_claim)**2))
        )

        # Paid amount (60-100% of incurred, depending on development)
        development_pct = np.random.uniform(0.60, 1.0)
        paid_amount = incurred_amount * development_pct

        # Claim status
        if development_pct > 0.95:
            status = 'Closed'
        elif development_pct > 0.75:
            status = 'Open - Developed'
        else:
            status = 'Open - Developing'

        claims.append({
            'ClaimID': claim_id,
            'PolicyID': policy_id,
            'LossDate': loss_date.strftime('%Y-%m-%d'),
            'ReportDate': report_date.strftime('%Y-%m-%d'),
            'Geography': policy['Geography'],
            'Industry': policy['Industry'],
            'PolicySize': policy['PolicySize'],
            'RiskRating': policy['RiskRating'],
            'IncurredAmount': round(incurred_amount, 2),
            'PaidAmount': round(paid_amount, 2),
            'ClaimStatus': status
        })

    df = pd.DataFrame(claims)
    print(f"Generated {len(df)} claims")
    return df

def generate_exposure(policies_df):
    """Generate monthly exposure data for each policy."""
    print("Generating exposure data...")

    exposure_records = []

    for _, policy in policies_df.iterrows():
        effective_date = datetime.strptime(policy['EffectiveDate'], '%Y-%m-%d')

        # Generate monthly exposure for policy duration
        current_date = effective_date
        month_counter = 0

        while current_date <= END_DATE and month_counter < 36:  # Max 3 years
            # First day of the month
            period_start = current_date.replace(day=1)
            period_key = period_start.strftime('%Y-%m')

            # Calculate earned premium (monthly)
            monthly_premium = policy['AnnualPremium'] / 12

            # Exposure may vary slightly month to month
            monthly_exposure = policy['ExposureUnits'] * np.random.uniform(0.95, 1.05)

            exposure_records.append({
                'PolicyID': policy['PolicyID'],
                'Period': period_key,
                'EarnedPremium': round(monthly_premium, 2),
                'ExposureUnits': round(monthly_exposure, 2),
                'Geography': policy['Geography'],
                'Industry': policy['Industry'],
                'PolicySize': policy['PolicySize'],
                'RiskRating': policy['RiskRating']
            })

            # Move to next month using relativedelta to handle month boundaries
            current_date = current_date + relativedelta(months=1)
            month_counter += 1

    df = pd.DataFrame(exposure_records)
    print(f"Generated {len(df)} exposure records")
    return df

def main():
    """Main execution function."""
    print("=" * 60)
    print("Actuarial Insights Workbench - Data Generation")
    print("=" * 60)
    print()

    # Create data directory if it doesn't exist
    os.makedirs('../data', exist_ok=True)

    # Generate datasets
    policies_df = generate_policies()
    claims_df = generate_claims(policies_df)
    exposure_df = generate_exposure(policies_df)

    # Save to CSV
    print("\nSaving datasets...")
    policies_df.to_csv('../data/policies.csv', index=False)
    claims_df.to_csv('../data/claims.csv', index=False)
    exposure_df.to_csv('../data/exposure.csv', index=False)

    # Print summary statistics
    print("\n" + "=" * 60)
    print("DATA GENERATION SUMMARY")
    print("=" * 60)
    print(f"\nPolicies: {len(policies_df)}")
    print(f"  - Date Range: {policies_df['EffectiveDate'].min()} to {policies_df['EffectiveDate'].max()}")
    print(f"  - Total Premium: ${policies_df['AnnualPremium'].sum():,.2f}")
    print(f"  - Avg Premium: ${policies_df['AnnualPremium'].mean():,.2f}")

    print(f"\nClaims: {len(claims_df)}")
    print(f"  - Total Incurred: ${claims_df['IncurredAmount'].sum():,.2f}")
    print(f"  - Total Paid: ${claims_df['PaidAmount'].sum():,.2f}")
    print(f"  - Avg Severity: ${claims_df['IncurredAmount'].mean():,.2f}")

    print(f"\nExposure Records: {len(exposure_df)}")
    print(f"  - Total Earned Premium: ${exposure_df['EarnedPremium'].sum():,.2f}")

    # Calculate overall loss ratio
    total_incurred = claims_df['IncurredAmount'].sum()
    total_earned = exposure_df['EarnedPremium'].sum()
    loss_ratio = (total_incurred / total_earned) * 100 if total_earned > 0 else 0

    print(f"\nOverall Loss Ratio: {loss_ratio:.2f}%")

    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
