# !pip install transformers
# !pip install torch torchvision torchaudio
# !pip install requests beautifulsoup4 pandas numpy

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re

class SentimentAnalysis():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    def analyze(self, s):
        tokens = self.tokenizer.encode(s, return_tensors = 'pt')
        result = self.model(tokens)
        return int(torch.argmax(result.logits)) + 1


model = SentimentAnalysis()

def analyse(text):
    return model.analyze(text)
# print(test.analyze("hello I'm tired"))
