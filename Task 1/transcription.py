import zipfile
import datetime
import math
import json
import os
import torch
from pymongo import MongoClient
from pydub.utils import make_chunks
from pydub import AudioSegment
from sentence_transformers import SentenceTransformer
from transformers import MT5ForConditionalGeneration, MT5Tokenizer, T5ForConditionalGeneration, T5Tokenizer
import whisper
from google.colab import drive
drive.mount('/content/drive')

device = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = whisper.load_model("large").to(device)


def get_mongo_client(uri):
    try:
        client = MongoClient(uri)
        print("Connected to MongoDB successfully.")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


mongodb_uri = "mongodb+srv://python:1234567890@cluster.kvnyt.mongodb.net"
client = get_mongo_client(mongodb_uri)

db = client['sandalquest']
collection = db['transcriptions']


def save_to_mongodb(metadata):
    try:
        collection.insert_one(metadata)
        print(f"Saved merged transcription for {
              metadata['filename']} to MongoDB.")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")


def is_file_processed(filename):
    try:
        return collection.find_one({"filename": filename}) is not None
    except Exception as e:
        print(f"Error checking file in MongoDB: {e}")
        return False


def split_audio_by_size(file_path, max_size_mb=20):
    try:
        audio = AudioSegment.from_file(file_path)
        file_size_bytes = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024

        num_chunks = math.ceil(file_size_bytes / max_size_bytes)
        chunk_length_ms = len(audio) // num_chunks

        chunks = make_chunks(audio, chunk_length_ms)
        print(f"Split audio into {len(chunks)} chunks based on size.")
        return chunks

    except Exception as e:
        print(f"Error splitting audio by size: {e}")
        return []


def transcribe_audio_kannada(audio_path):
    try:
        print("Transcribing in progress...")
        transcription = whisper_model.transcribe(
            audio_path, language="kn")['text']
        return transcription
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""


def process_audio_files(directory_path):
    file_list = os.listdir(directory_path)
    process_index = 1

    for filename in file_list:
        file_path = os.path.join(directory_path, filename)

        if not filename.endswith(".mp3"):
            continue

        if is_file_processed(filename):
            print(f"File {filename} already processed. Skipping.")
            continue

        try:
            print(f"Processing file {process_index}: {filename}")
            chunks = split_audio_by_size(file_path, max_size_mb=20)
            merged_transcription = ""

            for i, chunk in enumerate(chunks):
                print(f"Transcribing chunk {
                      i + 1}/{len(chunks)} of file {filename}...")
                chunk.export("temp_chunk.wav", format="wav")
                kannada_text = transcribe_audio_kannada("temp_chunk.wav")
                merged_transcription += kannada_text + " "

            metadata = {
                'file_index': process_index,
                'filename': filename,
                'merged_transcription': merged_transcription.strip(),
                'timestamp': datetime.datetime.utcnow(),
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'audio_format': filename.split(".")[-1],
                'duration_ms': len(AudioSegment.from_file(file_path))
            }

            save_to_mongodb(metadata)
            print(f"Finished processing file {process_index}: {filename}")
            process_index += 1

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            continue

    print("All files processed or skipped successfully.")


zip_path = "/content/drive/MyDrive/SandalWoonDatasets.zip"
extracted_path = "/content/drive/MyDrive/SandalWood"
os.makedirs(extracted_path, exist_ok=True)


def list_files_in_directory(directory_path):
    extracted_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            extracted_files.append(os.path.relpath(
                os.path.join(root, file), directory_path))
    return extracted_files


with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_files = zip_ref.namelist()
    extracted_files = list_files_in_directory(extracted_path)
    missing_files = [file for file in zip_files if file not in extracted_files]

    if missing_files:
        print(f"Missing {len(missing_files)
                         } files. Re-extracting missing files...")
        for file in missing_files:
            try:
                zip_ref.extract(file, extracted_path)
                print(f"Re-extracted file: {file}")
            except Exception as e:
                print(f"Error extracting file {file}: {e}")
    else:
        print("All files are already extracted.")

print("Dataset extraction and verification completed.")
print("Final list of extracted files:")
for file in list_files_in_directory(extracted_path):
    print(file)

total_files_in_zip = len(zip_files)
total_extracted_files = len(list_files_in_directory(extracted_path))

if total_files_in_zip == total_extracted_files:
    print(f"All {total_files_in_zip} files are extracted successfully.")
else:
    print(f"Extraction completed with {
          total_extracted_files}/{total_files_in_zip} files available.")

process_audio_files(extracted_path)
