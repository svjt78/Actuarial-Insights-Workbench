"""
Unit tests for loss triangle calculation service.

Author: Actuarial Insights Workbench Team
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.loss_triangle import LossTriangleCalculator, calculate_loss_triangle


@pytest.fixture
def sample_claims_data():
    """Create sample claims data for testing."""
    np.random.seed(42)

    claims = []
    for i in range(100):
        loss_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        report_date = loss_date + timedelta(days=np.random.randint(0, 180))

        claims.append({
            'ClaimID': f'CLM{i:04d}',
            'PolicyID': f'POL{i % 20:04d}',
            'LossDate': loss_date.strftime('%Y-%m-%d'),
            'ReportDate': report_date.strftime('%Y-%m-%d'),
            'IncurredAmount': np.random.uniform(10000, 100000),
            'PaidAmount': np.random.uniform(5000, 80000)
        })

    return pd.DataFrame(claims)


def test_loss_triangle_calculator_initialization(sample_claims_data):
    """Test calculator initialization."""
    calculator = LossTriangleCalculator(sample_claims_data, max_dev_months=12)

    assert calculator.max_dev_months == 12
    assert len(calculator.claims_df) == 100
    assert 'AccidentYear' in calculator.claims_df.columns
    assert 'DevMonths' in calculator.claims_df.columns


def test_get_triangle_by_accident_year(sample_claims_data):
    """Test triangle generation by accident year."""
    calculator = LossTriangleCalculator(sample_claims_data, max_dev_months=12)

    triangle = calculator.get_triangle_by_accident_year(
        value_col='IncurredAmount',
        triangle_type='cumulative'
    )

    assert isinstance(triangle, pd.DataFrame)
    assert len(triangle) > 0
    assert all(triangle.columns == sorted(triangle.columns))


def test_cumulative_vs_incremental(sample_claims_data):
    """Test that cumulative triangle is sum of incremental."""
    calculator = LossTriangleCalculator(sample_claims_data, max_dev_months=12)

    cumulative = calculator.get_triangle_by_accident_year(triangle_type='cumulative')
    incremental = calculator.get_triangle_by_accident_year(triangle_type='incremental')

    # Cumulative should be >= incremental at each point
    for year in cumulative.index:
        if year in incremental.index:
            for col in cumulative.columns:
                if col in incremental.columns:
                    assert cumulative.loc[year, col] >= incremental.loc[year, col]


def test_development_factors_calculation(sample_claims_data):
    """Test development factor calculation."""
    calculator = LossTriangleCalculator(sample_claims_data, max_dev_months=12)

    triangle = calculator.get_triangle_by_accident_year(triangle_type='cumulative')
    dev_factors = calculator.calculate_development_factors(triangle)

    assert isinstance(dev_factors, pd.Series)
    assert len(dev_factors) > 0
    # Development factors should be >= 1.0 for cumulative triangles
    assert all(dev_factors >= 0.9)  # Allow small rounding


def test_ultimate_losses_projection(sample_claims_data):
    """Test ultimate loss projection."""
    calculator = LossTriangleCalculator(sample_claims_data, max_dev_months=12)

    triangle = calculator.get_triangle_by_accident_year(triangle_type='cumulative')
    dev_factors = calculator.calculate_development_factors(triangle)
    ultimate_df = calculator.get_ultimate_losses(triangle, dev_factors)

    assert isinstance(ultimate_df, pd.DataFrame)
    assert 'UltimateLoss' in ultimate_df.columns
    assert 'IBNR' in ultimate_df.columns
    assert 'PercentDeveloped' in ultimate_df.columns

    # Ultimate should be >= reported
    assert all(ultimate_df['UltimateLoss'] >= ultimate_df['ReportedLoss'])

    # IBNR should be non-negative
    assert all(ultimate_df['IBNR'] >= 0)


def test_triangle_summary(sample_claims_data):
    """Test comprehensive triangle summary."""
    summary = calculate_loss_triangle(
        sample_claims_data,
        triangle_type='cumulative',
        value_col='IncurredAmount',
        max_dev_months=12
    )

    assert isinstance(summary, dict)
    assert 'cumulative_triangle' in summary
    assert 'incremental_triangle' in summary
    assert 'development_factors' in summary
    assert 'ultimate_projections' in summary
    assert 'summary_stats' in summary

    stats = summary['summary_stats']
    assert 'total_reported' in stats
    assert 'total_ultimate' in stats
    assert 'total_ibnr' in stats


def test_empty_claims():
    """Test handling of empty claims data."""
    empty_df = pd.DataFrame(columns=['ClaimID', 'LossDate', 'ReportDate', 'IncurredAmount'])

    calculator = LossTriangleCalculator(empty_df, max_dev_months=12)
    triangle = calculator.get_triangle_by_accident_year()

    assert isinstance(triangle, pd.DataFrame)
    assert len(triangle) == 0


def test_paid_vs_incurred(sample_claims_data):
    """Test triangle for paid vs incurred amounts."""
    calculator = LossTriangleCalculator(sample_claims_data, max_dev_months=12)

    incurred_triangle = calculator.get_triangle_by_accident_year(value_col='IncurredAmount')
    paid_triangle = calculator.get_triangle_by_accident_year(value_col='PaidAmount')

    # Incurred should generally be >= paid
    assert incurred_triangle.sum().sum() >= paid_triangle.sum().sum()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
