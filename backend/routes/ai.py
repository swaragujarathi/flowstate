import json
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai
from pydantic import ValidationError
from schemas.ai import AIRequest, AIParseResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        f"GEMINI_API_KEY not found.\nLoaded from: {dotenv_path}"
    )

client = genai.Client(api_key=api_key)


PROMPT = """
You are an AI task parser for a study planner.

Convert the user's study plan into JSON.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT write explanations.
Do NOT wrap the response inside ```.

Return this exact structure:

{
    "tasks": [
        {
            "title": "...",
            "estimated_hours": 0,
            "priority": "High",
            "difficulty": "Medium",
            "deadline": "YYYY-MM-DD"
        }
    ]
}

Rules:

1. Priority must be one of:
High
Medium
Low

2. Difficulty must be one of:
Easy
Medium
Hard

3. If no deadline exists, return null.

4. If one deadline applies to multiple tasks, copy it.

5. If estimated hours are missing, estimate them.

6. Infer priority and difficulty if omitted.

7. Return ONLY JSON.
"""


@router.post(
    "/parse",
    response_model=AIParseResponse
)
async def parse_tasks(request: AIRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Input cannot be empty."
        )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{PROMPT}\n\nStudy Plan:\n{request.text}"
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

        data = json.loads(text)

        validated = AIParseResponse.model_validate(data)

        return validated

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Gemini returned invalid JSON."
        )

    except ValidationError as e:

        raise HTTPException(
            status_code=400,
            detail=e.errors()
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )