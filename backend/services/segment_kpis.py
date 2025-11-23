"""
Segment KPIs Calculation Service
Calculates key performance indicators by underwriting segment.

Author: Actuarial Insights Workbench Team
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class SegmentKPICalculator:
    """
    Calculates actuarial and underwriting KPIs by segment.

    Supports segmentation by Geography, Industry, Policy Size, and Risk Rating.
    Calculates Loss Ratio, Frequency, Severity, and other key metrics.
    """

    def __init__(self, policies_df: pd.DataFrame, claims_df: pd.DataFrame, exposure_df: pd.DataFrame):
        """
        Initialize the segment KPI calculator.

        Args:
            policies_df: DataFrame containing policy data
            claims_df: DataFrame containing claims data
            exposure_df: DataFrame containing exposure/premium data
        """
        self.policies_df = policies_df.copy()
        self.claims_df = claims_df.copy()
        self.exposure_df = exposure_df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Prepare data for KPI calculations."""
        # Convert date columns
        if 'LossDate' in self.claims_df.columns:
            self.claims_df['LossDate'] = pd.to_datetime(self.claims_df['LossDate'])
            self.claims_df['LossYear'] = self.claims_df['LossDate'].dt.year

    def calculate_kpis_by_segment(
        self,
        segment_by: str,
        min_premium: float = 0
    ) -> pd.DataFrame:
        """
        Calculate comprehensive KPIs for each segment.

        Args:
            segment_by: Dimension to segment by ('Geography', 'Industry', 'PolicySize', 'RiskRating')
            min_premium: Minimum earned premium to include segment

        Returns:
            DataFrame with KPIs by segment
        """
        if segment_by not in ['Geography', 'Industry', 'PolicySize', 'RiskRating']:
            raise ValueError(f"Invalid segment_by value: {segment_by}")

        # Aggregate exposure and premium by segment
        exposure_agg = self.exposure_df.groupby(segment_by).agg({
            'EarnedPremium': 'sum',
            'ExposureUnits': 'sum',
            'PolicyID': 'nunique'
        }).reset_index()

        exposure_agg.columns = [segment_by, 'EarnedPremium', 'TotalExposure', 'PolicyCount']

        # Aggregate claims by segment
        claims_agg = self.claims_df.groupby(segment_by).agg({
            'IncurredAmount': 'sum',
            'PaidAmount': 'sum',
            'ClaimID': 'count'
        }).reset_index()

        claims_agg.columns = [segment_by, 'IncurredLoss', 'PaidLoss', 'ClaimCount']

        # Merge exposure and claims
        kpis = exposure_agg.merge(claims_agg, on=segment_by, how='left')

        # Fill NaN values (segments with no claims)
        kpis[['IncurredLoss', 'PaidLoss', 'ClaimCount']] = \
            kpis[['IncurredLoss', 'PaidLoss', 'ClaimCount']].fillna(0)

        # Calculate KPIs
        kpis['LossRatio'] = (kpis['IncurredLoss'] / kpis['EarnedPremium'] * 100).round(2)
        kpis['PaidLossRatio'] = (kpis['PaidLoss'] / kpis['EarnedPremium'] * 100).round(2)

        # Frequency (claims per 100 exposure units)
        kpis['Frequency'] = (kpis['ClaimCount'] / kpis['TotalExposure'] * 100).round(4)

        # Severity (average claim amount)
        kpis['Severity'] = (kpis['IncurredLoss'] / kpis['ClaimCount']).fillna(0).round(2)

        # Pure Premium (loss cost per exposure unit)
        kpis['PurePremium'] = (kpis['IncurredLoss'] / kpis['TotalExposure']).round(2)

        # Average Premium per Policy
        kpis['AvgPremium'] = (kpis['EarnedPremium'] / kpis['PolicyCount']).round(2)

        # Filter by minimum premium
        kpis = kpis[kpis['EarnedPremium'] >= min_premium]

        # Sort by earned premium (largest first)
        kpis = kpis.sort_values('EarnedPremium', ascending=False)

        return kpis

    def calculate_overall_kpis(self) -> Dict:
        """
        Calculate portfolio-level KPIs (all segments combined).

        Returns:
            Dictionary containing overall portfolio metrics
        """
        total_earned_premium = self.exposure_df['EarnedPremium'].sum()
        total_exposure = self.exposure_df['ExposureUnits'].sum()
        total_policies = self.policies_df['PolicyID'].nunique()

        total_incurred = self.claims_df['IncurredAmount'].sum()
        total_paid = self.claims_df['PaidAmount'].sum()
        total_claims = len(self.claims_df)

        loss_ratio = (total_incurred / total_earned_premium * 100) if total_earned_premium > 0 else 0
        paid_loss_ratio = (total_paid / total_earned_premium * 100) if total_earned_premium > 0 else 0
        frequency = (total_claims / total_exposure * 100) if total_exposure > 0 else 0
        severity = (total_incurred / total_claims) if total_claims > 0 else 0
        pure_premium = (total_incurred / total_exposure) if total_exposure > 0 else 0

        return {
            'total_earned_premium': round(total_earned_premium, 2),
            'total_incurred_loss': round(total_incurred, 2),
            'total_paid_loss': round(total_paid, 2),
            'total_exposure': round(total_exposure, 2),
            'policy_count': int(total_policies),
            'claim_count': int(total_claims),
            'loss_ratio': round(loss_ratio, 2),
            'paid_loss_ratio': round(paid_loss_ratio, 2),
            'frequency': round(frequency, 4),
            'severity': round(severity, 2),
            'pure_premium': round(pure_premium, 2),
            'avg_premium_per_policy': round(total_earned_premium / total_policies, 2) if total_policies > 0 else 0
        }

    def calculate_trend_analysis(
        self,
        segment_by: str,
        time_period: str = 'year'
    ) -> pd.DataFrame:
        """
        Calculate KPI trends over time by segment.

        Args:
            segment_by: Dimension to segment by
            time_period: 'year' or 'quarter'

        Returns:
            DataFrame with KPIs by segment and time period
        """
        # Add time period to exposure data
        exposure_with_time = self.exposure_df.copy()
        exposure_with_time['Period'] = pd.to_datetime(exposure_with_time['Period'])

        if time_period == 'year':
            exposure_with_time['TimePeriod'] = exposure_with_time['Period'].dt.year
        else:
            exposure_with_time['TimePeriod'] = exposure_with_time['Period'].dt.to_period('Q').astype(str)

        # Aggregate by segment and time
        trend_exposure = exposure_with_time.groupby([segment_by, 'TimePeriod']).agg({
            'EarnedPremium': 'sum',
            'ExposureUnits': 'sum'
        }).reset_index()

        # Add time period to claims
        claims_with_time = self.claims_df.copy()
        if time_period == 'year':
            claims_with_time['TimePeriod'] = claims_with_time['LossYear']
        else:
            claims_with_time['TimePeriod'] = pd.to_datetime(
                claims_with_time['LossDate']
            ).dt.to_period('Q').astype(str)

        # Aggregate claims by segment and time
        trend_claims = claims_with_time.groupby([segment_by, 'TimePeriod']).agg({
            'IncurredAmount': 'sum',
            'ClaimID': 'count'
        }).reset_index()

        trend_claims.columns = [segment_by, 'TimePeriod', 'IncurredLoss', 'ClaimCount']

        # Merge
        trend_df = trend_exposure.merge(
            trend_claims,
            on=[segment_by, 'TimePeriod'],
            how='left'
        )

        # Fill NaN
        trend_df[['IncurredLoss', 'ClaimCount']] = trend_df[['IncurredLoss', 'ClaimCount']].fillna(0)

        # Calculate KPIs
        trend_df['LossRatio'] = (trend_df['IncurredLoss'] / trend_df['EarnedPremium'] * 100).round(2)
        trend_df['Frequency'] = (trend_df['ClaimCount'] / trend_df['ExposureUnits'] * 100).round(4)
        trend_df['Severity'] = (trend_df['IncurredLoss'] / trend_df['ClaimCount']).fillna(0).round(2)

        return trend_df

    def get_top_segments(
        self,
        segment_by: str,
        metric: str = 'EarnedPremium',
        top_n: int = 10
    ) -> pd.DataFrame:
        """
        Get top N segments by specified metric.

        Args:
            segment_by: Dimension to segment by
            metric: Metric to rank by ('EarnedPremium', 'LossRatio', 'ClaimCount', etc.)
            top_n: Number of top segments to return

        Returns:
            DataFrame with top segments
        """
        kpis = self.calculate_kpis_by_segment(segment_by)

        if metric not in kpis.columns:
            raise ValueError(f"Metric {metric} not found in KPIs")

        return kpis.nlargest(top_n, metric)

    def get_segment_comparison(self, segments: List[str]) -> Dict:
        """
        Compare KPIs across multiple segment dimensions.

        Args:
            segments: List of segment dimensions to compare

        Returns:
            Dictionary with KPIs for each segment dimension
        """
        comparison = {}

        for segment in segments:
            if segment in ['Geography', 'Industry', 'PolicySize', 'RiskRating']:
                comparison[segment] = self.calculate_kpis_by_segment(segment).to_dict('records')

        comparison['overall'] = self.calculate_overall_kpis()

        return comparison


def calculate_segment_kpis(
    policies_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    exposure_df: pd.DataFrame,
    segment_by: str = 'Geography'
) -> Dict:
    """
    Convenience function to calculate segment KPIs.

    Args:
        policies_df: Policies DataFrame
        claims_df: Claims DataFrame
        exposure_df: Exposure DataFrame
        segment_by: Segment dimension

    Returns:
        Dictionary with KPIs and overall metrics
    """
    calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)

    return {
        'segment_kpis': calculator.calculate_kpis_by_segment(segment_by).to_dict('records'),
        'overall_kpis': calculator.calculate_overall_kpis()
    }
