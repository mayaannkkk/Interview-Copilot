from langchain_groq import ChatGroq 

llm = ChatGroq(model="openai/gpt-oss-120b")


def general_agent(state):

    result = llm.invoke(state["query"])

    return {
        "response": result.content
    }