"""
Risk Prediction Page
ML-powered predictions for loss ratio and claim severity.

Author: Actuarial Insights Workbench Team
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import os

st.set_page_config(page_title="Risk Prediction", page_icon="🎯", layout="wide")

# Get backend URL
BACKEND_URL = os.getenv('BACKEND_HOST', 'localhost')
BACKEND_PORT = os.getenv('BACKEND_PORT', '8003')
API_BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"

st.title("🎯 Risk Prediction & Scoring")
st.markdown("ML-powered predictions for expected loss ratio and claim severity")

st.markdown("---")

# Input form
st.subheader("📝 Policy Characteristics")

col1, col2, col3 = st.columns(3)

with col1:
    geography = st.selectbox(
        "Geography",
        options=["Northeast", "Southeast", "Midwest", "Southwest", "West", "Northwest"],
        help="Geographic region of the property"
    )

    industry = st.selectbox(
        "Industry",
        options=["Manufacturing", "Retail", "Office", "Warehouse", "Healthcare", "Education", "Hospitality", "Technology"],
        help="Industry sector"
    )

with col2:
    policy_size = st.selectbox(
        "Policy Size",
        options=["Small", "Medium", "Large", "Enterprise"],
        help="Policy size category"
    )

    risk_rating = st.slider(
        "Risk Rating (COPE)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="Composite COPE-based risk score (1=low risk, 10=high risk)"
    )

with col3:
    exposure_units = st.number_input(
        "Exposure Units",
        min_value=1.0,
        max_value=10000.0,
        value=50.0,
        step=10.0,
        help="Building value in $100K units"
    )

    annual_premium = st.number_input(
        "Annual Premium ($)",
        min_value=1000.0,
        max_value=10000000.0,
        value=25000.0,
        step=1000.0,
        help="Annual premium amount"
    )

st.markdown("---")

# Prediction buttons
col1, col2, col3 = st.columns(3)

with col1:
    predict_lr = st.button("🎲 Predict Loss Ratio", type="primary", use_container_width=True)

with col2:
    predict_sev = st.button("💰 Predict Severity", use_container_width=True)

with col3:
    predict_both = st.button("🔮 Predict Both", type="secondary", use_container_width=True)

# Prepare request data
request_data = {
    "geography": geography,
    "industry": industry,
    "policy_size": policy_size,
    "risk_rating": risk_rating,
    "exposure_units": exposure_units,
    "annual_premium": annual_premium
}

# Handle predictions
if predict_lr or predict_both:
    with st.spinner("Generating loss ratio prediction..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict/loss_ratio",
                json=request_data,
                timeout=10
            )

            if response.status_code == 200:
                st.session_state['lr_prediction'] = response.json()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend API. Make sure the backend service is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if predict_sev or predict_both:
    with st.spinner("Generating severity prediction..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict/severity",
                json=request_data,
                timeout=10
            )

            if response.status_code == 200:
                st.session_state['sev_prediction'] = response.json()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend API. Make sure the backend service is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display Loss Ratio Prediction
if 'lr_prediction' in st.session_state and st.session_state['lr_prediction']:
    st.markdown("---")
    st.subheader("📊 Loss Ratio Prediction")

    lr_data = st.session_state['lr_prediction']

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        predicted_lr = lr_data.get('predicted_loss_ratio', 0)
        ci = lr_data.get('confidence_interval', [0, 0])

        # Gauge chart for loss ratio
        fig_lr = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=predicted_lr,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Predicted Loss Ratio (%)", 'font': {'size': 20}},
            delta={'reference': 65, 'suffix': "% vs target"},
            gauge={
                'axis': {'range': [None, 150]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 70], 'color': "yellow"},
                    {'range': [70, 150], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 65
                }
            }
        ))

        fig_lr.update_layout(height=300)
        st.plotly_chart(fig_lr, use_container_width=True)

    with col2:
        st.metric("Predicted LR", f"{predicted_lr:.2f}%")
        st.caption("Expected loss ratio")

    with col3:
        st.metric("Confidence Interval", f"{ci[0]:.1f}% - {ci[1]:.1f}%")
        st.caption("95% confidence range")

    # Interpretation
    if predicted_lr < 55:
        st.success("✅ **Favorable Risk** - Loss ratio well below target")
    elif predicted_lr < 70:
        st.info("ℹ️ **Acceptable Risk** - Loss ratio near target range")
    else:
        st.warning("⚠️ **Elevated Risk** - Loss ratio above target, consider higher premium or declining")

    if not lr_data.get('model_loaded', True):
        st.info(f"ℹ️ {lr_data.get('message', 'Model prediction')}")

# Display Severity Prediction
if 'sev_prediction' in st.session_state and st.session_state['sev_prediction']:
    st.markdown("---")
    st.subheader("💰 Severity Prediction")

    sev_data = st.session_state['sev_prediction']

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        predicted_sev = sev_data.get('predicted_severity', 0)
        ci_sev = sev_data.get('confidence_interval', [0, 0])

        # Bar chart for severity
        fig_sev = go.Figure()

        fig_sev.add_trace(go.Bar(
            x=['Low Estimate', 'Predicted', 'High Estimate'],
            y=[ci_sev[0], predicted_sev, ci_sev[1]],
            marker_color=['lightblue', 'darkblue', 'lightcoral'],
            text=[f"${ci_sev[0]:,.0f}", f"${predicted_sev:,.0f}", f"${ci_sev[1]:,.0f}"],
            textposition='outside'
        ))

        fig_sev.update_layout(
            title="Expected Claim Severity",
            yaxis_title="Amount ($)",
            showlegend=False,
            height=300
        )

        st.plotly_chart(fig_sev, use_container_width=True)

    with col2:
        st.metric("Predicted Severity", f"${predicted_sev:,.0f}")
        st.caption("Expected claim amount")

    with col3:
        range_pct = ((ci_sev[1] - ci_sev[0]) / predicted_sev * 100) if predicted_sev > 0 else 0
        st.metric("Uncertainty", f"±{range_pct/2:.1f}%")
        st.caption("Prediction range")

    if not sev_data.get('model_loaded', True):
        st.info(f"ℹ️ {sev_data.get('message', 'Model prediction')}")

# Risk Summary
if 'lr_prediction' in st.session_state and 'sev_prediction' in st.session_state:
    st.markdown("---")
    st.subheader("📋 Risk Summary")

    lr_pred = st.session_state['lr_prediction'].get('predicted_loss_ratio', 0)
    sev_pred = st.session_state['sev_prediction'].get('predicted_severity', 0)

    # Calculate expected loss
    expected_loss = annual_premium * (lr_pred / 100)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Expected Loss", f"${expected_loss:,.0f}")

    with col2:
        profit = annual_premium - expected_loss
        st.metric("Expected Profit", f"${profit:,.0f}")

    with col3:
        margin = (profit / annual_premium * 100) if annual_premium > 0 else 0
        st.metric("Profit Margin", f"{margin:.1f}%")

    with col4:
        risk_score = min(10, risk_rating * (lr_pred / 65))
        st.metric("Composite Risk Score", f"{risk_score:.1f}/10")

# Input Summary
with st.expander("📋 View Input Summary"):
    st.json(request_data)

# Feature Importance
with st.expander("🔍 Model Feature Importance"):
    st.markdown("""
    ### Key Factors Influencing Predictions:

    1. **Risk Rating (COPE)** - Primary driver of loss expectations
    2. **Geography** - Regional loss patterns and catastrophe exposure
    3. **Industry** - Business-specific hazards and loss patterns
    4. **Policy Size** - Exposure amount and limit selections
    5. **Exposure Units** - Building value and replacement cost
    6. **Annual Premium** - Pricing adequacy indicator

    The models use LightGBM gradient boosting trained on historical portfolio data
    to predict expected outcomes based on these characteristics.
    """)

# About the models
with st.expander("ℹ️ About the Prediction Models"):
    st.markdown("""
    ### Model Information

    **Loss Ratio Model:**
    - Predicts expected loss ratio (%) for a policy
    - Trained on historical policy and claims data
    - Uses LightGBM regression algorithm
    - Confidence intervals represent uncertainty in prediction

    **Severity Model:**
    - Predicts expected claim amount if a loss occurs
    - Considers risk characteristics and policy limits
    - Useful for reserve setting and pricing

    **Usage Notes:**
    - Predictions are estimates based on historical patterns
    - Actual results may vary due to random variation
    - Use in combination with underwriting judgment
    - Confidence intervals indicate prediction uncertainty
    """)
