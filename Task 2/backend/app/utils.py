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


def load_and_preprocess_text(file_path: str):
    """Load text from a file and preprocess it."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def tokenize_text(text, max_length=1024):
    """Tokenize text and ensure it's within the max_length limit."""
    tokens = tokenizer.encode(
        text, return_tensors='pt', truncation=True, max_length=max_length)
    return tokens


def split_into_chunks(document, max_chunk_size=1024):
    """Split the document into smaller chunks for processing."""
    chunks = []
    current_chunk = []
    current_length = 0

    sentences = document.split('.')
    for sentence in sentences:
        sentence_tokens = tokenize_text(sentence)
        sentence_length = sentence_tokens.size(1)

        if current_length + sentence_length > max_chunk_size:
            # If adding the sentence exceeds the max chunk size, store the current chunk and reset
            chunks.append(current_chunk)
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            # Otherwise, add the sentence to the current chunk
            current_chunk.append(sentence)
            current_length += sentence_length

    # Add the last chunk if there's any remaining
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def retrieve_relevant_section(question, chunk_text):
    """Retrieve the most relevant part of the chunk for the question (using GPT-2 or other methods)."""
    return chunk_text


def get_embeddings(tokens):
    """Get the embeddings of the tokenized text."""
    with torch.no_grad():
        outputs = model.transformer(tokens.to(device))
        last_hidden_states = outputs.last_hidden_state
    return torch.mean(last_hidden_states, dim=1).cpu().numpy()


def generate_answer(question: str, relevant_section):
    """Generate a focused answer from GPT-2 based on the relevant section."""
    input_text = f"Context: {
        relevant_section}\nBased on the context, provide a focused and relevant answer.\nQuestion: {question}\nAnswer:"

    inputs = tokenizer.encode(input_text, return_tensors='pt').to(device)

    # Generate the answer with more controlled settings to stay on topic
    outputs = model.generate(inputs, max_length=200, num_return_sequences=1,
                             no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.6, do_sample=False)

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer


def answer_question_from_text(question: str):
    """Main function to load the document, split into chunks, and generate an answer."""
    document = load_and_preprocess_text("./preprocessed_data.txt")
    print(f"Loaded document with {len(document)} characters.")
    # Split the document into chunks to handle long text
    document_chunks = split_into_chunks(document)

    best_section = None
    best_similarity = -1

    for chunk in document_chunks:
        chunk_text = ' '.join(chunk)

        # Retrieve the most relevant section (you can improve this with better similarity methods)
        relevant_section = retrieve_relevant_section(question, chunk_text)

        # Get embeddings for the chunk and the question
        chunk_tokens = tokenize_text(chunk_text)
        chunk_embedding = get_embeddings(chunk_tokens)

        query_tokens = tokenize_text(question)
        query_embedding = get_embeddings(query_tokens)

        # Calculate cosine similarity between the question and the chunk
        similarity = np.dot(query_embedding, chunk_embedding.T) / \
            (np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding))

        if similarity > best_similarity:
            best_similarity = similarity
            best_section = relevant_section

    # Generate the answer based on the best section of the document
    answer = generate_answer(question, best_section)
    return answer


def speak_answer(answer: str):
    """Convert the answer text to speech using gTTS and save it to output folder."""
    match = re.search(r'Answer:(.*)', answer,
                      re.DOTALL)  # re.DOTALL allows for multiline answers
    if match:
        # Remove any extra spaces before/after the answer
        final_answer = match.group(1).strip()
        # Convert the final answer to speech
        tts = gTTS(text=final_answer, lang='en')

        # Save the speech to the OUTPUT_DIR
        output_file_path = os.path.join(
            OUTPUT_DIR, f"{uuid.uuid4().hex}_answer.mp3")
        tts.save(output_file_path)  # Save the audio as an mp3 file
        return output_file_path
    else:
        print("No valid answer found after 'Answer:'")
        return None
