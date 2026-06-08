import time
import requests
import streamlit as st

API_URL =  "https://financial-research-agent-co3y.onrender.com"      #"http://localhost:8000"

st.set_page_config(page_title="Financial Research Agent", page_icon="📈", layout="wide")
st.title("📈 Financial Research Agent")
st.caption("Powered by LangGraph + SEC EDGAR + NewsAPI")

ticker = st.text_input("Enter stock ticker", placeholder="e.g. AAPL, GOOGL, MSFT").strip().upper()

if st.button("Run Research", disabled=not ticker):
    with st.spinner(f"Starting research for {ticker}..."):
        try:
            resp = requests.post(f"{API_URL}/research", json={"ticker": ticker}, timeout=10)
            resp.raise_for_status()
            job_id = resp.json()["job_id"]
        except Exception as e:
            st.error(f"Failed to start research: {e}")
            st.stop()

    st.info(f"Job started: `{job_id}`")
    progress = st.progress(0, text="Running agent pipeline...")

    for i in range(120):
        time.sleep(5)
        try:
            poll = requests.get(f"{API_URL}/research/{job_id}", timeout=10)
            data = poll.json()
        except Exception:
            continue

        progress.progress(min((i + 1) / 120, 0.99), text=f"Status: {data.get('status', 'running')}...")

        if data.get("status") == "completed":
            progress.progress(1.0, text="Done!")
            result = data.get("result", {})

            st.success("Research complete!")

            col1, col2, col3 = st.columns(3)
            market = result.get("market_data", {})
            col1.metric("Current Price", f"${market.get('current_price', 'N/A')}")
            col2.metric("Recommendation", result.get("recommendation", "N/A"))
            col3.metric("Confidence", f"{result.get('confidence_score', 0):.0%}")

            with st.expander("Executive Summary", expanded=True):
                st.write(result.get("executive_summary", "N/A"))

            with st.expander("Financial Analysis"):
                st.write(result.get("financial_analysis", "N/A"))

            with st.expander("Sentiment Analysis"):
                st.write(result.get("sentiment_analysis", "N/A"))
                st.metric("Sentiment Score", f"{result.get('sentiment_score', 0):.2f}")

            with st.expander("Detailed Report"):
                st.write(result.get("detailed_report", "N/A"))

            with st.expander("Raw Market Data"):
                st.json(market)

            break
    else:
        st.warning("Research is taking longer than expected. Check back later.")
