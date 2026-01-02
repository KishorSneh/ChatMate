import csv
import random

math_templates = [
    "Solve {}",
    "Find the derivative of {}",
    "Integrate {}",
    "Factor {}",
    "Simplify {}",
    "Expand {}",
    "What is the root of {}",
    "Calculate d/dx of {}"
]

math_expressions = [
    "x^2 + 3x",
    "sin(x)",
    "e^x",
    "x^3 - 8",
    "2x + 3",
    "x^2 - 16",
    "ln(x)",
    "x^4 + 2x^2",
    "cos(x)",
    "(x+1)^2 - x^2"
]

gk_templates = [
    "What is {}?",
    "Who is {}?",
    "Explain {}",
    "Define {}",
    "Where is {}?",
    "Name {}",
    "When did {} happen?",
    "How does {} work?"
]

gk_topics = [
    "the capital of India",
    "Newton's laws",
    "the president of USA",
    "photosynthesis",
    "the water cycle",
    "gravity",
    "electricity",
    "the currency of Japan",
    "the largest planet",
    "the smallest prime number",
    "the Great Wall of China",
    "the Mona Lisa",
    "democracy",
    "speed of light",
    "H2O"
]

pdf_templates = [
    "Summarize this PDF",
    "Extract text from the PDF",
    "Summarize the research paper",
    "Read this PDF document",
    "Analyze the PDF content",
    "Give a summary of PDF",
    "Summarize the uploaded research",
    "Provide a summary of PDF"
]

num_samples = 1000  # generate 1000 samples per label
rows = []

# Generate Math examples
for _ in range(num_samples):
    expr = random.choice(math_expressions)
    template = random.choice(math_templates)
    rows.append([template.format(expr), "math"])

# Generate GK examples
for _ in range(num_samples):
    topic = random.choice(gk_topics)
    template = random.choice(gk_templates)
    rows.append([template.format(topic), "gk"])

# Generate PDF examples
for _ in range(num_samples):
    template = random.choice(pdf_templates)
    rows.append([template, "pdf"])

# Shuffle rows for variety
random.shuffle(rows)

# Save to CSV
with open("train_data_large.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(rows)

print("Large synthetic dataset created: train_data_large.csv")
