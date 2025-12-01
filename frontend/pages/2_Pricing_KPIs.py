"""
Pricing & Portfolio KPIs Page
Displays segment-level performance metrics.

Author: Actuarial Insights Workbench Team
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import os

st.set_page_config(page_title="Pricing & KPIs", page_icon="📊", layout="wide")

# Get backend URL
BACKEND_URL = os.getenv('BACKEND_HOST', 'localhost')
BACKEND_PORT = os.getenv('BACKEND_PORT', '8003')
API_BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"

st.title("📊 Pricing & Portfolio KPIs")
st.markdown("Analyze portfolio performance across segments")

st.markdown("---")

# Controls
col1, col2 = st.columns([2, 1])

with col1:
    segment_by = st.selectbox(
        "Segment By",
        options=["Geography", "Industry", "PolicySize", "RiskRating"],
        format_func=lambda x: {
            "Geography": "Geography (Region)",
            "Industry": "Industry Sector",
            "PolicySize": "Policy Size",
            "RiskRating": "Risk Rating (COPE)"
        }.get(x, x)
    )

with col2:
    min_premium = st.number_input(
        "Min Premium Filter ($)",
        min_value=0,
        value=0,
        step=10000,
        help="Filter out segments with earned premium below this threshold"
    )

# Fetch data button
if st.button("🔄 Load KPI Data", type="primary"):
    with st.spinner("Fetching segment KPIs..."):
        try:
            response = requests.get(
                f"{API_BASE_URL}/segment_insights",
                params={
                    "segment_by": segment_by,
                    "min_premium": min_premium
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state['kpi_data'] = data
                st.success("✅ Data loaded successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                st.session_state['kpi_data'] = None

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend API. Make sure the backend service is running.")
            st.session_state['kpi_data'] = None
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            st.session_state['kpi_data'] = None

# Display data if available
if 'kpi_data' in st.session_state and st.session_state['kpi_data']:
    data = st.session_state['kpi_data']

    st.markdown("---")

    # Overall Portfolio Metrics
    st.subheader("🎯 Overall Portfolio Performance")

    overall = data.get('overall_kpis', {})

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Premium",
            f"${overall.get('total_earned_premium', 0) / 1_000_000:.1f}M",
            help="Total earned premium"
        )

    with col2:
        lr = overall.get('loss_ratio', 0)
        st.metric(
            "Loss Ratio",
            f"{lr:.1f}%",
            delta=f"{lr - 65:.1f}% vs 65% target",
            delta_color="inverse",
            help="Incurred loss ratio"
        )

    with col3:
        freq = overall.get('frequency', 0)
        st.metric(
            "Frequency",
            f"{freq:.2f}",
            help="Claims per 100 exposure units"
        )

    with col4:
        sev = overall.get('severity', 0)
        st.metric(
            "Severity",
            f"${sev / 1000:.0f}K",
            help="Average claim amount"
        )

    with col5:
        st.metric(
            "Claim Count",
            f"{overall.get('claim_count', 0):,}",
            help="Total number of claims"
        )

    st.markdown("---")

    # Segment KPIs Table
    st.subheader(f"📋 KPIs by {segment_by}")

    segment_kpis = data.get('segment_kpis', [])

    if segment_kpis:
        df_kpis = pd.DataFrame(segment_kpis)

        # Display formatted table
        st.dataframe(
            df_kpis.style.format({
                'EarnedPremium': '${:,.0f}',
                'IncurredLoss': '${:,.0f}',
                'PaidLoss': '${:,.0f}',
                'LossRatio': '{:.2f}%',
                'PaidLossRatio': '{:.2f}%',
                'Frequency': '{:.4f}',
                'Severity': '${:,.0f}',
                'PurePremium': '${:,.2f}',
                'AvgPremium': '${:,.0f}',
                'TotalExposure': '{:,.0f}',
                'PolicyCount': '{:,.0f}',
                'ClaimCount': '{:,.0f}'
            }).background_gradient(
                subset=['LossRatio'],
                cmap='RdYlGn_r',
                vmin=40,
                vmax=100
            ),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Loss Ratio by Segment
            fig_lr = px.bar(
                df_kpis,
                x=segment_by,
                y='LossRatio',
                title=f'Loss Ratio by {segment_by}',
                color='LossRatio',
                color_continuous_scale='RdYlGn_r',
                labels={'LossRatio': 'Loss Ratio (%)'}
            )

            fig_lr.add_hline(
                y=65,
                line_dash="dash",
                line_color="red",
                annotation_text="Target 65%"
            )

            fig_lr.update_layout(height=400)
            st.plotly_chart(fig_lr, use_container_width=True)

        with col2:
            # Premium Distribution
            fig_premium = px.pie(
                df_kpis,
                values='EarnedPremium',
                names=segment_by,
                title=f'Premium Distribution by {segment_by}',
                hole=0.4
            )

            fig_premium.update_layout(height=400)
            st.plotly_chart(fig_premium, use_container_width=True)

        # Frequency vs Severity Analysis
        st.subheader("📈 Frequency vs Severity Analysis")

        fig_freq_sev = px.scatter(
            df_kpis,
            x='Frequency',
            y='Severity',
            size='EarnedPremium',
            color='LossRatio',
            hover_name=segment_by,
            title=f'Frequency vs Severity by {segment_by}',
            labels={
                'Frequency': 'Claim Frequency (per 100 units)',
                'Severity': 'Average Severity ($)',
                'EarnedPremium': 'Earned Premium'
            },
            color_continuous_scale='RdYlGn_r'
        )

        fig_freq_sev.update_layout(height=500)
        st.plotly_chart(fig_freq_sev, use_container_width=True)

        st.markdown("---")

        # Top/Bottom Performers
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Top Performing Segments")
            st.caption("Lowest loss ratios")

            top_performers = df_kpis.nsmallest(5, 'LossRatio')[[segment_by, 'LossRatio', 'EarnedPremium']]
            top_performers['LossRatio'] = top_performers['LossRatio'].apply(lambda x: f"{x:.2f}%")
            top_performers['EarnedPremium'] = top_performers['EarnedPremium'].apply(lambda x: f"${x:,.0f}")

            st.dataframe(top_performers, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("⚠️ Segments Needing Attention")
            st.caption("Highest loss ratios")

            bottom_performers = df_kpis.nlargest(5, 'LossRatio')[[segment_by, 'LossRatio', 'ClaimCount']]
            bottom_performers['LossRatio'] = bottom_performers['LossRatio'].apply(lambda x: f"{x:.2f}%")
            bottom_performers['ClaimCount'] = bottom_performers['ClaimCount'].apply(lambda x: f"{int(x):,}")

            st.dataframe(bottom_performers, use_container_width=True, hide_index=True)

    else:
        st.warning("No segment data available")

else:
    st.info("👆 Click 'Load KPI Data' to view portfolio analytics")

# KPI Definitions
with st.expander("ℹ️ KPI Definitions"):
    st.markdown("""
    ### Key Performance Indicators

    - **Loss Ratio**: Incurred losses divided by earned premium (%)
    - **Paid Loss Ratio**: Paid losses divided by earned premium (%)
    - **Frequency**: Number of claims per 100 exposure units
    - **Severity**: Average claim amount (total incurred / claim count)
    - **Pure Premium**: Loss cost per exposure unit (incurred / exposure)
    - **Earned Premium**: Premium recognized for coverage provided
    - **Exposure Units**: Measure of risk exposure (e.g., building value in $100K units)

    ### Industry Benchmarks (Commercial Property)

    - **Target Loss Ratio**: 60-70%
    - **Typical Frequency**: 0.5-2.0 claims per 100 units
    - **Expense Ratio**: ~30-35%
    - **Combined Ratio**: <100% for profitability

    ### COPE Risk Rating

    - **Construction**: Building materials and fire resistance
    - **Occupancy**: Business type and hazard level
    - **Protection**: Fire protection and security systems
    - **Exposure**: Proximity to hazards and natural disasters
    """)

# Download options
if 'kpi_data' in st.session_state and st.session_state['kpi_data']:
    segment_kpis = st.session_state['kpi_data'].get('segment_kpis', [])

    if segment_kpis:
        df_download = pd.DataFrame(segment_kpis)

        st.download_button(
            label="📥 Download KPI Data (CSV)",
            data=df_download.to_csv(index=False),
            file_name=f"segment_kpis_{segment_by}.csv",
            mime="text/csv"
        )
