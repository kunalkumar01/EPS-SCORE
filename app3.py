import streamlit as st
import plotly.graph_objects as go

# ----- Custom CSS for improved look -----
custom_css = """
<style>
.main > div {padding-top: 1rem;}
.block-container {
    padding: 1rem 2rem;
    border-radius: 8px;
    background-color: #f7f9fc; 
}
h1, h2, h3, h4 {
    font-family: 'Arial', sans-serif;
    letter-spacing: -0.5px;
}
[data-testid="stSidebar"] {
    background-color: #ECEEF1;
}
[data-testid="stHeader"] {
    background-color: #FFF;
}
.css-1v0mbdj, .css-12oz5g7 {
    background-color: #FFFFFF;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
}
.css-1xm32e0 {
    background-color: #fff !important; 
    border-radius: 8px;
    padding-top: 1rem !important;
}
.stTabs [role="tablist"] button [data-baseweb="tab"] {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
}
.stTabs [role="tablist"] button[data-selected="true"] [data-baseweb="tab"] {
    color: #1464F4; 
    border-bottom: 3px solid #1464F4;
}
button:hover {
    cursor: pointer;
    opacity: 0.9;
}
.st-alert {
    border-radius: 6px;
}
</style>
"""

def main():
    # Page config
    st.set_page_config(
        page_title="Ethical Propensity Score Dashboard",
        layout="wide",
    )
    
    # Inject custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # ----- LOGO SECTION -----
    # Attempt to display your Google Images link:
    logo_url = "https://images.app.goo.gl/kFzKTNFxSZfkqgHX8"
    st.image(logo_url, width=150)
    
    # Dashboard title
    st.title("Ethical Propensity Score (EPS) Dashboard")
    st.write("**Vinod Gupta School of Management, IIT Kharagpur**")

    # Sidebar
    st.sidebar.title("Navigation & Settings")
    
    # Developer names
    with st.sidebar.expander("Developed By"):
        st.write("1. Kunal Kumar")
        st.write("2. Amit Kumar Ray")
        st.write("3. Sumit Saphui")
        st.write("4. Chayan Bera")
        st.write("5. Prabhakar Kumar Gaurav")
        st.write("6. Shrestha Dey")
    
    page_selection = st.sidebar.radio(
        "Go to Section",
        ["Data Input", "EPS Dashboard"]
    )
    
    st.sidebar.write("---")
    st.sidebar.subheader("Adjust Metric Weights")
    bias_weight = st.sidebar.slider("Bias Index Weight", 0, 30, 15)
    transparency_weight = st.sidebar.slider("Transparency Weight", 0, 30, 10)
    accountability_weight = st.sidebar.slider("Accountability Weight", 0, 30, 10)
    privacy_weight = st.sidebar.slider("Privacy Weight", 0, 30, 10)
    fairness_weight = st.sidebar.slider("Fairness Weight", 0, 30, 15)
    sentiment_weight = st.sidebar.slider("Sentiment Weight", 0, 30, 10)
    
    # Store in session_state
    st.session_state["bias_weight"] = bias_weight
    st.session_state["transparency_weight"] = transparency_weight
    st.session_state["accountability_weight"] = accountability_weight
    st.session_state["privacy_weight"] = privacy_weight
    st.session_state["fairness_weight"] = fairness_weight
    st.session_state["sentiment_weight"] = sentiment_weight
    
    # -------------- PAGE 1: DATA INPUT --------------
    if page_selection == "Data Input":
        st.subheader("AI Hiring Metrics: Data Entry")
        st.write("""
        Enter your AI hiring metrics in the form below. 
        Then switch to the **EPS Dashboard** (in the sidebar) 
        to view live calculations, recommendations, and interactive charts.
        """)
        
        st.write("### Step 1: Basic Inputs")
        col1, col2 = st.columns(2)
        with col1:
            total_decisions = st.number_input("Total AI Decisions", min_value=1, value=100)
            bias_complaints = st.number_input("Number of Bias Complaints", min_value=0, value=5)
            explainable_ai = st.number_input("Explainable AI Decisions", min_value=0, value=60)
            human_reviewed = st.number_input("Human-Reviewed Decisions", min_value=0, value=30)
        with col2:
            data_transactions = st.number_input("Total Data Transactions", min_value=1, value=500)
            policy_violations = st.number_input("Policy Violations Detected", min_value=0, value=1)
            diverse_hires = st.number_input("Number of Diverse Hires", min_value=0, value=20)
            total_hires = st.number_input("Total Hires", min_value=1, value=40)
        
        st.write("### Step 2: Feedback & Sentiment")
        positive_feedback = st.number_input("Positive Feedback (count)", min_value=0, value=80)
        total_feedback = st.number_input("Total Feedback (count)", min_value=1, value=100)
        
        st.write("---")
        if st.button("Save Values"):
            st.session_state["total_decisions"] = total_decisions
            st.session_state["bias_complaints"] = bias_complaints
            st.session_state["explainable_ai"] = explainable_ai
            st.session_state["human_reviewed"] = human_reviewed
            st.session_state["data_transactions"] = data_transactions
            st.session_state["policy_violations"] = policy_violations
            st.session_state["diverse_hires"] = diverse_hires
            st.session_state["total_hires"] = total_hires
            st.session_state["positive_feedback"] = positive_feedback
            st.session_state["total_feedback"] = total_feedback
            
            st.success("Data saved! Navigate to 'EPS Dashboard' to see real-time calculations.")
    
    # -------------- PAGE 2: EPS DASHBOARD --------------
    else:
        st.subheader("EPS Dashboard & Recommendations")
        
        # Retrieve data or set defaults
        total_decisions = st.session_state.get("total_decisions", 1)
        bias_complaints = st.session_state.get("bias_complaints", 0)
        explainable_ai = st.session_state.get("explainable_ai", 0)
        human_reviewed = st.session_state.get("human_reviewed", 0)
        data_transactions = st.session_state.get("data_transactions", 1)
        policy_violations = st.session_state.get("policy_violations", 0)
        diverse_hires = st.session_state.get("diverse_hires", 0)
        total_hires = st.session_state.get("total_hires", 1)
        positive_feedback = st.session_state.get("positive_feedback", 0)
        total_feedback = st.session_state.get("total_feedback", 1)
        
        # Weights
        bias_w = st.session_state["bias_weight"]
        transp_w = st.session_state["transparency_weight"]
        acc_w = st.session_state["accountability_weight"]
        priv_w = st.session_state["privacy_weight"]
        fair_w = st.session_state["fairness_weight"]
        sent_w = st.session_state["sentiment_weight"]
        
        # Avoid division by zero
        if total_decisions == 0: total_decisions = 1
        if total_hires == 0: total_hires = 1
        if data_transactions == 0: data_transactions = 1
        if total_feedback == 0: total_feedback = 1
        
        # Calculate metrics
        bias_index = (bias_complaints / total_decisions) * 100
        transparency_score = (explainable_ai / total_decisions) * 100
        accountability_index = (human_reviewed / total_decisions) * 100
        privacy_compliance = ((data_transactions - policy_violations) / data_transactions) * 100
        fairness_index = (diverse_hires / total_hires) * 100
        stakeholder_sentiment = (positive_feedback / total_feedback) * 100
        
        # Weighted average
        sum_of_weights = (bias_w + transp_w + acc_w + priv_w + fair_w + sent_w)
        if sum_of_weights == 0:
            sum_of_weights = 1
        
        eps = (
            (bias_index * bias_w) +
            (transparency_score * transp_w) +
            (accountability_index * acc_w) +
            (privacy_compliance * priv_w) +
            (fairness_index * fair_w) +
            (stakeholder_sentiment * sent_w)
        ) / sum_of_weights
        
        # TABS
        tab1, tab2 = st.tabs(["EPS Metrics", "Recommendations"])
        
        with tab1:
            st.write("### AI Hiring Metrics Overview")
            colA, colB, colC = st.columns(3)
            colA.metric("Bias Index (%)", f"{bias_index:.2f}")
            colA.metric("Transparency (%)", f"{transparency_score:.2f}")
            colB.metric("Accountability (%)", f"{accountability_index:.2f}")
            colB.metric("Privacy (%)", f"{privacy_compliance:.2f}")
            colC.metric("Fairness (%)", f"{fairness_index:.2f}")
            colC.metric("Sentiment (%)", f"{stakeholder_sentiment:.2f}")
            
            st.write("### Overall Ethical Propensity Score")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = eps,
                title = {'text': "Ethical Propensity Score (EPS)", 'font': {'size': 18}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 2},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "red"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "green"}
                    ],
                }
            ))
            fig.update_layout(height=300, margin=dict(l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"**EPS:** {eps:.2f} / 100")

        with tab2:
            st.write("### Tailored Recommendations")
            if eps < 40:
                st.error("EPS is critically low. Immediate action required to reduce bias and improve oversight.")
            elif eps < 70:
                st.warning("EPS is moderate. Consider additional transparency measures, improved data collection, and deeper audits.")
            else:
                st.success("EPS is strong! Continue regular audits and keep refining AI models to maintain high ethical standards.")
            
            st.write("---")
            st.write("#### Metric-Specific Suggestions")
            if bias_index > 10:
                st.write("- **High Bias Index:** Investigate training data for skew, re-check feature importance, and consider re-tuning your AI models.")
            if fairness_index < 50:
                st.write("- **Low Fairness Index:** Partner with diverse job boards and community organizations. Ensure job descriptions attract underrepresented groups.")
            if privacy_compliance < 90:
                st.write("- **Privacy Gaps:** Conduct a data audit to ensure compliance with GDPR/CCPA. Limit data retention for unselected candidates.")
            if accountability_index < 50:
                st.write("- **Accountability Shortfall:** Increase human-in-the-loop reviews for borderline AI decisions; ensure final hiring decisions involve a person.")
            if transparency_score < 50:
                st.write("- **Low Transparency:** Provide clearer explanations to candidates on why they were (or weren’t) selected. Implement an 'explainable AI' framework.")
            if stakeholder_sentiment < 70:
                st.write("- **Improving Sentiment:** Collect more feedback from applicants and employees to refine the user experience around AI-driven hiring.")

            st.write("---")
            st.info("**Tip:** Adjust the metric weights in the sidebar to reflect your organization’s priorities or regulatory focus (e.g., emphasis on fairness vs. privacy).")


if __name__ == "__main__":
    main()
