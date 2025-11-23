"""
Loss Triangle Calculation Service
Generates loss development triangles for actuarial analysis.

Author: Actuarial Insights Workbench Team
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional


class LossTriangleCalculator:
    """
    Calculates loss development triangles from claims data.

    Supports both incremental and cumulative triangle views with
    monthly development periods up to 36 months.
    """

    def __init__(self, claims_df: pd.DataFrame, max_dev_months: int = 36):
        """
        Initialize the loss triangle calculator.

        Args:
            claims_df: DataFrame containing claims data
            max_dev_months: Maximum development months to include (default: 36)
        """
        self.claims_df = claims_df.copy()
        self.max_dev_months = max_dev_months
        self._prepare_data()

    def _prepare_data(self):
        """Prepare claims data for triangle calculation."""
        # Convert date columns to datetime
        self.claims_df['LossDate'] = pd.to_datetime(self.claims_df['LossDate'])
        self.claims_df['ReportDate'] = pd.to_datetime(self.claims_df['ReportDate'])

        # Extract accident year and month
        self.claims_df['AccidentYear'] = self.claims_df['LossDate'].dt.year
        self.claims_df['AccidentMonth'] = self.claims_df['LossDate'].dt.to_period('M')

        # Calculate development months (from loss date to report date)
        self.claims_df['DevMonths'] = (
            (self.claims_df['ReportDate'].dt.year - self.claims_df['LossDate'].dt.year) * 12 +
            (self.claims_df['ReportDate'].dt.month - self.claims_df['LossDate'].dt.month)
        )

        # Ensure development months is non-negative
        self.claims_df['DevMonths'] = self.claims_df['DevMonths'].clip(lower=0)

    def get_triangle_by_accident_year(
        self,
        value_col: str = 'IncurredAmount',
        triangle_type: str = 'cumulative'
    ) -> pd.DataFrame:
        """
        Generate loss triangle by accident year.

        Args:
            value_col: Column to aggregate ('IncurredAmount' or 'PaidAmount')
            triangle_type: 'cumulative' or 'incremental'

        Returns:
            DataFrame with accident years as rows and development months as columns
        """
        # Filter to max development months
        df_filtered = self.claims_df[self.claims_df['DevMonths'] <= self.max_dev_months].copy()

        # Group by accident year and development month
        triangle = df_filtered.groupby(['AccidentYear', 'DevMonths'])[value_col].sum().reset_index()

        # Pivot to create triangle structure
        triangle_pivot = triangle.pivot(
            index='AccidentYear',
            columns='DevMonths',
            values=value_col
        ).fillna(0)

        # Generate cumulative if requested
        if triangle_type == 'cumulative':
            triangle_pivot = triangle_pivot.cumsum(axis=1)

        # Ensure all development months are present (0 to max_dev_months)
        for month in range(self.max_dev_months + 1):
            if month not in triangle_pivot.columns:
                triangle_pivot[month] = 0

        # Sort columns
        triangle_pivot = triangle_pivot.sort_index(axis=1)

        return triangle_pivot

    def get_triangle_by_accident_month(
        self,
        value_col: str = 'IncurredAmount',
        triangle_type: str = 'cumulative',
        num_months: int = 12
    ) -> pd.DataFrame:
        """
        Generate loss triangle by accident month (more granular).

        Args:
            value_col: Column to aggregate
            triangle_type: 'cumulative' or 'incremental'
            num_months: Number of recent accident months to include

        Returns:
            DataFrame with accident months as rows and development months as columns
        """
        # Get most recent accident months
        recent_months = sorted(self.claims_df['AccidentMonth'].unique(), reverse=True)[:num_months]
        df_filtered = self.claims_df[
            (self.claims_df['AccidentMonth'].isin(recent_months)) &
            (self.claims_df['DevMonths'] <= self.max_dev_months)
        ].copy()

        # Group by accident month and development month
        triangle = df_filtered.groupby(['AccidentMonth', 'DevMonths'])[value_col].sum().reset_index()

        # Pivot to create triangle structure
        triangle_pivot = triangle.pivot(
            index='AccidentMonth',
            columns='DevMonths',
            values=value_col
        ).fillna(0)

        # Generate cumulative if requested
        if triangle_type == 'cumulative':
            triangle_pivot = triangle_pivot.cumsum(axis=1)

        # Convert period index to string for JSON serialization
        triangle_pivot.index = triangle_pivot.index.astype(str)

        return triangle_pivot

    def calculate_development_factors(
        self,
        triangle: pd.DataFrame,
        method: str = 'volume_weighted'
    ) -> pd.Series:
        """
        Calculate age-to-age development factors from a cumulative triangle.

        Args:
            triangle: Cumulative loss triangle
            method: 'volume_weighted' or 'simple_average'

        Returns:
            Series of development factors indexed by development month
        """
        factors = {}

        for i in range(len(triangle.columns) - 1):
            col_current = triangle.columns[i]
            col_next = triangle.columns[i + 1]

            # Only use rows where both periods have data
            valid_rows = (triangle[col_current] > 0) & (triangle[col_next] > 0)

            if valid_rows.sum() == 0:
                factors[f'{col_current}-{col_next}'] = 1.0
                continue

            if method == 'volume_weighted':
                # Volume-weighted average (industry standard)
                total_current = triangle.loc[valid_rows, col_current].sum()
                total_next = triangle.loc[valid_rows, col_next].sum()
                factor = total_next / total_current if total_current > 0 else 1.0
            else:
                # Simple average
                ratios = triangle.loc[valid_rows, col_next] / triangle.loc[valid_rows, col_current]
                factor = ratios.mean()

            factors[f'{col_current}-{col_next}'] = factor

        return pd.Series(factors)

    def get_ultimate_losses(
        self,
        triangle: pd.DataFrame,
        development_factors: pd.Series
    ) -> pd.DataFrame:
        """
        Project ultimate losses using development factors.

        Args:
            triangle: Cumulative loss triangle
            development_factors: Age-to-age development factors

        Returns:
            DataFrame with reported, developed, and ultimate losses
        """
        results = []

        for accident_year in triangle.index:
            # Get latest reported value (rightmost non-zero value)
            row = triangle.loc[accident_year]
            reported = row[row > 0].iloc[-1] if (row > 0).any() else 0
            latest_dev = row[row > 0].index[-1] if (row > 0).any() else 0

            # Calculate ultimate using remaining development factors
            ultimate = reported
            for factor_key, factor_value in development_factors.items():
                from_dev, to_dev = map(int, factor_key.split('-'))
                if from_dev >= latest_dev:
                    ultimate *= factor_value

            results.append({
                'AccidentYear': accident_year,
                'ReportedLoss': reported,
                'LatestDevMonth': latest_dev,
                'UltimateLoss': ultimate,
                'IBNR': ultimate - reported,
                'PercentDeveloped': (reported / ultimate * 100) if ultimate > 0 else 100
            })

        return pd.DataFrame(results)

    def get_triangle_summary(self, value_col: str = 'IncurredAmount') -> Dict:
        """
        Get comprehensive triangle summary with key metrics.

        Args:
            value_col: Column to analyze

        Returns:
            Dictionary containing triangle data and metrics
        """
        # Generate triangles
        triangle_cumulative = self.get_triangle_by_accident_year(value_col, 'cumulative')
        triangle_incremental = self.get_triangle_by_accident_year(value_col, 'incremental')

        # Calculate development factors
        dev_factors = self.calculate_development_factors(triangle_cumulative)

        # Project ultimate losses
        ultimate_df = self.get_ultimate_losses(triangle_cumulative, dev_factors)

        return {
            'cumulative_triangle': triangle_cumulative.to_dict(),
            'incremental_triangle': triangle_incremental.to_dict(),
            'development_factors': dev_factors.to_dict(),
            'ultimate_projections': ultimate_df.to_dict('records'),
            'summary_stats': {
                'total_reported': float(triangle_cumulative.max(axis=1).sum()),
                'total_ultimate': float(ultimate_df['UltimateLoss'].sum()),
                'total_ibnr': float(ultimate_df['IBNR'].sum()),
                'avg_dev_factor': float(dev_factors.mean()) if len(dev_factors) > 0 else 1.0
            }
        }


def calculate_loss_triangle(
    claims_df: pd.DataFrame,
    triangle_type: str = 'cumulative',
    value_col: str = 'IncurredAmount',
    max_dev_months: int = 36
) -> Dict:
    """
    Convenience function to calculate loss triangle.

    Args:
        claims_df: DataFrame with claims data
        triangle_type: 'cumulative' or 'incremental'
        value_col: Column to aggregate
        max_dev_months: Maximum development months

    Returns:
        Dictionary containing triangle and related metrics
    """
    calculator = LossTriangleCalculator(claims_df, max_dev_months)
    return calculator.get_triangle_summary(value_col)
