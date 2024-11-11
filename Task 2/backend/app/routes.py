from fastapi import APIRouter, File, UploadFile
from app.services import recognize_audio, generate_answer, speak_answer
from app.models import find_existing_answer, store_conversation
from app.config import collection, OUTPUT_DIR
import os
import uuid

router = APIRouter()


@router.post("/predict")
async def predict(audio_file: UploadFile = File(...)):
    audio_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}_{
                              audio_file.filename}")
    with open(audio_path, "wb") as f:
        f.write(await audio_file.read())

    question = recognize_audio(audio_path)
    if not question:
        return {"error": "Could not recognize the question from the audio"}

    existing_answer, existing_audio_url = await find_existing_answer(collection, question)
    if existing_answer:
        return {"question": question, "answer": existing_answer, "audio_file_url": existing_audio_url}

    # Update with actual context text
    answer = generate_answer(question, "Context text here")
    audio_path = speak_answer(answer)
    audio_url = f"/static/outputs/{os.path.basename(audio_path)}"

    await store_conversation(collection, question, answer, audio_url)
    return {"question": question, "answer": answer, "audio_file_url": audio_url}
