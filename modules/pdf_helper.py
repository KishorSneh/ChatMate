# File: modules/pdf_helper.py

from typing import Dict
import re
import PyPDF2

def clean_pdf_text(text: str) -> str:
    """
    Clean the PDF output text.
    """
    text = str(text).replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 1000:
        text = text[:1000].rstrip() + "..."
    return text

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + " "
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return clean_pdf_text(text)

def summarize_text(text: str) -> str:
    """
    Simple dummy summarization (can be replaced with real NLP model later)
    """
    sentences = text.split('.')
    summary = '. '.join(sentences[:min(3, len(sentences))]).strip()
    if not summary.endswith('.'):
        summary += '.'
    return summary

def handle_pdf_query(user_message: str, file_path: str = None) -> Dict:
    """
    Handle PDF-related queries.
    """
    user_message = (user_message or "").strip()
    if not user_message:
        return {"handled": True, "reply": "Please specify your PDF query."}

    lower_msg = user_message.lower()
    if file_path is None:
        reply = "Please upload a PDF file to process."
        return {"handled": True, "reply": reply}

    pdf_text = extract_text_from_pdf(file_path)

    if any(keyword in lower_msg for keyword in ["summarize", "summary", "research paper"]):
        reply = summarize_text(pdf_text)
    elif any(keyword in lower_msg for keyword in ["extract", "text", "read"]):
        reply = pdf_text
    elif any(keyword in lower_msg for keyword in ["analyze"]):
        reply = f"Analysis: The PDF contains {len(pdf_text.split())} words and covers key concepts. (Simulated)"
    else:
        reply = "I can help summarize, extract text, or analyze PDFs. Please rephrase your request."

    reply = clean_pdf_text(reply)
    return {"handled": True, "reply": reply}

# Test standalone
if __name__ == "__main__":
    print("PDF Helper Module with real PDF support\nType 'exit' to quit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ("exit","quit"): break
        pdf_path = input("PDF file path: ").strip()
        print("ChatMate:", handle_pdf_query(user, pdf_path)["reply"])
