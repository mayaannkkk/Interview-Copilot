from langgraph.graph import StateGraph, END
from app.schemas.state import InterviewState

from app.agents.planner import planner_node
from app.agents.resume_agent import resume_agent
from app.agents.interviewer import interviewer_node
from app.agents.general_agent import general_agent

builder = StateGraph(InterviewState) # pyrefly: ignore

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "resume",
    resume_agent
)

builder.add_node(
    "interview",
    interviewer_node
)

builder.add_node(
    "general",
    general_agent
)

builder.set_entry_point("planner")

def route_decision(state):
    route = state.get("route", "").lower()
    if "resume" in route:
        return "resume"
    elif "interview" in route or "mock" in route:
        return "interview"
    else:
        return "general"

builder.add_conditional_edges(
    "planner",
    route_decision,
    {
        "resume": "resume",
        "interview": "interview",
        "general": "general"
    }
)

builder.add_edge("resume", END)
builder.add_edge("interview", END)
builder.add_edge("general", END)

graph = builder.compile()