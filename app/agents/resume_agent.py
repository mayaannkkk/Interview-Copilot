import os
import re
from langchain_groq import ChatGroq
from app.tools.resume_tool import extract_resume_text

llm = ChatGroq(model="llama-3.3-70b-versatile")

# Matches a Windows-style absolute path ending in .pdf, even if it's
# embedded inside other text (e.g. "Analyze this: C:\...\tmp123.pdf.")
PDF_PATH_PATTERN = re.compile(r'[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]+\.pdf', re.IGNORECASE)


def _find_pdf_path(query: str) -> str | None:
    """Try to locate a valid, existing .pdf path inside the query string."""
    if not isinstance(query, str):
        return None

    candidate = query.strip()

    # Case 1: query is already a clean, existing path
    if candidate.lower().endswith(".pdf") and os.path.exists(candidate):
        return candidate

    # Case 2: query contains a path buried in other text (e.g. planner
    # rewrote/paraphrased it). Extract it with regex and verify it exists.
    match = PDF_PATH_PATTERN.search(query)
    if match:
        extracted = match.group(0)
        if os.path.exists(extracted):
            return extracted
        print(f"[DEBUG] Regex found a .pdf-looking path but it doesn't exist: {extracted!r}")

    return None


def resume_agent(state):
    query = state.get("query", "")
    print("QUERY:", repr(query))

    pdf_path = _find_pdf_path(query)
    print("RESOLVED PDF PATH:", pdf_path)

    if pdf_path:
        resume_content = extract_resume_text(pdf_path)
        print(f"RESUME CONTENT ({len(resume_content)} chars):", resume_content[:300])
    else:
        # No valid PDF path found — treat query as raw pasted resume text
        resume_content = query if isinstance(query, str) else ""

    # Guard: extraction failed or returned an error string
    if not resume_content or resume_content.strip().lower().startswith("error"):
        return {
            "response": (
                "I couldn't read any text from that resume. This usually means the PDF is "
                "a scanned image rather than selectable text — try exporting a text-based "
                "PDF, or paste your resume content directly as a message."
            ),
            "route": "resume_analysis",
        }

    prompt = f"""
    You are a senior AI interviewer. Analyze the resume text below and produce your response using EXACTLY these three headers:

    ## Strengths
    ## Weaknesses
    ## Interview Questions

    Base every point strictly on specific details from the resume (skills, projects, experience). Do not invent generic advice unrelated to this resume.

    Resume:
    {resume_content}
    """

    result = llm.invoke(prompt)

    return {
        "response": result.content,
        "route": "resume_analysis",
    }