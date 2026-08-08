import os
import tempfile
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the LangGraph compiled graph directly for local execution fallback
from app.graph.workflow import graph

st.set_page_config(
    page_title="AI Agentic Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #9333EA, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge-route {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .badge-resume { background-color: #1E1B4B; color: #818CF8; border: 1px solid #4338CA; }
    .badge-interview { background-color: #14532D; color: #4ADE80; border: 1px solid #15803D; }
    .badge-general { background-color: #4C1D95; color: #C084FC; border: 1px solid #6B21A8; }
    
    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-title">🎯 AI Agentic Interview Coach</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent interview prep powered by LangGraph routing & Groq LLMs</div>', unsafe_allow_html=True)

# Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/brain.png", width=64)
    st.header("⚙️ Configuration")
    
    execution_mode = st.radio(
        "Execution Engine",
        ["Direct LangGraph Engine", "FastAPI Service (http://127.0.0.1:8000)"],
        help="Choose whether to invoke the LangGraph workflow directly in Python or send requests to the running FastAPI server."
    )
    
    api_url = st.text_input("FastAPI Base URL", value="http://127.0.0.1:8000")
    
    st.divider()
    
    st.header("🛠️ Features")
    st.markdown("""
    - 📄 **Resume Critique**: Detailed analysis, strengths, weaknesses & tailored questions.
    - ❓ **Mock Interview Questions**: Custom intermediate questions on any domain or topic.
    - 💬 **General Interview Advice**: Behavioral tips, star method, salary negotiation & more.
    """)
    
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Interview Coach. You can ask me general interview questions, upload a resume for review, or request mock interview practice on any topic!", "route": None}
    ]

# Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("route"):
            route = message["route"].lower()
            badge_class = "badge-general"
            if "resume" in route:
                badge_class = "badge-resume"
            elif "interview" in route or "mock" in route:
                badge_class = "badge-interview"
            st.markdown(f'<span class="badge-route {badge_class}">Routed to: {message["route"].upper()}</span>', unsafe_allow_html=True)
        st.markdown(message["content"])

# Quick Upload Section in Expander
with st.expander("📄 Upload Resume (PDF) for Quick Analysis", expanded=False):
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Analyze Uploaded Resume"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            st.session_state.messages.append({"role": "user", "content": f"Analyze uploaded resume file: {uploaded_file.name}"})
            
            with st.spinner("Analyzing resume via LangGraph Resume Agent..."):
                try:
                    if "FastAPI" in execution_mode:
                        response = requests.post(f"{api_url}/chat", params={"query": tmp_path})
                        if response.status_code == 200:
                            data = response.json()
                            bot_response = data.get("response", "No response returned.")
                            route = data.get("route", "resume_analysis")
                        else:
                            bot_response = f"FastAPI Error ({response.status_code}): {response.text}"
                            route = "error"
                    else:
                        data = graph.invoke({"query": tmp_path})
                        bot_response = data.get("response", "No response generated.")
                        route = data.get("route", "resume_analysis")
                except Exception as e:
                    bot_response = f"Error processing resume: {str(e)}"
                    route = "error"
                finally:
                    if os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass

            st.session_state.messages.append({"role": "assistant", "content": bot_response, "route": route})
            st.rerun()

# Chat Input Handler
if prompt := st.chat_input("Ask a question, paste resume text, or request mock interview questions..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Routing query through AI agents..."):
            try:
                if "FastAPI" in execution_mode:
                    response = requests.post(f"{api_url}/chat", params={"query": prompt})
                    if response.status_code == 200:
                        data = response.json()
                        bot_response = data.get("response", "No response returned.")
                        route = data.get("route", "general")
                    else:
                        bot_response = f"FastAPI Error ({response.status_code}): {response.text}"
                        route = "error"
                else:
                    data = graph.invoke({"query": prompt})
                    bot_response = data.get("response", "No response generated.")
                    route = data.get("route", "general")
            except Exception as e:
                bot_response = f"An error occurred while communicating with the agent: {str(e)}"
                route = "error"

        if route and route != "error":
            route_str = route.lower()
            badge_class = "badge-general"
            if "resume" in route_str:
                badge_class = "badge-resume"
            elif "interview" in route_str or "mock" in route_str:
                badge_class = "badge-interview"
            st.markdown(f'<span class="badge-route {badge_class}">Routed to: {route.upper()}</span>', unsafe_allow_html=True)
            
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response, "route": route})
