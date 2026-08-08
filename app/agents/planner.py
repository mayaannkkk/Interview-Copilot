import os
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def planner_node(state):
    query = state["query"]

    # Deterministic short-circuit: if the query is a real, existing PDF
    # file path, it's a resume upload — skip the LLM classification
    # entirely, since the LLM has no way to know a bare file path is a
    # resume (it just sees a string like "C:\...\tmp123.pdf").
    if isinstance(query, str) and query.strip().lower().endswith(".pdf") and os.path.exists(query.strip()):
        print("[DEBUG] Planner: query is an existing .pdf path -> routing to resume_analysis")
        return {"route": "resume_analysis"}

    prompt = f"""
    Classify the query into one of:

    resume_analysis
    mock_interview
    general

    Query:
    {query}

    Return only category.
    """

    content = llm.invoke(prompt).content
    if isinstance(content, list):
        route = "".join(
            c.get("text", "") if isinstance(c, dict) else c
            for c in content
        ).strip()
    else:
        route = content.strip()

    print(f"[DEBUG] Planner: LLM classified route as {route!r}")

    return {
        "route": route
    }