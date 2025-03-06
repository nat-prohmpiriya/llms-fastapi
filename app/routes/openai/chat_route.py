from fastapi import APIRouter, Depends, HTTPException
from schema.openai.chat_models import ChatRequest, ChatResponse
from services.opeai_service import OpenAIService

router = APIRouter(
    prefix="/api/v1/openai",
    tags=["OpenAI"]
)


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest, openai_service: OpenAIService = Depends(OpenAIService)):
    try:
        return await openai_service.chat_completion(request)
    except Exception as e:
        raise e