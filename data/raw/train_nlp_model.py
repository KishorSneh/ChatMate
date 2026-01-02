# train_nlp_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
data = pd.read_csv("train_data.csv")

# Encode labels
le = LabelEncoder()
data['label_encoded'] = le.fit_transform(data['label'])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    data['text'], data['label_encoded'], test_size=0.1, random_state=42
)

# Text vectorization
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

# Evaluate
y_pred = clf.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))

# Save model & vectorizer
joblib.dump(clf, "chatmate_nlp_model.pkl")
joblib.dump(vectorizer, "chatmate_vectorizer.pkl")
joblib.dump(le, "chatmate_label_encoder.pkl")

print("✅ NLP model, vectorizer & label encoder saved successfully!")
