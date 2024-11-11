from fastapi import APIRouter
from app.services import recognize_audio,  speak_answer
from app.utils import load_and_preprocess_text, answer_question_from_text
from app.models import find_existing_answer, store_conversation
from app.config import collection, UPLOAD_DIR
import os
import uuid
from fastapi import Request
import json
import re
import base64

router = APIRouter()


def save_file(file: str) -> str:
    # Save the audio file to disk
    base64_data = re.sub(r'^data:.*;base64,', '', file)
    file_data = base64.b64decode(base64_data)

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}.m4a")
    with open(file_path, "wb") as f:
        f.write(file_data)
    return file_path


@router.post("/predict")
async def predict(request: Request):
    print("Received request")
    try:
        body = await request.body()
        data = json.loads(body)
        audio_data = data.get("audio_data")  # as datauri string
        if not audio_data:
            return {"error": "No audio data provided"}

        audio_path = save_file(audio_data)

        question = recognize_audio(audio_path)
        if not question:
            return {"error": "Could not recognize the question from the audio"}

        existing_answer, existing_audio_url = await find_existing_answer(collection, question)
        if existing_answer:
            print(f"Question: {question}")
            print(f"Answer: {existing_answer}")
            print(f"Audio URL: {existing_audio_url}")
            print("Conversation already stored in database")
            return {"question": question, "answer": existing_answer, "audio_file_url": existing_audio_url}

        # Update with actual context text
        answer = answer_question_from_text(question)
        audio_path = speak_answer(answer)
        audio_url = f"/static/outputs/{os.path.basename(audio_path)}"

        await store_conversation(collection, question, answer, audio_url)
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print(f"Audio URL: {audio_url}")
        print("Conversation stored in database")
        return {"question": question, "answer": answer, "audio_file_url": audio_url}

    except Exception as e:
        return {"error": str(e)}
