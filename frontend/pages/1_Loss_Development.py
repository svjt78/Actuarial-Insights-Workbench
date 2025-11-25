"""
Loss Development Dashboard Page
Displays loss triangles and development patterns.

Author: Actuarial Insights Workbench Team
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import os

st.set_page_config(page_title="Loss Development", page_icon="📈", layout="wide")

# Get backend URL
BACKEND_URL = os.getenv('BACKEND_HOST', 'localhost')
BACKEND_PORT = os.getenv('BACKEND_PORT', '8000')
API_BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"

st.title("📈 Loss Development Dashboard")
st.markdown("Analyze loss emergence patterns and development factors")

st.markdown("---")

# Controls
col1, col2, col3 = st.columns(3)

with col1:
    value_col = st.selectbox(
        "Loss Type",
        options=["IncurredAmount", "PaidAmount"],
        format_func=lambda x: "Incurred Losses" if x == "IncurredAmount" else "Paid Losses"
    )

with col2:
    triangle_type = st.selectbox(
        "Triangle Type",
        options=["cumulative", "incremental"],
        format_func=lambda x: x.capitalize()
    )

with col3:
    max_dev_months = st.slider(
        "Development Months",
        min_value=12,
        max_value=36,
        value=36,
        step=6
    )

# Fetch data button
if st.button("🔄 Load Triangle Data", type="primary"):
    with st.spinner("Fetching loss triangle data..."):
        try:
            response = requests.get(
                f"{API_BASE_URL}/loss_triangle",
                params={
                    "value_col": value_col,
                    "triangle_type": triangle_type,
                    "max_dev_months": max_dev_months
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state['triangle_data'] = data
                st.success("✅ Data loaded successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                st.session_state['triangle_data'] = None

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend API. Make sure the backend service is running.")
            st.session_state['triangle_data'] = None
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            st.session_state['triangle_data'] = None

# Display data if available
if 'triangle_data' in st.session_state and st.session_state['triangle_data']:
    data = st.session_state['triangle_data']

    st.markdown("---")

    # Summary statistics
    st.subheader("📊 Summary Statistics")

    summary = data.get('summary_stats', {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Reported",
            f"${summary.get('total_reported', 0):,.0f}",
            help="Total reported losses to date"
        )

    with col2:
        st.metric(
            "Projected Ultimate",
            f"${summary.get('total_ultimate', 0):,.0f}",
            help="Projected ultimate losses"
        )

    with col3:
        ibnr = summary.get('total_ibnr', 0)
        st.metric(
            "Total IBNR",
            f"${ibnr:,.0f}",
            help="Incurred But Not Reported reserves"
        )

    with col4:
        avg_dev = summary.get('avg_dev_factor', 1.0)
        st.metric(
            "Avg Dev Factor",
            f"{avg_dev:.3f}",
            help="Average development factor"
        )

    st.markdown("---")

    # Loss Triangle Heatmap
    st.subheader(f"🔥 {triangle_type.capitalize()} Loss Triangle")

    triangle_dict = data.get('cumulative_triangle' if triangle_type == 'cumulative' else 'incremental_triangle', {})

    if triangle_dict:
        # Convert to DataFrame
        triangle_df = pd.DataFrame(triangle_dict)

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=triangle_df.values,
            x=triangle_df.columns,
            y=triangle_df.index,
            colorscale='Blues',
            text=triangle_df.values,
            texttemplate='%{text:,.0f}',
            textfont={"size": 10},
            colorbar=dict(title="Loss Amount")
        ))

        fig.update_layout(
            title=f"{triangle_type.capitalize()} Loss Triangle by Accident Year",
            xaxis_title="Development Month",
            yaxis_title="Accident Year",
            yaxis=dict(type='category'),
            height=400,
            font=dict(size=12)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Development Factors
    st.subheader("📐 Age-to-Age Development Factors")

    dev_factors = data.get('development_factors', {})

    if dev_factors:
        # Convert to DataFrame for display
        df_factors = pd.DataFrame([
            {
                'Period': k,
                'Factor': f"{v:.4f}",
                'Implied % Development': f"{(v - 1) * 100:.2f}%"
            }
            for k, v in dev_factors.items()
        ])

        st.dataframe(df_factors, use_container_width=True)

        # Visualize development pattern
        factors_chart = pd.DataFrame([
            {'Development Period': k, 'Factor': v}
            for k, v in dev_factors.items()
        ])

        fig_factors = px.line(
            factors_chart,
            x='Development Period',
            y='Factor',
            title='Development Factor Pattern',
            markers=True
        )

        fig_factors.update_layout(
            yaxis_title="Development Factor",
            xaxis_title="Development Period (Months)",
            xaxis=dict(type='category'),
            height=300
        )

        st.plotly_chart(fig_factors, use_container_width=True)

    st.markdown("---")

    # Ultimate Projections
    st.subheader("🎯 Ultimate Loss Projections")

    ultimate_data = data.get('ultimate_projections', [])

    if ultimate_data:
        df_ultimate = pd.DataFrame(ultimate_data)

        # Convert AccidentYear to string to prevent comma formatting
        df_ultimate['AccidentYear'] = df_ultimate['AccidentYear'].astype(str)

        # Format columns
        df_ultimate['ReportedLoss'] = df_ultimate['ReportedLoss'].apply(lambda x: f"${x:,.0f}")
        df_ultimate['UltimateLoss'] = df_ultimate['UltimateLoss'].apply(lambda x: f"${x:,.0f}")
        df_ultimate['IBNR'] = df_ultimate['IBNR'].apply(lambda x: f"${x:,.0f}")
        df_ultimate['PercentDeveloped'] = df_ultimate['PercentDeveloped'].apply(lambda x: f"{x:.1f}%")

        st.dataframe(df_ultimate, use_container_width=True, hide_index=True)

        # Visualize maturity
        df_vis = pd.DataFrame(ultimate_data)

        # Convert AccidentYear to string for proper categorical display
        df_vis['AccidentYear'] = df_vis['AccidentYear'].astype(str)

        fig_maturity = px.bar(
            df_vis,
            x='AccidentYear',
            y='PercentDeveloped',
            title='Loss Development Maturity by Accident Year',
            labels={'PercentDeveloped': '% Developed', 'AccidentYear': 'Accident Year'},
            color='PercentDeveloped',
            color_continuous_scale='RdYlGn'
        )

        fig_maturity.update_layout(
            height=300,
            xaxis={'type': 'category'}  # Force categorical axis
        )

        st.plotly_chart(fig_maturity, use_container_width=True)

else:
    st.info("👆 Click 'Load Triangle Data' to view loss development analysis")

# Methodology explanation
with st.expander("ℹ️ About Loss Development Triangles"):
    st.markdown("""
    ### What is a Loss Development Triangle?

    A loss development triangle is a fundamental actuarial tool used to:
    - Track how losses emerge and develop over time
    - Calculate age-to-age development factors
    - Project ultimate losses and IBNR reserves

    ### Key Concepts:

    - **Accident Year**: The year when the loss occurred
    - **Development Month**: Months elapsed since the accident
    - **Cumulative Triangle**: Shows total losses reported to date
    - **Incremental Triangle**: Shows losses reported in each development period
    - **Development Factors**: Ratios showing how losses develop from one period to the next
    - **IBNR**: Incurred But Not Reported - estimated unreported losses

    ### Methodology:

    This dashboard uses the **chain-ladder method** with volume-weighted development factors
    to project ultimate losses for each accident year.
    """)
