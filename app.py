import streamlit as st
from agent import agent

st.title("🤖 Calendar Booking Assistant")

user_input = st.text_input("Ask me to book a meeting:")

if user_input:
    result = agent.invoke({"user_input": user_input})
    if result["status"] == "booked":
        st.success("✅ Meeting booked!")
        st.markdown(f"[View in Google Calendar]({result['event_link']})")
    elif result["status"] == "unavailable":
        st.warning("⚠️ That time slot is not available.")
    else:
        st.info("I couldn't understand your request.")
