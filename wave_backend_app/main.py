from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='history.log', encoding='utf-8', level=logging.DEBUG)

tokenCounter = 0

class PromptRequest(BaseModel):
    prompt: str

@app.post("/run-prompt")
async def run_prompt(request: PromptRequest):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for students."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        completion_text = response.choices[0].message.content
        tokenCounter += len(completion_text)*.75 
        logger.info('Current token count: ' + tokenCounter)

        if tokenCounter >= 1000000:
            logger.warning("Token court surpassed 1m, double check Google Cloud console.")

        

        return {"response": completion_text}

    except Exception as e:
        logger.exception("An error occurred while processing the prompt." + e)
        return {"error": str(e)}