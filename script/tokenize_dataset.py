from transformers import DistilBertTokenizerFast
from datasets import load_dataset

# Load dataset from CSV file (make sure 'text' column exists)
dataset = load_dataset("csv", data_files={"train": "train_data.csv"})

# Initialize tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

# Define tokenize function
def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

# Apply tokenizer
tokenized_dataset = dataset["train"].map(tokenize, batched=True)

# Save processed dataset
tokenized_dataset.save_to_disk("tokenized_data")
