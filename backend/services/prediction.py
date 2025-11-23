"""
Prediction Service
Handles ML model predictions for Loss Ratio and Claim Severity.

Author: Actuarial Insights Workbench Team
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import joblib
import os
from pathlib import Path


class PredictionService:
    """
    Service for making predictions using trained ML models.

    Supports Loss Ratio and Severity predictions using LightGBM models.
    """

    def __init__(self, models_dir: str = "models"):
        """
        Initialize the prediction service.

        Args:
            models_dir: Directory containing trained model files
        """
        self.models_dir = Path(models_dir)
        self.lr_model = None
        self.severity_model = None
        self.feature_names = None

        # Load models if they exist
        self._load_models()

    def _load_models(self):
        """Load trained models from disk."""
        lr_model_path = self.models_dir / "lr_model.pkl"
        severity_model_path = self.models_dir / "severity_model.pkl"

        if lr_model_path.exists():
            self.lr_model = joblib.load(lr_model_path)
            print(f"Loaded Loss Ratio model from {lr_model_path}")

        if severity_model_path.exists():
            self.severity_model = joblib.load(severity_model_path)
            print(f"Loaded Severity model from {severity_model_path}")

    def prepare_features(self, input_data: Dict) -> pd.DataFrame:
        """
        Prepare features from input data.

        Args:
            input_data: Dictionary with input features

        Returns:
            DataFrame with prepared features
        """
        # Geography encoding
        geography_map = {
            'Northeast': 0, 'Southeast': 1, 'Midwest': 2,
            'Southwest': 3, 'West': 4, 'Northwest': 5
        }

        # Industry encoding
        industry_map = {
            'Manufacturing': 0, 'Retail': 1, 'Office': 2, 'Warehouse': 3,
            'Healthcare': 4, 'Education': 5, 'Hospitality': 6, 'Technology': 7
        }

        # Policy size encoding
        policy_size_map = {'Small': 0, 'Medium': 1, 'Large': 2, 'Enterprise': 3}

        features = {
            'RiskRating': input_data.get('risk_rating', 5.0),
            'Geography': geography_map.get(input_data.get('geography', 'Midwest'), 2),
            'Industry': industry_map.get(input_data.get('industry', 'Office'), 2),
            'PolicySize': policy_size_map.get(input_data.get('policy_size', 'Medium'), 1),
            'ExposureUnits': input_data.get('exposure_units', 50.0),
            'AnnualPremium': input_data.get('annual_premium', 25000.0)
        }

        return pd.DataFrame([features])

    def predict_loss_ratio(self, input_data: Dict) -> Dict:
        """
        Predict expected loss ratio.

        Args:
            input_data: Input features dictionary

        Returns:
            Dictionary with prediction and confidence interval
        """
        if self.lr_model is None:
            # Return dummy prediction if model not loaded
            return {
                'predicted_loss_ratio': 65.0,
                'confidence_interval': [50.0, 80.0],
                'model_loaded': False,
                'message': 'Model not loaded - using default estimate'
            }

        features_df = self.prepare_features(input_data)

        try:
            prediction = self.lr_model.predict(features_df)[0]

            # Calculate confidence interval (simplified)
            # In production, you'd use proper confidence intervals from the model
            confidence_interval = [
                max(0, prediction - 15),
                min(100, prediction + 15)
            ]

            return {
                'predicted_loss_ratio': round(float(prediction), 2),
                'confidence_interval': [round(ci, 2) for ci in confidence_interval],
                'model_loaded': True,
                'input_features': input_data
            }

        except Exception as e:
            return {
                'error': str(e),
                'model_loaded': True,
                'message': 'Prediction failed'
            }

    def predict_severity(self, input_data: Dict) -> Dict:
        """
        Predict expected claim severity.

        Args:
            input_data: Input features dictionary

        Returns:
            Dictionary with prediction and confidence interval
        """
        if self.severity_model is None:
            # Return dummy prediction if model not loaded
            policy_size = input_data.get('policy_size', 'Medium')
            base_severity = {
                'Small': 50000,
                'Medium': 100000,
                'Large': 250000,
                'Enterprise': 500000
            }

            return {
                'predicted_severity': base_severity.get(policy_size, 100000),
                'confidence_interval': [
                    base_severity.get(policy_size, 100000) * 0.7,
                    base_severity.get(policy_size, 100000) * 1.3
                ],
                'model_loaded': False,
                'message': 'Model not loaded - using policy size-based estimate'
            }

        features_df = self.prepare_features(input_data)

        try:
            prediction = self.severity_model.predict(features_df)[0]

            # Calculate confidence interval
            confidence_interval = [
                max(0, prediction * 0.7),
                prediction * 1.3
            ]

            return {
                'predicted_severity': round(float(prediction), 2),
                'confidence_interval': [round(ci, 2) for ci in confidence_interval],
                'model_loaded': True,
                'input_features': input_data
            }

        except Exception as e:
            return {
                'error': str(e),
                'model_loaded': True,
                'message': 'Prediction failed'
            }

    def predict_both(self, input_data: Dict) -> Dict:
        """
        Predict both loss ratio and severity.

        Args:
            input_data: Input features dictionary

        Returns:
            Dictionary with both predictions
        """
        lr_prediction = self.predict_loss_ratio(input_data)
        severity_prediction = self.predict_severity(input_data)

        return {
            'loss_ratio': lr_prediction,
            'severity': severity_prediction,
            'input_features': input_data
        }

    def get_feature_importance(self, model_type: str = 'loss_ratio') -> Optional[Dict]:
        """
        Get feature importance from the specified model.

        Args:
            model_type: 'loss_ratio' or 'severity'

        Returns:
            Dictionary with feature importances
        """
        model = self.lr_model if model_type == 'loss_ratio' else self.severity_model

        if model is None:
            return None

        try:
            if hasattr(model, 'feature_importances_'):
                feature_names = ['RiskRating', 'Geography', 'Industry', 'PolicySize', 'ExposureUnits', 'AnnualPremium']
                importances = model.feature_importances_

                importance_dict = dict(zip(feature_names, importances.tolist()))

                # Sort by importance
                sorted_importance = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))

                return sorted_importance
            else:
                return None

        except Exception as e:
            print(f"Error getting feature importance: {e}")
            return None


# Global prediction service instance
_prediction_service = None


def get_prediction_service(models_dir: str = "models") -> PredictionService:
    """
    Get the global prediction service instance.

    Args:
        models_dir: Directory containing model files

    Returns:
        PredictionService instance
    """
    global _prediction_service

    if _prediction_service is None:
        _prediction_service = PredictionService(models_dir)

    return _prediction_service
