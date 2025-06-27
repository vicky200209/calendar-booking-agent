from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    start: str
    end: str
    available: bool
    status: str
    event_link: str
from langgraph.graph import StateGraph
import requests

# This function simulates parsing natural language into datetime (for now, hardcoded)
def parse_user_input(state):
    user_input = state["user_input"].lower()

    # Simple pattern simulation — you can later plug in GPT/OpenAI here
    if "tomorrow" in user_input:
        start = "2025-07-01T15:00:00+05:30"
        end = "2025-07-01T16:00:00+05:30"
    elif "friday" in user_input:
        start = "2025-07-05T14:00:00+05:30"
        end = "2025-07-05T15:00:00+05:30"
    else:
        start = "2025-07-02T11:00:00+05:30"
        end = "2025-07-02T12:00:00+05:30"

    return {
        "user_input": user_input,
        "start": start,
        "end": end
    }

# Check if the time is available using FastAPI
def check_availability(state):
    res = requests.get("http://localhost:8000/availability/", params={
        "start": state["start"],
        "end": state["end"]
    })
    return {
        **state,
        "available": res.json()["available"]
    }

# Book the event if available
def confirm_booking(state):
    if not state["available"]:
        return {"status": "unavailable", **state}

    res = requests.post("http://localhost:8000/book/", json={
        "summary": "Meeting booked by AI",
        "start": state["start"],
        "end": state["end"]
    })
    return {
        "status": "booked",
        "event_link": res.json().get("event_link"),
        **state
    }

# Build LangGraph agent
def build_agent():
    graph = StateGraph(AgentState)
    graph.set_entry_point("parse_user_input")
    graph.add_node("parse_user_input", parse_user_input)
    graph.add_node("check", check_availability)
    graph.add_node("confirm", confirm_booking)
    graph.add_edge("parse_user_input", "check")
    graph.add_edge("check", "confirm")
    graph.set_finish_point("confirm")
    return graph.compile()

# Export the compiled agent
agent = build_agent()
