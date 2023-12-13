
import time
import datetime
import torch

import pandas as pd
import numpy as np

from torch import optim
from collections import defaultdict
# from nltk.corpus import stopwords
from transformers import BertTokenizer
from transformers import Trainer, TrainingArguments, get_linear_schedule_with_warmup
from transformers import BertForSequenceClassification, AdamW, BertConfig, BertModel
# from scipy.special import softmax
from torch import Tensor

def load_model(dir: str):
    """
    Loads the model
    """
    model =  BertForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)
    model.load_state_dict(torch.load(dir, map_location=torch.device('cpu')))
    model.eval()

    return model

def predict(prompt):
    """
    predict performs inference on the model
    :param: ``prompt`` the input to send to the model"""

    model = load_model("pytorch_model.bin")
    tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()

    return {
        "predicted_class": predicted_class,
        "probabilitites": probabilities
    }
