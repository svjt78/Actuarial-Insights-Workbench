"""
GenAI Explanation Service
Provides natural language explanations for actuarial insights using OpenAI GPT-3.5.

Author: Actuarial Insights Workbench Team
"""

import os
from typing import Dict, Optional
from openai import OpenAI
import json


class ActuarialExplainer:
    """
    Generates natural language explanations for actuarial data and trends
    using OpenAI's GPT-3.5-turbo model.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the explainer with OpenAI API key.

        Args:
            api_key: OpenAI API key (if not provided, reads from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and not found in environment")

        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"

    def explain_loss_ratio(
        self,
        segment: str,
        loss_ratio: float,
        benchmark: float,
        context: Optional[Dict] = None
    ) -> str:
        """
        Explain a loss ratio for a specific segment.

        Args:
            segment: Segment name (e.g., "Northeast" or "Manufacturing")
            loss_ratio: Actual loss ratio percentage
            benchmark: Benchmark or expected loss ratio
            context: Additional context data

        Returns:
            Natural language explanation
        """
        context_str = ""
        if context:
            context_str = f"\n\nAdditional context: {json.dumps(context, indent=2)}"

        prompt = f"""You are an expert actuarial analyst explaining insurance metrics to underwriters.

Explain the following Commercial Property insurance loss ratio:

Segment: {segment}
Actual Loss Ratio: {loss_ratio:.2f}%
Benchmark/Expected: {benchmark:.2f}%
Variance: {loss_ratio - benchmark:.2f} percentage points
{context_str}

Provide a concise 2-3 sentence explanation that:
1. Interprets whether this is favorable or unfavorable
2. Suggests potential drivers or factors
3. Recommends next steps if needed

Keep the tone professional but accessible."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert actuarial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    def explain_trend(
        self,
        metric_name: str,
        trend_data: Dict,
        trend_direction: str = "neutral"
    ) -> str:
        """
        Explain a trend in an actuarial metric.

        Args:
            metric_name: Name of the metric (e.g., "Loss Ratio", "Claim Frequency")
            trend_data: Dictionary with trend data points
            trend_direction: "increasing", "decreasing", or "neutral"

        Returns:
            Natural language explanation
        """
        prompt = f"""You are an expert actuarial analyst explaining insurance trends.

Analyze the following trend in Commercial Property insurance:

Metric: {metric_name}
Trend Direction: {trend_direction}
Data: {json.dumps(trend_data, indent=2)}

Provide a concise 2-3 sentence explanation that:
1. Describes the trend pattern
2. Assesses the implications for the portfolio
3. Suggests potential actions or areas for investigation

Keep the tone professional but accessible."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert actuarial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    def explain_prediction(
        self,
        prediction_type: str,
        predicted_value: float,
        input_features: Dict,
        model_confidence: Optional[float] = None
    ) -> str:
        """
        Explain a model prediction.

        Args:
            prediction_type: Type of prediction ("Loss Ratio" or "Severity")
            predicted_value: Predicted value
            input_features: Input features used for prediction
            model_confidence: Optional confidence score

        Returns:
            Natural language explanation
        """
        confidence_str = ""
        if model_confidence is not None:
            confidence_str = f"\nModel Confidence: {model_confidence:.1f}%"

        prompt = f"""You are an expert actuarial analyst explaining ML model predictions.

Explain the following prediction for Commercial Property insurance:

Prediction Type: {prediction_type}
Predicted Value: {predicted_value:.2f}{'%' if prediction_type == 'Loss Ratio' else ''}
{confidence_str}

Input Features:
{json.dumps(input_features, indent=2)}

Provide a concise 2-3 sentence explanation that:
1. Interprets the prediction
2. Highlights key factors driving the prediction
3. Notes any important considerations or caveats

Keep the tone professional but accessible."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert actuarial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    def answer_question(
        self,
        question: str,
        context_data: Optional[Dict] = None
    ) -> str:
        """
        Answer a general question about actuarial data.

        Args:
            question: User's question
            context_data: Optional context data to inform the answer

        Returns:
            Natural language answer
        """
        context_str = ""
        if context_data:
            context_str = f"\n\nContext data:\n{json.dumps(context_data, indent=2)}"

        prompt = f"""You are an expert actuarial analyst for Commercial Property insurance.

Answer the following question based on the provided context:

Question: {question}
{context_str}

Provide a clear, concise answer (2-4 sentences) that:
1. Directly addresses the question
2. References specific data points when available
3. Provides actionable insights when relevant

Keep the tone professional but accessible."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert actuarial analyst specializing in Commercial Property insurance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )

        return response.choices[0].message.content.strip()

    def explain_cope_rating(
        self,
        risk_rating: float,
        geography: str,
        industry: str
    ) -> str:
        """
        Explain a COPE-based risk rating.

        Args:
            risk_rating: Composite risk rating (1-10 scale)
            geography: Geographic region
            industry: Industry sector

        Returns:
            Natural language explanation
        """
        prompt = f"""You are an expert commercial property underwriter explaining risk ratings.

Explain the following COPE-based risk rating:

Risk Rating: {risk_rating:.2f} / 10
Geography: {geography}
Industry: {industry}

COPE Framework (Construction, Occupancy, Protection, Exposure) is used to assess property risk.

Provide a concise 2-3 sentence explanation that:
1. Interprets the risk level (low, moderate, high)
2. Notes how geography and industry may influence the rating
3. Suggests what underwriting factors to consider

Keep the tone professional but accessible."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert commercial property underwriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()


def get_explanation(
    explanation_type: str,
    data: Dict,
    api_key: Optional[str] = None
) -> str:
    """
    Convenience function to get an explanation.

    Args:
        explanation_type: Type of explanation needed
        data: Data to explain
        api_key: Optional OpenAI API key

    Returns:
        Natural language explanation
    """
    try:
        explainer = ActuarialExplainer(api_key)

        if explanation_type == "loss_ratio":
            return explainer.explain_loss_ratio(
                data.get("segment"),
                data.get("loss_ratio"),
                data.get("benchmark"),
                data.get("context")
            )
        elif explanation_type == "trend":
            return explainer.explain_trend(
                data.get("metric_name"),
                data.get("trend_data"),
                data.get("trend_direction")
            )
        elif explanation_type == "prediction":
            return explainer.explain_prediction(
                data.get("prediction_type"),
                data.get("predicted_value"),
                data.get("input_features"),
                data.get("model_confidence")
            )
        elif explanation_type == "question":
            return explainer.answer_question(
                data.get("question"),
                data.get("context_data")
            )
        elif explanation_type == "cope_rating":
            return explainer.explain_cope_rating(
                data.get("risk_rating"),
                data.get("geography"),
                data.get("industry")
            )
        else:
            return f"Unknown explanation type: {explanation_type}"

    except Exception as e:
        return f"Error generating explanation: {str(e)}"
