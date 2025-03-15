import streamlit as st
import plotly.graph_objects as go

def main():
    # -------------------------------------------------
    # PAGE CONFIGURATIONS
    # -------------------------------------------------
    st.set_page_config(
        page_title="Enhanced Ethical Propensity Score Dashboard",
        layout="wide"
    )
    
    # -------------------------------------------------
    # SIDEBAR CONTROLS
    # -------------------------------------------------
    st.sidebar.title("Navigation & Settings")
    
    # A simple navigation radio button
    page_selection = st.sidebar.radio(
        "Go to Section",
        ["Input Data", "Dashboard & Recommendations"]
    )
    
    # Sliders to adjust metric weights dynamically
    st.sidebar.title("Adjust Metric Weights")
    bias_weight = st.sidebar.slider("Bias Index Weight", 0, 30, 15)
    transparency_weight = st.sidebar.slider("Transparency Weight", 0, 30, 10)
    accountability_weight = st.sidebar.slider("Accountability Weight", 0, 30, 10)
    privacy_weight = st.sidebar.slider("Privacy Weight", 0, 30, 10)
    fairness_weight = st.sidebar.slider("Fairness Weight", 0, 30, 15)
    sentiment_weight = st.sidebar.slider("Sentiment Weight", 0, 30, 10)
    
    # If needed, store these weights for global usage
    st.session_state["bias_weight"] = bias_weight
    st.session_state["transparency_weight"] = transparency_weight
    st.session_state["accountability_weight"] = accountability_weight
    st.session_state["privacy_weight"] = privacy_weight
    st.session_state["fairness_weight"] = fairness_weight
    st.session_state["sentiment_weight"] = sentiment_weight
    
    # -------------------------------------------------
    # PAGE 1: INPUT DATA
    # -------------------------------------------------
    if page_selection == "Input Data":
        st.title("Enhanced EPS Dashboard – Data Entry")
        st.write("Use this page to enter your AI hiring metrics. Then switch to the 'Dashboard & Recommendations' page to view results.")
        
        # Use session_state to preserve form data across page switches
        if "total_decisions" not in st.session_state:
            st.session_state["total_decisions"] = 1
        
        # -- Basic Data Entry --
        with st.form("basic_data_form", clear_on_submit=False):
            st.subheader("Basic Information")
            
            total_decisions = st.number_input(
                "Total AI Decisions", 
                min_value=1, 
                value=st.session_state["total_decisions"]
            )
            bias_complaints = st.number_input("Number of Bias Complaints", min_value=0, value=0)
            explainable_ai = st.number_input("Explainable AI Decisions", min_value=0, value=0)
            human_reviewed = st.number_input("Human-Reviewed Decisions", min_value=0, value=0)
            data_transactions = st.number_input("Total Data Transactions", min_value=1, value=1)
            
            st.subheader("Advanced Inputs")
            policy_violations = st.number_input("Policy Violations Detected", min_value=0, value=0)
            diverse_hires = st.number_input("Number of Diverse Hires", min_value=0, value=0)
            total_hires = st.number_input("Total Hires", min_value=1, value=1)
            positive_feedback = st.number_input("Positive Feedback (count)", min_value=0, value=0)
            total_feedback = st.number_input("Total Feedback (count)", min_value=1, value=1)
            
            # Submit button
            submitted = st.form_submit_button("Save & Proceed")
            if submitted:
                # store the data in session_state
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
                
                st.success("Data saved successfully! Please switch to 'Dashboard & Recommendations' to see the results.")

    # -------------------------------------------------
    # PAGE 2: DASHBOARD & RECOMMENDATIONS
    # -------------------------------------------------
    else:
        st.title("EPS Results & Recommendations")
        
        # retrieve data from session_state
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
        if total_decisions == 0:
            total_decisions = 1
        if total_hires == 0:
            total_hires = 1
        if data_transactions == 0:
            data_transactions = 1
        if total_feedback == 0:
            total_feedback = 1
        
        # 1. Bias Index
        bias_index = (bias_complaints / total_decisions) * 100
        # 2. Transparency Score
        transparency_score = (explainable_ai / total_decisions) * 100
        # 3. Accountability Index
        accountability_index = (human_reviewed / total_decisions) * 100
        # 4. Privacy Compliance Score
        privacy_compliance = ((data_transactions - policy_violations) / data_transactions) * 100
        # 5. Fairness Index
        fairness_index = (diverse_hires / total_hires) * 100
        # 6. Stakeholder Sentiment
        stakeholder_sentiment = (positive_feedback / total_feedback) * 100
        
        # Weighted sum
        sum_of_weights = bias_w + transp_w + acc_w + priv_w + fair_w + sent_w
        if sum_of_weights == 0:
            sum_of_weights = 1  # avoid zero division if all sliders are zero
        
        eps = (
            (bias_index * bias_w) +
            (transparency_score * transp_w) +
            (accountability_index * acc_w) +
            (privacy_compliance * priv_w) +
            (fairness_index * fair_w) +
            (stakeholder_sentiment * sent_w)
        ) / sum_of_weights
        
        # Display data in tabs for a nicer layout
        tab1, tab2 = st.tabs(["Dashboard", "Recommendations"])
        
        with tab1:
            st.subheader("EPS Dashboard")
            
            colA, colB, colC = st.columns(3)
            colA.metric("Bias Index (%)", f"{bias_index:.2f}")
            colA.metric("Transparency (%)", f"{transparency_score:.2f}")
            colB.metric("Accountability (%)", f"{accountability_index:.2f}")
            colB.metric("Privacy Compliance (%)", f"{privacy_compliance:.2f}")
            colC.metric("Fairness (%)", f"{fairness_index:.2f}")
            colC.metric("Sentiment (%)", f"{stakeholder_sentiment:.2f}")
            
            # Show EPS as a gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = eps,
                title = {'text': "Ethical Propensity Score (EPS)"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "red"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "green"}
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"**Current EPS:** {eps:.2f} / 100")
        
        with tab2:
            st.subheader("Recommendations")
            if eps < 40:
                st.error("Your EPS is critically low. Immediate intervention is required to reduce bias and strengthen compliance.")
            elif eps < 70:
                st.warning("Your EPS is moderate. You may need to refine data collection, expand human oversight, and improve transparency.")
            else:
                st.success("Your EPS is high! Maintain continuous audits and stakeholder engagement to keep ethical standards strong.")
            
            # Additional recommended actions based on metrics
            if bias_index > 10:
                st.write("- **Action**: Investigate underlying data for potential biases. Consider re-training or re-tuning your AI models.")
            if fairness_index < 50:
                st.write("- **Action**: Check pipeline diversity. Partner with community organizations or implement targeted outreach to underrepresented groups.")
            if privacy_compliance < 90:
                st.write("- **Action**: Audit data handling processes. Ensure alignment with GDPR, CCPA, or other relevant regulations.")
            if accountability_index < 50:
                st.write("- **Action**: Increase human oversight in final selection. Consider 'human-in-the-loop' checks on borderline AI decisions.")

if __name__ == "__main__":
    main()
