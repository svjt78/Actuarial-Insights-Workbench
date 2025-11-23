"""
GenAI Insights Page
Natural language explanations powered by OpenAI GPT-3.5.

Author: Actuarial Insights Workbench Team
"""

import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="GenAI Insights", page_icon="🤖", layout="wide")

# Get backend URL
BACKEND_URL = os.getenv('BACKEND_HOST', 'localhost')
BACKEND_PORT = os.getenv('BACKEND_PORT', '8000')
API_BASE_URL = f"http://{BACKEND_URL}:{BACKEND_PORT}"

st.title("🤖 GenAI Insights & Explanations")
st.markdown("Ask questions about your portfolio and get expert actuarial explanations")

st.markdown("---")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Explanation type selector
explanation_mode = st.radio(
    "Choose Analysis Mode:",
    options=["Question & Answer", "Loss Ratio Analysis", "Trend Explanation", "Risk Rating Explanation"],
    horizontal=True
)

st.markdown("---")

# Question & Answer Mode
if explanation_mode == "Question & Answer":
    st.subheader("💬 Ask About Your Portfolio")

    # Provide context
    col1, col2 = st.columns([2, 1])

    with col1:
        question = st.text_area(
            "Your Question:",
            height=100,
            placeholder="Example: What factors are driving the high loss ratio in the Manufacturing sector?",
            help="Ask any question about actuarial metrics, trends, or insights"
        )

    with col2:
        st.markdown("**Sample Questions:**")
        st.markdown("""
        - What is causing the loss ratio trend?
        - Which segments should we focus on?
        - How does geography impact severity?
        - Should we adjust pricing in the West region?
        - What drives claim frequency in Manufacturing?
        """)

    if st.button("🔍 Get Answer", type="primary"):
        if question.strip():
            with st.spinner("Analyzing your question..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/explain",
                        json={
                            "explanation_type": "question",
                            "data": {
                                "question": question,
                                "context_data": {
                                    "portfolio": "Commercial Property",
                                    "policies": 1000,
                                    "overall_lr": 12.0
                                }
                            }
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()
                        explanation = result.get('explanation', 'No explanation generated')

                        # Add to chat history
                        st.session_state.chat_history.append({
                            "question": question,
                            "answer": explanation
                        })

                        st.success("✅ Analysis complete!")
                        st.markdown("### 💡 Answer:")
                        st.info(explanation)

                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend API. Make sure the backend service is running.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question")

# Loss Ratio Analysis Mode
elif explanation_mode == "Loss Ratio Analysis":
    st.subheader("📊 Explain Loss Ratio Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        segment_name = st.text_input("Segment Name", value="Northeast", help="Name of the segment to analyze")

    with col2:
        actual_lr = st.number_input("Actual Loss Ratio (%)", value=75.0, min_value=0.0, max_value=200.0, step=5.0)

    with col3:
        benchmark_lr = st.number_input("Benchmark/Target (%)", value=65.0, min_value=0.0, max_value=200.0, step=5.0)

    # Optional context
    with st.expander("➕ Add Additional Context"):
        claim_count = st.number_input("Number of Claims", value=25, min_value=0)
        premium = st.number_input("Earned Premium ($)", value=1000000.0, min_value=0.0)
        time_period = st.selectbox("Time Period", ["Current Year", "YTD", "Last 12 Months", "All Time"])

    if st.button("🎯 Explain Loss Ratio", type="primary"):
        with st.spinner("Generating explanation..."):
            try:
                context = {
                    "claim_count": claim_count,
                    "earned_premium": premium,
                    "time_period": time_period
                }

                response = requests.post(
                    f"{API_BASE_URL}/explain",
                    json={
                        "explanation_type": "loss_ratio",
                        "data": {
                            "segment": segment_name,
                            "loss_ratio": actual_lr,
                            "benchmark": benchmark_lr,
                            "context": context
                        }
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    explanation = result.get('explanation', 'No explanation generated')

                    # Display variance
                    variance = actual_lr - benchmark_lr
                    if variance > 0:
                        st.error(f"⚠️ Loss ratio is **{variance:.1f} points above** benchmark")
                    else:
                        st.success(f"✅ Loss ratio is **{abs(variance):.1f} points below** benchmark")

                    st.markdown("### 💡 Analysis:")
                    st.info(explanation)

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Trend Explanation Mode
elif explanation_mode == "Trend Explanation":
    st.subheader("📈 Explain Metric Trends")

    metric_name = st.selectbox(
        "Select Metric:",
        options=["Loss Ratio", "Claim Frequency", "Severity", "Premium Growth", "Claim Count"]
    )

    trend_direction = st.radio(
        "Trend Direction:",
        options=["Increasing", "Decreasing", "Neutral"],
        horizontal=True
    )

    # Manual trend data input
    st.markdown("**Trend Data (Recent Periods):**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        period1 = st.number_input("Period 1", value=60.0, help="Oldest period")

    with col2:
        period2 = st.number_input("Period 2", value=65.0)

    with col3:
        period3 = st.number_input("Period 3", value=70.0)

    with col4:
        period4 = st.number_input("Period 4 (Latest)", value=75.0, help="Most recent")

    if st.button("📊 Explain Trend", type="primary"):
        with st.spinner("Analyzing trend..."):
            try:
                trend_data = {
                    "Period_1": period1,
                    "Period_2": period2,
                    "Period_3": period3,
                    "Period_4_Latest": period4,
                    "change": period4 - period1,
                    "avg": (period1 + period2 + period3 + period4) / 4
                }

                response = requests.post(
                    f"{API_BASE_URL}/explain",
                    json={
                        "explanation_type": "trend",
                        "data": {
                            "metric_name": metric_name,
                            "trend_data": trend_data,
                            "trend_direction": trend_direction.lower()
                        }
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    explanation = result.get('explanation', 'No explanation generated')

                    st.markdown("### 💡 Trend Analysis:")
                    st.info(explanation)

                    # Show data
                    with st.expander("📊 View Trend Data"):
                        st.json(trend_data)

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Risk Rating Explanation Mode
elif explanation_mode == "Risk Rating Explanation":
    st.subheader("🎯 Explain COPE Risk Rating")

    col1, col2, col3 = st.columns(3)

    with col1:
        risk_rating_val = st.slider("Risk Rating", min_value=1.0, max_value=10.0, value=6.5, step=0.5)

    with col2:
        geography_val = st.selectbox("Geography", ["Northeast", "Southeast", "Midwest", "Southwest", "West", "Northwest"])

    with col3:
        industry_val = st.selectbox("Industry", ["Manufacturing", "Retail", "Office", "Warehouse", "Healthcare", "Education", "Hospitality", "Technology"])

    if st.button("🔍 Explain Rating", type="primary"):
        with st.spinner("Generating explanation..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/explain",
                    json={
                        "explanation_type": "cope_rating",
                        "data": {
                            "risk_rating": risk_rating_val,
                            "geography": geography_val,
                            "industry": industry_val
                        }
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    explanation = result.get('explanation', 'No explanation generated')

                    # Risk level indicator
                    if risk_rating_val <= 3.5:
                        st.success(f"✅ **Low Risk** (Rating: {risk_rating_val}/10)")
                    elif risk_rating_val <= 6.5:
                        st.info(f"ℹ️ **Moderate Risk** (Rating: {risk_rating_val}/10)")
                    else:
                        st.warning(f"⚠️ **High Risk** (Rating: {risk_rating_val}/10)")

                    st.markdown("### 💡 Risk Assessment:")
                    st.info(explanation)

                    # COPE framework reminder
                    with st.expander("📚 COPE Framework Reference"):
                        st.markdown("""
                        **COPE Risk Factors:**

                        - **Construction** - Building materials, fire resistance, structural integrity
                        - **Occupancy** - Business type, hazard level, security
                        - **Protection** - Sprinklers, fire alarms, security systems
                        - **Exposure** - Proximity to hazards, natural disaster risk, neighboring properties
                        """)

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Chat History
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("💬 Conversation History")

    for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
        with st.expander(f"Q: {chat['question'][:80]}...", expanded=(i == 0)):
            st.markdown(f"**Question:** {chat['question']}")
            st.markdown(f"**Answer:** {chat['answer']}")

    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# Information
st.markdown("---")

with st.expander("ℹ️ About GenAI Insights"):
    st.markdown("""
    ### How It Works

    This feature uses **OpenAI GPT-3.5-turbo** to provide natural language explanations
    of actuarial metrics and trends.

    ### Capabilities:

    - **Question & Answer**: Ask any question about your portfolio
    - **Loss Ratio Analysis**: Understand performance vs benchmarks
    - **Trend Explanation**: Get insights on metric movements
    - **Risk Rating**: Explain COPE-based risk assessments

    ### Model Information:

    - **Model**: GPT-3.5-turbo
    - **Temperature**: 0.7 (balanced creativity and accuracy)
    - **Max Tokens**: 300-400 (concise responses)
    - **Context**: Actuarial expertise in Commercial Property insurance

    ### Privacy & Security:

    - API calls are made through secure backend
    - No sensitive policy or customer data is sent to OpenAI
    - Explanations are generated based on aggregated metrics only

    ### Best Practices:

    - Provide specific questions for better answers
    - Include relevant context (time periods, segments)
    - Use explanations to complement, not replace, expert judgment
    - Verify insights with underlying data
    """)

with st.expander("🎓 Sample Use Cases"):
    st.markdown("""
    ### Underwriting:
    - "Should we accept this risk with a 7.5 risk rating in the West region?"
    - "What underwriting guidelines should we adjust for Manufacturing?"

    ### Pricing:
    - "Why is our loss ratio trending upward in the Southeast?"
    - "How should we price Small vs Large policies differently?"

    ### Portfolio Management:
    - "Which segments are driving our portfolio loss ratio?"
    - "What actions should we take on segments with LR > 80%?"

    ### Claims:
    - "What's causing the increase in severity for Warehouse properties?"
    - "How does claim frequency vary by geography?"
    """)
