#!/usr/bin/env python
# coding: utf-8

# In[1]:

import transformers
from transformers import pipeline
import tensorflow as tf
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# In[2]:

import os
current_directory_path = os.getcwd()

hateful_tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
hateful_model = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert")

emotion_model = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def getPrediction(txt):

    inputs = hateful_tokenizer([txt], return_tensors="pt", truncation=True, padding=True)
    output = hateful_model(**inputs)[0]
    scores = torch.sigmoid(output).cpu().detach().numpy()

    classes = ["toxic","severe_toxic","obscene","threat","insult","identity_hate"]

    result = dict()

    for c,s in zip(classes,scores[0]):
        result[c] = str(round(s*100,2))+"%"

    return result


def getEmotionPrediction(txt):

    model_outputs = emotion_model([txt])
    
    result = dict()

    for i in model_outputs[0]:
        result[i['label']] = str(round(float(i['score'])*100,2))+"%"

    return result
