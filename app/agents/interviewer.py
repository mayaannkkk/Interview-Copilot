from langchain_groq import ChatGroq 

llm = ChatGroq(model="llama-3.3-70b-versatile")


def interviewer_node(state):

    query = state["query"]

    prompt = f"""
    Generate 5 interview questions on:

    {query}

    Difficulty:
    Intermediate
    """

    result = llm.invoke(prompt)

    return {
        "response": result.content
    }