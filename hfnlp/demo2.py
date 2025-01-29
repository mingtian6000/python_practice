from transformers import AutoModelForSequenceClassification, AutoTokenizer

#序列分类
model = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model)
print(model)

raw_inputs = [
    "I've been waiting for a HuggingFace course my whole life.",
    "I hate this so much!"
]

#padding: pad_to_max_length=True, padding='longest', truncation=True
#return_tensors: 'pt' for pytorch tensors, 'tf' for tensorflow tensors, 'np' for numpy arrays
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs)

print(tokenizer.decode(inputs['input_ids'][0]))
print(tokenizer.decode(inputs['input_ids'][1]))

outputs = model(**inputs)
print(outputs)
print(outputs.logits.shape)

print(outputs.logits)

import torch
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions)

print(model.config.id2label)
