from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/run-prompt")
async def run_prompt(request: PromptRequest):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for students."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        completion_text = response.choices[0].message.content

        return {"response": completion_text}

    except Exception as e:
        return {"error": str(e)}
