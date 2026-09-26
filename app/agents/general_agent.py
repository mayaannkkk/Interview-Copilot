from langchain_groq import ChatGroq 

llm = ChatGroq(model="qwen/qwen3.8-27b")


def general_agent(state):

    result = llm.invoke(state["query"])

    return {
        "response": result.content
    }