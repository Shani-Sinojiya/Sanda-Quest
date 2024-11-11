from datetime import datetime

# Helper function to find an existing answer in MongoDB


async def find_existing_answer(collection, question: str):
    existing_record = await collection.find_one({"question": question})
    if existing_record:
        return existing_record.get("answer"), existing_record.get("audio_file_url")
    return None, None

# Helper function to store the conversation in MongoDB


async def store_conversation(collection, question: str, answer: str, audio_file_url: str):
    conversation_data = {
        "question": question,
        "answer": answer,
        "audio_file_url": audio_file_url,
        "timestamp": datetime.utcnow()
    }
    await collection.insert_one(conversation_data)
