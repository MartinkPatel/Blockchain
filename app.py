from fastapi import FastAPI, UploadFile, File, Form,HTTPException
from pydantic import BaseModel
from typing import Optional
import backend

app = FastAPI()

# Request/response models

class Message(BaseModel):
    walletid : str
    url: str
    dataset: str



class LLMResponse(BaseModel):
    response: str

@app.post("/submit", response_model=LLMResponse)
async def query_llm(request: Message):
    walletid = Message.walletid
    hugging_face_url = Message.url
    dataset_details = Message.dataset

    # Call your LLM here and get a response (pseudo-code)

    return {"response": f'''{walletid} {hugging_face_url} {dataset_details} '''}

@app.post("/voice_query", response_model=LLMResponse)
async def query_llm_with_audio(file: UploadFile = File(...)):
    # # Code to handle audio processing and then send to LLM
    # print(file)
    # audio_data = await file.read()  # Read audio data from file
    # llm_response = model.stt(audio_data)  # Pseudo function
    # return {"response": llm_response}

    if file.content_type != "audio/x-wav":
        raise HTTPException(status_code=400, detail="Invalid file type. Only WAV audio files are supported.")

    # Read audio data from file
    audio_data = await file.read()
    if not audio_data:
        raise HTTPException(status_code=400, detail="Uploaded audio file is empty.")

    # Call the pseudo STT model function to process audio
    return {"response": "gsdsds"}

# Replace `run_llm` and `process_audio_and_query_llm` with actual implementations