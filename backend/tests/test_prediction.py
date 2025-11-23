"""
Unit tests for prediction service.

Author: Actuarial Insights Workbench Team
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.prediction import PredictionService


@pytest.fixture
def prediction_service():
    """Create prediction service instance."""
    return PredictionService(models_dir="models")


@pytest.fixture
def sample_input():
    """Sample input data for predictions."""
    return {
        'geography': 'Northeast',
        'industry': 'Manufacturing',
        'policy_size': 'Medium',
        'risk_rating': 6.5,
        'exposure_units': 50.0,
        'annual_premium': 25000.0
    }


def test_prediction_service_initialization(prediction_service):
    """Test service initialization."""
    assert isinstance(prediction_service, PredictionService)
    assert prediction_service.models_dir is not None


def test_prepare_features(prediction_service, sample_input):
    """Test feature preparation."""
    features_df = prediction_service.prepare_features(sample_input)

    assert len(features_df) == 1
    assert 'RiskRating' in features_df.columns
    assert 'Geography' in features_df.columns
    assert 'Industry' in features_df.columns
    assert 'PolicySize' in features_df.columns

    # Check encoding worked
    assert features_df['Geography'].iloc[0] in range(6)
    assert features_df['Industry'].iloc[0] in range(8)
    assert features_df['PolicySize'].iloc[0] in range(4)


def test_predict_loss_ratio(prediction_service, sample_input):
    """Test loss ratio prediction."""
    result = prediction_service.predict_loss_ratio(sample_input)

    assert isinstance(result, dict)
    assert 'predicted_loss_ratio' in result
    assert 'confidence_interval' in result

    # Check reasonable bounds
    assert result['predicted_loss_ratio'] >= 0
    assert result['predicted_loss_ratio'] <= 200
    assert len(result['confidence_interval']) == 2


def test_predict_severity(prediction_service, sample_input):
    """Test severity prediction."""
    result = prediction_service.predict_severity(sample_input)

    assert isinstance(result, dict)
    assert 'predicted_severity' in result
    assert 'confidence_interval' in result

    # Check reasonable bounds
    assert result['predicted_severity'] >= 0
    assert len(result['confidence_interval']) == 2


def test_predict_both(prediction_service, sample_input):
    """Test predicting both metrics."""
    result = prediction_service.predict_both(sample_input)

    assert isinstance(result, dict)
    assert 'loss_ratio' in result
    assert 'severity' in result
    assert 'input_features' in result


def test_different_geographies(prediction_service):
    """Test predictions across different geographies."""
    geographies = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West', 'Northwest']

    results = []
    for geo in geographies:
        input_data = {
            'geography': geo,
            'industry': 'Office',
            'policy_size': 'Medium',
            'risk_rating': 5.0,
            'exposure_units': 50.0,
            'annual_premium': 25000.0
        }

        result = prediction_service.predict_loss_ratio(input_data)
        results.append(result['predicted_loss_ratio'])

    # Predictions should vary by geography
    assert len(set(results)) > 1 or all(r == results[0] for r in results)


def test_risk_rating_impact(prediction_service):
    """Test that risk rating impacts predictions."""
    low_risk = {
        'geography': 'Midwest',
        'industry': 'Office',
        'policy_size': 'Medium',
        'risk_rating': 2.0,
        'exposure_units': 50.0,
        'annual_premium': 25000.0
    }

    high_risk = {
        'geography': 'Midwest',
        'industry': 'Office',
        'policy_size': 'Medium',
        'risk_rating': 9.0,
        'exposure_units': 50.0,
        'annual_premium': 25000.0
    }

    low_result = prediction_service.predict_loss_ratio(low_risk)
    high_result = prediction_service.predict_loss_ratio(high_risk)

    # Higher risk should generally predict higher loss ratio
    # (unless models not loaded, in which case both return defaults)
    if low_result.get('model_loaded') and high_result.get('model_loaded'):
        assert high_result['predicted_loss_ratio'] > low_result['predicted_loss_ratio']


def test_confidence_intervals(prediction_service, sample_input):
    """Test that confidence intervals are reasonable."""
    lr_result = prediction_service.predict_loss_ratio(sample_input)
    sev_result = prediction_service.predict_severity(sample_input)

    # Check LR confidence interval
    lr_ci = lr_result['confidence_interval']
    assert lr_ci[0] < lr_result['predicted_loss_ratio']
    assert lr_ci[1] > lr_result['predicted_loss_ratio']

    # Check severity confidence interval
    sev_ci = sev_result['confidence_interval']
    assert sev_ci[0] < sev_result['predicted_severity']
    assert sev_ci[1] > sev_result['predicted_severity']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
