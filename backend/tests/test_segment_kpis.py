"""
Unit tests for segment KPIs calculation service.

Author: Actuarial Insights Workbench Team
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.segment_kpis import SegmentKPICalculator, calculate_segment_kpis


@pytest.fixture
def sample_data():
    """Create sample policies, claims, and exposure data."""
    np.random.seed(42)

    # Policies
    policies = []
    for i in range(50):
        policies.append({
            'PolicyID': f'POL{i:04d}',
            'EffectiveDate': '2023-01-01',
            'Geography': np.random.choice(['Northeast', 'Southeast', 'Midwest']),
            'Industry': np.random.choice(['Manufacturing', 'Retail', 'Office']),
            'PolicySize': np.random.choice(['Small', 'Medium', 'Large']),
            'RiskRating': np.random.uniform(3, 8),
            'AnnualPremium': np.random.uniform(10000, 100000),
            'ExposureUnits': np.random.uniform(10, 100)
        })

    policies_df = pd.DataFrame(policies)

    # Claims (20% of policies have claims)
    claims = []
    for i in range(10):
        claims.append({
            'ClaimID': f'CLM{i:04d}',
            'PolicyID': f'POL{i * 5:04d}',
            'LossDate': '2023-06-01',
            'Geography': policies[i * 5]['Geography'],
            'Industry': policies[i * 5]['Industry'],
            'PolicySize': policies[i * 5]['PolicySize'],
            'RiskRating': policies[i * 5]['RiskRating'],
            'IncurredAmount': np.random.uniform(10000, 50000),
            'PaidAmount': np.random.uniform(5000, 40000)
        })

    claims_df = pd.DataFrame(claims)

    # Exposure
    exposure = []
    for policy in policies:
        for month in range(12):
            exposure.append({
                'PolicyID': policy['PolicyID'],
                'Period': f'2023-{month + 1:02d}',
                'EarnedPremium': policy['AnnualPremium'] / 12,
                'ExposureUnits': policy['ExposureUnits'],
                'Geography': policy['Geography'],
                'Industry': policy['Industry'],
                'PolicySize': policy['PolicySize'],
                'RiskRating': policy['RiskRating']
            })

    exposure_df = pd.DataFrame(exposure)

    return policies_df, claims_df, exposure_df


def test_segment_kpi_calculator_initialization(sample_data):
    """Test calculator initialization."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)

    assert len(calculator.policies_df) == 50
    assert len(calculator.claims_df) == 10
    assert len(calculator.exposure_df) == 600  # 50 policies * 12 months


def test_calculate_kpis_by_geography(sample_data):
    """Test KPI calculation by geography."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)
    kpis = calculator.calculate_kpis_by_segment('Geography')

    assert isinstance(kpis, pd.DataFrame)
    assert 'Geography' in kpis.columns
    assert 'LossRatio' in kpis.columns
    assert 'Frequency' in kpis.columns
    assert 'Severity' in kpis.columns
    assert 'EarnedPremium' in kpis.columns

    # Check that metrics are reasonable
    assert all(kpis['LossRatio'] >= 0)
    assert all(kpis['Frequency'] >= 0)
    assert all(kpis['Severity'] >= 0)


def test_calculate_kpis_by_industry(sample_data):
    """Test KPI calculation by industry."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)
    kpis = calculator.calculate_kpis_by_segment('Industry')

    assert isinstance(kpis, pd.DataFrame)
    assert 'Industry' in kpis.columns
    assert len(kpis) <= 3  # Max 3 industries in sample data


def test_overall_kpis(sample_data):
    """Test overall portfolio KPIs."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)
    overall = calculator.calculate_overall_kpis()

    assert isinstance(overall, dict)
    assert 'total_earned_premium' in overall
    assert 'loss_ratio' in overall
    assert 'frequency' in overall
    assert 'severity' in overall
    assert 'policy_count' in overall
    assert 'claim_count' in overall

    # Verify calculations
    assert overall['policy_count'] == 50
    assert overall['claim_count'] == 10
    assert overall['loss_ratio'] >= 0


def test_min_premium_filter(sample_data):
    """Test minimum premium filtering."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)

    # With no filter
    kpis_all = calculator.calculate_kpis_by_segment('Geography', min_premium=0)

    # With high filter
    kpis_filtered = calculator.calculate_kpis_by_segment('Geography', min_premium=100000000)

    assert len(kpis_all) >= len(kpis_filtered)


def test_top_segments(sample_data):
    """Test top segments identification."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)

    top_by_premium = calculator.get_top_segments(
        segment_by='Geography',
        metric='EarnedPremium',
        top_n=2
    )

    assert isinstance(top_by_premium, pd.DataFrame)
    assert len(top_by_premium) <= 2


def test_segment_comparison(sample_data):
    """Test segment comparison across dimensions."""
    policies_df, claims_df, exposure_df = sample_data

    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)

    comparison = calculator.get_segment_comparison(['Geography', 'Industry'])

    assert isinstance(comparison, dict)
    assert 'Geography' in comparison
    assert 'Industry' in comparison
    assert 'overall' in comparison


def test_convenience_function(sample_data):
    """Test convenience function for KPI calculation."""
    policies_df, claims_df, exposure_df = sample_data

    result = calculate_segment_kpis(
        policies_df,
        claims_df,
        exposure_df,
        segment_by='Geography'
    )

    assert isinstance(result, dict)
    assert 'segment_kpis' in result
    assert 'overall_kpis' in result


def test_empty_claims_handling(sample_data):
    """Test handling of segments with no claims."""
    policies_df, _, exposure_df = sample_data

    # Empty claims DataFrame
    empty_claims = pd.DataFrame(columns=['ClaimID', 'PolicyID', 'IncurredAmount', 'PaidAmount'])

    calculator = SegmentKPICalculator(policies_df, empty_claims, exposure_df)
    kpis = calculator.calculate_kpis_by_segment('Geography')

    # Should handle empty claims gracefully
    assert all(kpis['LossRatio'] == 0)
    assert all(kpis['ClaimCount'] == 0)
    assert all(kpis['Severity'] == 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
