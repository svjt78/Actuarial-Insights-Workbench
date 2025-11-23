"""
Actuarial Insights Workbench - FastAPI Backend
Main application file with API endpoints.

Author: Actuarial Insights Workbench Team
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import pandas as pd
import os
from dotenv import load_dotenv

# Import service modules
from services.loss_triangle import calculate_loss_triangle, LossTriangleCalculator
from services.segment_kpis import calculate_segment_kpis, SegmentKPICalculator
from services.prediction import get_prediction_service
from services.explain import get_explanation, ActuarialExplainer

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Actuarial Insights Workbench API",
    description="API for actuarial analytics, ML predictions, and GenAI explanations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data on startup
policies_df = None
claims_df = None
exposure_df = None
prediction_service = None


@app.on_event("startup")
async def startup_event():
    """Load data and initialize services on startup."""
    global policies_df, claims_df, exposure_df, prediction_service

    try:
        # Load data (path is /app/data due to volume mount)
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        policies_df = pd.read_csv(os.path.join(data_dir, "policies.csv"))
        claims_df = pd.read_csv(os.path.join(data_dir, "claims.csv"))
        exposure_df = pd.read_csv(os.path.join(data_dir, "exposure.csv"))

        print("✅ Data loaded successfully")
        print(f"   - Policies: {len(policies_df)}")
        print(f"   - Claims: {len(claims_df)}")
        print(f"   - Exposure records: {len(exposure_df)}")

        # Initialize prediction service
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        prediction_service = get_prediction_service(models_dir)
        print("✅ Prediction service initialized")

    except Exception as e:
        print(f"⚠️  Error loading data: {e}")


# Pydantic models for request/response
class PredictionRequest(BaseModel):
    """Request model for predictions."""
    geography: str = Field(..., example="Northeast")
    industry: str = Field(..., example="Manufacturing")
    policy_size: str = Field(..., example="Medium")
    risk_rating: float = Field(..., ge=1.0, le=10.0, example=6.5)
    exposure_units: float = Field(..., gt=0, example=50.0)
    annual_premium: float = Field(..., gt=0, example=25000.0)


class ExplanationRequest(BaseModel):
    """Request model for GenAI explanations."""
    explanation_type: str = Field(..., example="question")
    data: Dict = Field(..., example={"question": "What is driving the loss ratio?"})


class SegmentInsightsQuery(BaseModel):
    """Query parameters for segment insights."""
    segment_by: str = Field(default="Geography", example="Geography")
    min_premium: float = Field(default=0, example=0)


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Actuarial Insights Workbench API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "predictions": "/predict/loss_ratio, /predict/severity, /predict/both",
            "analytics": "/segment_insights, /loss_triangle",
            "genai": "/explain"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "data_loaded": policies_df is not None,
        "model_loaded": prediction_service is not None
    }


@app.post("/predict/loss_ratio")
async def predict_loss_ratio(request: PredictionRequest):
    """
    Predict expected loss ratio for a policy.

    Args:
        request: Policy characteristics

    Returns:
        Predicted loss ratio with confidence interval
    """
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not available")

    try:
        input_data = request.dict()
        result = prediction_service.predict_loss_ratio(input_data)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/severity")
async def predict_severity(request: PredictionRequest):
    """
    Predict expected claim severity for a policy.

    Args:
        request: Policy characteristics

    Returns:
        Predicted severity with confidence interval
    """
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not available")

    try:
        input_data = request.dict()
        result = prediction_service.predict_severity(input_data)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/both")
async def predict_both(request: PredictionRequest):
    """
    Predict both loss ratio and severity for a policy.

    Args:
        request: Policy characteristics

    Returns:
        Both predictions with confidence intervals
    """
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not available")

    try:
        input_data = request.dict()
        result = prediction_service.predict_both(input_data)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/segment_insights")
async def get_segment_insights(
    segment_by: str = "Geography",
    min_premium: float = 0
):
    """
    Get KPIs by segment.

    Args:
        segment_by: Dimension to segment by (Geography, Industry, PolicySize, RiskRating)
        min_premium: Minimum earned premium filter

    Returns:
        Segment-level KPIs and overall portfolio metrics
    """
    if policies_df is None or claims_df is None or exposure_df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")

    try:
        calculator = SegmentKPICalculator(policies_df, claims_df, exposure_df)

        result = {
            "segment_kpis": calculator.calculate_kpis_by_segment(
                segment_by,
                min_premium
            ).to_dict('records'),
            "overall_kpis": calculator.calculate_overall_kpis(),
            "segment_by": segment_by
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/loss_triangle")
async def get_loss_triangle(
    value_col: str = "IncurredAmount",
    triangle_type: str = "cumulative",
    max_dev_months: int = 36
):
    """
    Get loss development triangle.

    Args:
        value_col: Value to aggregate (IncurredAmount or PaidAmount)
        triangle_type: cumulative or incremental
        max_dev_months: Maximum development months

    Returns:
        Loss triangle with development factors and ultimate projections
    """
    if claims_df is None:
        raise HTTPException(status_code=503, detail="Claims data not loaded")

    try:
        result = calculate_loss_triangle(
            claims_df,
            triangle_type,
            value_col,
            max_dev_months
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
async def get_explanation_endpoint(request: ExplanationRequest):
    """
    Get GenAI explanation for actuarial insights.

    Args:
        request: Explanation type and data

    Returns:
        Natural language explanation
    """
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured"
        )

    try:
        explanation = get_explanation(
            request.explanation_type,
            request.data,
            api_key
        )

        return {
            "explanation": explanation,
            "explanation_type": request.explanation_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/feature_importance/{model_type}")
async def get_feature_importance(model_type: str):
    """
    Get feature importance from a trained model.

    Args:
        model_type: 'loss_ratio' or 'severity'

    Returns:
        Feature importance scores
    """
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not available")

    if model_type not in ['loss_ratio', 'severity']:
        raise HTTPException(status_code=400, detail="Invalid model_type")

    try:
        importance = prediction_service.get_feature_importance(model_type)

        if importance is None:
            return {
                "message": "Feature importance not available",
                "model_loaded": False
            }

        return {
            "feature_importance": importance,
            "model_type": model_type,
            "model_loaded": True
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data_summary")
async def get_data_summary():
    """
    Get summary statistics of loaded data.

    Returns:
        Summary of policies, claims, and exposure data
    """
    if policies_df is None or claims_df is None or exposure_df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")

    try:
        return {
            "policies": {
                "count": len(policies_df),
                "date_range": {
                    "start": policies_df['EffectiveDate'].min(),
                    "end": policies_df['EffectiveDate'].max()
                },
                "total_premium": float(policies_df['AnnualPremium'].sum()),
                "avg_premium": float(policies_df['AnnualPremium'].mean())
            },
            "claims": {
                "count": len(claims_df),
                "total_incurred": float(claims_df['IncurredAmount'].sum()),
                "total_paid": float(claims_df['PaidAmount'].sum()),
                "avg_severity": float(claims_df['IncurredAmount'].mean())
            },
            "exposure": {
                "records": len(exposure_df),
                "total_earned_premium": float(exposure_df['EarnedPremium'].sum())
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
