import pandas as pd
from datasets import Dataset

# Load your CSV
df = pd.read_csv("train_data.csv")

# Convert labels into numbers
label2id = {"math": 0, "gk": 1, "pdf": 2}
df["label"] = df["label"].map(label2id)

# Convert to HuggingFace dataset
dataset = Dataset.from_pandas(df)

# Split train/test
dataset = dataset.train_test_split(test_size=0.2)
