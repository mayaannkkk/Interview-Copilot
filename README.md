# 🚀 Interview Copilot

Interview Copilot is an AI-powered interview preparation platform.

The platform helps candidates prepare for technical interviews through intelligent resume analysis, mock interview sessions, and an AI-powered assistant.

---

## 🌟 Features

### 📄 Resume Analyzer Agent

Upload your resume in PDF format and receive:

- Resume strengths
- Areas of improvement
- Personalized interview questions
- Skill-based feedback

### 🎤 Mock Interview Agent

Practice interviews with AI-generated questions.

- Technical interview simulation
- Topic-based interview questions
- Interactive interview preparation

### 💡 General AI Assistant

Ask questions related to:

- Artificial Intelligence
- Machine Learning
- Data Science
- Python
- FastAPI
- LangChain
- LangGraph
- Interview Preparation
- or Any domain

---

## 🏗️ Architecture

Interview Copilot uses a LangGraph-based multi-agent workflow.

```text
                    User Query
                         │
                         ▼
                  Planner Agent
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
 Resume Agent     Mock Interview      General Agent
                        Agent
      │                  │                  │
      └──────────────────┴──────────────────┘
                         │
                         ▼
                     Response
```

The Planner Agent identifies the user's intent and routes requests to the appropriate specialized agent.

---

## 🛠️ Tech Stack

### AI & Agent Frameworks

- LangGraph
- LangChain

### LLM

- Groq
- Llama 3.3 70B Versatile

### Frontend

- Streamlit

### Backend

- Python

### Libraries

- PyPDF
- Requests
- Python Dotenv

---

## 📂 Project Structure

```text
Interview-Copilot/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── resume_agent.py
│   │   ├── interviewer.py
│   │   └── general_agent.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── schemas/
│   │   └── state.py
│   │
│   ├── tools/
│   │   └── resume_tool.py
│   │
│   └── main.py
│
├── streamlit_app.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mayaannkkk/Interview-Copilot

cd interview-copilot
```

### 2. Create Virtual Environment

Using UV:

```bash
uv venv
```

Activate Environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/Mac**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

---

## 📖 How It Works

### Resume Analysis

1. Upload a PDF resume.
2. Resume text is extracted using PyPDF.
3. The Resume Agent analyzes the content.
4. Strengths, weaknesses, and personalized interview questions are generated.

### Mock Interview

1. Select Mock Interview mode.
2. Enter a topic.
3. The Interview Agent generates interview questions.
4. Practice answering technical questions.

### General Assistant

1. Ask any interview or AI-related question.
2. The General Agent responds using Groq's Llama 3.3 70B model.

---

## 🚀 Future Improvements

- Tool Calling
- Memory Support
- RAG (Retrieval-Augmented Generation)
- Interview Performance Tracking
- Personalized Learning Roadmaps
- Voice-Based Interviews
- Multi-turn Mock Interview Sessions
- Interview Scoring System

---

### Live Demo

https://interview-copilot-01.streamlit.app/

---

## 🎯 Key Learnings

Through this project, I gained hands-on experience with:

- Agentic AI Workflows
- LangGraph State Management
- Multi-Agent Architectures
- LLM Integration using Groq
- PDF Processing with PyPDF
- Streamlit Deployment
- Building End-to-End AI Applications

---

## 👨‍💻 Author

### Mayank Goyal

⭐ If you found this project useful, consider giving it a star!
