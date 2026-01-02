# File: modules/nlp_manager.py

import joblib
import os

class NLPManager:
    """
    NLPManager for ChatMate using a trained offline classifier.
    Handles multi-label classification: math, gk, pdf.
    """

    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "../chatmate_nlp_model.pkl")
        vectorizer_path = os.path.join(os.path.dirname(__file__), "../chatmate_vectorizer.pkl")
        label_encoder_path = os.path.join(os.path.dirname(__file__), "../chatmate_label_encoder.pkl")
        
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.label_encoder = joblib.load(label_encoder_path)
            print("[INFO] NLPManager loaded trained model successfully!")
        except Exception as e:
            print(f"[WARNING] Failed to load NLP model: {e}")
            self.model = None
            self.vectorizer = None
            self.label_encoder = None

    def predict(self, text):
        """
        Predict label and confidence for a given user message.
        Returns (label_name, confidence)
        """
        if self.model is None or self.vectorizer is None or self.label_encoder is None:
            return None, 0.0

        X_vec = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X_vec)[0]
        idx = probs.argmax()
        label_name = self.label_encoder.inverse_transform([idx])[0]
        confidence = float(probs[idx])
        return label_name, confidence

    def get_response(self, predicted_label):
        """
        Map predicted label to ChatMate's module handling
        """
        if predicted_label == "math":
            return "This looks like a math question. Let me solve it."
        elif predicted_label == "gk":
            return "This seems like a general knowledge question. Here's what I know."
        elif predicted_label == "pdf":
            return "This relates to a PDF document. I can help summarize it."
        else:
            return "I am not sure how to respond to that."

    def get_dataset(self):
        """
        Optionally return the dataset info (not required for inference)
        """
        return None

# Test standalone
if __name__ == "__main__":
    nlp = NLPManager()
    while True:
        user = input("You: ").strip()
        if user.lower() in ("exit", "quit"):
            break
        label, conf = nlp.predict(user)
        resp = nlp.get_response(label) if label else "Model not loaded."
        print(f"ChatMate: {resp} (Label: {label}, Confidence: {conf:.2f})")
