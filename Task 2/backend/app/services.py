import os
import numpy as np
import torch
import speech_recognition as sr
from app.utils import tokenize_text, generate_answer, speak_answer
from app.config import OUTPUT_DIR


def recognize_audio(file_path: str):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except (sr.UnknownValueError, sr.RequestError):
        return None


def get_embeddings(tokens, model, device):
    with torch.no_grad():
        outputs = model.transformer(tokens.to(device))
        return torch.mean(outputs.last_hidden_state, dim=1).cpu().numpy()


def calculate_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
