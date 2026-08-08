from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.graph.workflow import graph


app = FastAPI()

@app.get('/')
def home():
    return "Welcome to the Interview Coach API"

# Chat Endpoint (POST)
@app.post("/chat")
def chat(query: str):

    result = graph.invoke(
        {
            "query": query
        }
    )

    return result