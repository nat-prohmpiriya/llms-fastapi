import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from ..schema.openai.chat_models import ChatRequest, ChatResponse, ChatMessage

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def chat_completion(self, request: ChatRequest) -> ChatResponse:
        response = await self.client.chat.completions.create(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        
        return ChatResponse(
            message=response.choices[0].message.content,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )