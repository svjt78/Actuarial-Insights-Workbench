"""
Model Training Script
Trains LightGBM models for Loss Ratio and Severity prediction.

Author: Actuarial Insights Workbench Team
"""

import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os


def prepare_training_data():
    """
    Load and prepare training data.

    Returns:
        Tuple of (features_df, loss_ratio_target, severity_target)
    """
    print("Loading data...")

    # Load datasets
    policies_df = pd.read_csv('../data/policies.csv')
    claims_df = pd.read_csv('../data/claims.csv')
    exposure_df = pd.read_csv('../data/exposure.csv')

    print(f"Loaded {len(policies_df)} policies, {len(claims_df)} claims, {len(exposure_df)} exposure records")

    # Aggregate exposure/premium by policy
    exposure_agg = exposure_df.groupby('PolicyID').agg({
        'EarnedPremium': 'sum',
        'ExposureUnits': 'mean'
    }).reset_index()

    # Aggregate claims by policy
    claims_agg = claims_df.groupby('PolicyID').agg({
        'IncurredAmount': 'sum',
        'ClaimID': 'count'
    }).reset_index()

    claims_agg.columns = ['PolicyID', 'TotalIncurred', 'ClaimCount']

    # Drop ExposureUnits from policies to avoid column name conflict during merge
    # We'll use the aggregated ExposureUnits from exposure data
    policies_for_merge = policies_df.drop(columns=['ExposureUnits'])

    # Merge policy data with exposure and claims
    training_df = policies_for_merge.merge(exposure_agg, on='PolicyID', how='left')
    training_df = training_df.merge(claims_agg, on='PolicyID', how='left')

    # Fill NaN for policies with no claims
    training_df['TotalIncurred'] = training_df['TotalIncurred'].fillna(0)
    training_df['ClaimCount'] = training_df['ClaimCount'].fillna(0)

    # Calculate loss ratio (target for first model)
    training_df['LossRatio'] = (training_df['TotalIncurred'] / training_df['EarnedPremium'] * 100).fillna(0)

    # Calculate average severity (target for second model)
    training_df['AvgSeverity'] = (training_df['TotalIncurred'] / training_df['ClaimCount']).fillna(0)

    print(f"Prepared {len(training_df)} training samples")

    return training_df


def encode_features(df):
    """
    Encode categorical features.

    Args:
        df: DataFrame with raw features

    Returns:
        DataFrame with encoded features
    """
    df = df.copy()

    # Geography encoding
    geography_map = {
        'Northeast': 0, 'Southeast': 1, 'Midwest': 2,
        'Southwest': 3, 'West': 4, 'Northwest': 5
    }
    df['Geography'] = df['Geography'].map(geography_map)

    # Industry encoding
    industry_map = {
        'Manufacturing': 0, 'Retail': 1, 'Office': 2, 'Warehouse': 3,
        'Healthcare': 4, 'Education': 5, 'Hospitality': 6, 'Technology': 7
    }
    df['Industry'] = df['Industry'].map(industry_map)

    # Policy size encoding
    policy_size_map = {'Small': 0, 'Medium': 1, 'Large': 2, 'Enterprise': 3}
    df['PolicySize'] = df['PolicySize'].map(policy_size_map)

    return df


def train_loss_ratio_model(training_df):
    """
    Train Loss Ratio prediction model.

    Args:
        training_df: Training data

    Returns:
        Trained model
    """
    print("\n" + "="*60)
    print("TRAINING LOSS RATIO MODEL")
    print("="*60)

    # Prepare features
    feature_cols = ['RiskRating', 'Geography', 'Industry', 'PolicySize', 'ExposureUnits', 'AnnualPremium']
    X = training_df[feature_cols].copy()
    y = training_df['LossRatio'].copy()

    # Encode categorical features
    X = encode_features(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Train model
    print("\nTraining LightGBM model...")
    model = LGBMRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        num_leaves=31,
        random_state=42,
        verbose=-1
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    print("\n" + "-"*60)
    print("MODEL PERFORMANCE")
    print("-"*60)
    print("\nTraining Set:")
    print(f"  MAE:  {mean_absolute_error(y_train, y_pred_train):.2f}")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y_train, y_pred_train)):.2f}")
    print(f"  R²:   {r2_score(y_train, y_pred_train):.4f}")

    print("\nTest Set:")
    print(f"  MAE:  {mean_absolute_error(y_test, y_pred_test):.2f}")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_test)):.2f}")
    print(f"  R²:   {r2_score(y_test, y_pred_test):.4f}")

    # Feature importance
    print("\nFeature Importance:")
    for feature, importance in zip(feature_cols, model.feature_importances_):
        print(f"  {feature:20s}: {importance:.4f}")

    return model


def train_severity_model(training_df):
    """
    Train Severity prediction model.

    Args:
        training_df: Training data

    Returns:
        Trained model
    """
    print("\n" + "="*60)
    print("TRAINING SEVERITY MODEL")
    print("="*60)

    # Filter to policies with claims
    df_with_claims = training_df[training_df['ClaimCount'] > 0].copy()
    print(f"Training on {len(df_with_claims)} policies with claims")

    # Prepare features
    feature_cols = ['RiskRating', 'Geography', 'Industry', 'PolicySize', 'ExposureUnits', 'AnnualPremium']
    X = df_with_claims[feature_cols].copy()
    y = df_with_claims['AvgSeverity'].copy()

    # Encode categorical features
    X = encode_features(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Train model
    print("\nTraining LightGBM model...")
    model = LGBMRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        num_leaves=31,
        random_state=42,
        verbose=-1
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    print("\n" + "-"*60)
    print("MODEL PERFORMANCE")
    print("-"*60)
    print("\nTraining Set:")
    print(f"  MAE:  ${mean_absolute_error(y_train, y_pred_train):,.2f}")
    print(f"  RMSE: ${np.sqrt(mean_squared_error(y_train, y_pred_train)):,.2f}")
    print(f"  R²:   {r2_score(y_train, y_pred_train):.4f}")

    print("\nTest Set:")
    print(f"  MAE:  ${mean_absolute_error(y_test, y_pred_test):,.2f}")
    print(f"  RMSE: ${np.sqrt(mean_squared_error(y_test, y_pred_test)):,.2f}")
    print(f"  R²:   {r2_score(y_test, y_pred_test):.4f}")

    # Feature importance
    print("\nFeature Importance:")
    for feature, importance in zip(feature_cols, model.feature_importances_):
        print(f"  {feature:20s}: {importance:.4f}")

    return model


def main():
    """Main execution function."""
    print("="*60)
    print("ACTUARIAL INSIGHTS WORKBENCH - MODEL TRAINING")
    print("="*60)
    print()

    # Load and prepare data
    training_df = prepare_training_data()

    # Train Loss Ratio model
    lr_model = train_loss_ratio_model(training_df)

    # Save model (use /app/models when running in Docker, ../backend/models for local)
    models_dir = '/app/models' if os.path.exists('/app/models') else '../backend/models'
    os.makedirs(models_dir, exist_ok=True)

    lr_model_path = os.path.join(models_dir, 'lr_model.pkl')
    joblib.dump(lr_model, lr_model_path)
    print(f"\n✅ Loss Ratio model saved to {lr_model_path}")

    # Train Severity model
    severity_model = train_severity_model(training_df)

    # Save model
    severity_model_path = os.path.join(models_dir, 'severity_model.pkl')
    joblib.dump(severity_model, severity_model_path)
    print(f"\n✅ Severity model saved to {severity_model_path}")

    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE!")
    print("="*60)
    print(f"\nModels saved in: ../backend/models/")
    print("  - lr_model.pkl (Loss Ratio)")
    print("  - severity_model.pkl (Severity)")


if __name__ == "__main__":
    main()
