import re
from typing import Dict

# Optional Hugging Face LLM
try:
    from transformers import pipeline
    _LLM_PIPELINE_AVAILABLE = True
except Exception:
    _LLM_PIPELINE_AVAILABLE = False

_llm = None
def _get_llm():
    global _llm
    if _llm is None and _LLM_PIPELINE_AVAILABLE:
        try:
            # Smaller local model suitable for CPU
            _llm = pipeline("text2text-generation", model="google/flan-t5-small")
        except Exception:
            _llm = None
    return _llm

def clean_llm_output(text: str) -> str:
    text = str(text).replace('\n',' ').strip()
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 1000: text = text[:1000].rstrip() + "..."
    return text

# ===== Simple FAQ fallback =====
_FAQ = {
    "what is the capital of india": "The capital of India is New Delhi.",
    "who is the president of usa": "As of 2025, the President of the USA is Joe Biden.",
    "who discovered gravity": "Sir Isaac Newton is credited with discovering the laws of gravity.",
    "what is the boiling point of water": "The boiling point of water is 100°C (212°F) at standard atmospheric pressure.",
    "who wrote hamlet": "William Shakespeare wrote the play 'Hamlet'."
}

def _faq_fallback(question: str) -> str:
    q = question.lower()
    for key, answer in _FAQ.items():
        if key in q:
            return answer
    return None

def handle_gk_query(user_message: str) -> Dict:
    user_message = (user_message or "").strip()
    if not user_message:
        return {"handled": True, "reply": "Please enter a question."}

    # Try LLM if available
    llm = _get_llm()
    if llm:
        try:
            prompt = f"You are a helpful student tutor. Explain clearly to a high school student:\n\nQuestion: {user_message}\n\nAnswer:"
            response = llm(prompt, max_length=256, do_sample=False)[0].get("generated_text", "")
            reply = clean_llm_output(response)
            return {"handled": True, "reply": reply}
        except Exception as e:
            reply = f"Error generating explanation: {e}"
            return {"handled": True, "reply": reply}

    # If LLM not available, fallback to FAQ
    faq_answer = _faq_fallback(user_message)
    if faq_answer:
        return {"handled": True, "reply": faq_answer}

    # Default fallback
    return {"handled": True, "reply": "Sorry, I cannot answer that question right now."}

# ===== Standalone Test =====
if __name__ == "__main__":
    print("GK Helper Module (LLM + FAQ fallback)\nType 'exit' to quit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ("exit","quit"): break
        print("ChatMate:", handle_gk_query(user)["reply"])
