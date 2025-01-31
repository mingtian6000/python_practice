#basic usage of huggingface
import warnings
from transformers import pipeline

#classifier = pipeline('sentiment-analysis')
#whats the default model?RobertaModel
#print(classifier.model)
# print(classifier('We are very happy to show you the 🤗 Transformers library.'))
# print(classifier('We are very sad to show you the 🤗 Transformers library.'))


classifier = pipeline("fill-mask")
#print(classifier.model) #RobertaModel
print(classifier("Paris is the <mask> of France."))