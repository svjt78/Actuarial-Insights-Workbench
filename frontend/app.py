"""
Actuarial Insights Workbench - Streamlit Frontend
Main application landing page.

Author: Actuarial Insights Workbench Team
"""

import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Actuarial Insights Workbench",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional theme
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Main page content
st.markdown('<div class="main-header">📊 Actuarial Insights Workbench</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Modern actuarial analytics powered by ML and GenAI</div>', unsafe_allow_html=True)

st.markdown("---")

# Welcome message
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Welcome to the Actuarial Insights Workbench

    This platform provides comprehensive actuarial analytics for Commercial Property insurance, combining:

    - **Loss Development Analysis** - Track loss emergence patterns with development triangles
    - **Predictive Modeling** - ML-powered loss ratio and severity predictions
    - **Segment Analytics** - Deep-dive KPIs by geography, industry, and risk characteristics
    - **GenAI Insights** - Natural language explanations of trends and predictions
    """)

    st.info("👈 **Navigate using the sidebar** to explore different analytics modules")

with col2:
    st.markdown("### Quick Stats")

    # These would normally come from the API
    st.metric("Portfolio Size", "1,000", help="Active policies")
    st.metric("Total Premium", "$122.9M", help="Earned premium")
    st.metric("Overall Loss Ratio", "12.0%", help="Incurred loss ratio")

st.markdown("---")

# Feature cards
st.markdown("### 🎯 Key Features")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("#### 📈 Loss Development Dashboard")
        st.markdown("Visualize loss emergence with cumulative and incremental triangles. Calculate age-to-age development factors and project ultimate losses using proven actuarial methods.")
        st.markdown("")  # Spacing

    with st.container():
        st.markdown("#### 🎯 Risk Prediction")
        st.markdown("Input policy characteristics and get instant ML predictions for expected loss ratio and claim severity, with confidence intervals and feature importance analysis.")
        st.markdown("")  # Spacing

with col2:
    with st.container():
        st.markdown("#### 📊 Pricing & KPIs")
        st.markdown("Analyze portfolio performance by segment with key metrics including loss ratio, frequency, severity, and pure premium across multiple dimensions.")
        st.markdown("")  # Spacing

    with st.container():
        st.markdown("#### 🤖 GenAI Insights")
        st.markdown("Ask questions about your portfolio in natural language and receive expert-level actuarial explanations powered by GPT-3.5-turbo.")
        st.markdown("")  # Spacing

st.markdown("---")

# Tech stack info
with st.expander("🛠 Technology Stack"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Frontend**
        - Streamlit
        - Plotly/Matplotlib
        - Python 3.11
        """)

    with col2:
        st.markdown("""
        **Backend**
        - FastAPI
        - LightGBM
        - Pandas/NumPy
        """)

    with col3:
        st.markdown("""
        **AI/ML**
        - OpenAI GPT-3.5
        - Scikit-learn
        - Feature Engineering
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Actuarial Insights Workbench | Built with modern actuarial science and AI</p>
    <p>For demonstration and educational purposes</p>
</div>
""", unsafe_allow_html=True)
