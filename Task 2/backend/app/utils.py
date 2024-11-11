import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from gtts import gTTS
import re
import uuid
import os
import numpy as np
from app.config import OUTPUT_DIR

# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def tokenize_text(text, max_length=1024):
    tokens = tokenizer.encode(
        text, return_tensors='pt', truncation=True, max_length=max_length)
    return tokens


def generate_answer(question: str, relevant_section: str):
    input_text = f"Context: {relevant_section}\nQuestion: {question}\nAnswer:"
    inputs = tokenizer.encode(input_text, return_tensors='pt').to(device)
    outputs = model.generate(
        inputs, max_length=200, num_return_sequences=1, top_k=50, top_p=0.95, temperature=0.6)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


def speak_answer(answer: str):
    match = re.search(r'Answer:(.*)', answer, re.DOTALL)
    if match:
        final_answer = match.group(1).strip()
        tts = gTTS(text=final_answer, lang='en')
        output_path = os.path.join(
            OUTPUT_DIR, f"{uuid.uuid4().hex}_answer.mp3")
        tts.save(output_path)
        return output_path
    return None
