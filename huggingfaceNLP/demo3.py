import warnings
warnings.filterwarnings("ignore")
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding

def tokenize_function(examples):
    return tokenizer(examples["sentence1"], examples["sentence2"], truncation=True)

raw_datasets = load_dataset("glue","mrpc")
#print(raw_datasets)

raw_train_dataset = raw_datasets["train"]
#print(raw_train_dataset[1])
#print(raw_train_dataset.features)

model = 'bert-base-uncased' #bert-base-uncased
tokenizer = AutoTokenizer.from_pretrained(model)

tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
#print(tokenized_datasets)

data_collator = DataCollatorWithPadding(tokenizer)
print(tokenized_datasets["train"][1])