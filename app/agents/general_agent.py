from langchain_groq import ChatGroq 

llm = ChatGroq(model="qwen/qwen3.6-27b")


def general_agent(state):

    result = llm.invoke(state["query"])

    return {
        "response": result.content
    }