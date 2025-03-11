from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from schema.openai.chat_models import ChatRequest, ChatResponse, ChatMessage
from services.opeai_service import OpenAIService
import json

router = APIRouter(
    prefix="/api/v1/openai",
    tags=["OpenAI"]
)


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest, openai_service: OpenAIService = Depends(OpenAIService)):
    try:
        # ถ้าต้องการ stream ให้ใช้ endpoint /chat/stream แทน
        if request.stream:
            raise HTTPException(status_code=400, detail="For streaming responses, use the /chat/stream endpoint")
        
        return await openai_service.chat_completion(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_completion_stream(request: ChatRequest, openai_service: OpenAIService = Depends(OpenAIService)):
    """
    Stream chat completion responses using POST
    """
    try:
        # กำหนดให้ใช้ stream เสมอสำหรับ endpoint นี้
        request.stream = True
        
        async def generate():
            async for chunk in openai_service.chat_completion_stream(request):
                # ส่งข้อมูลในรูปแบบ Server-Sent Events (SSE)
                if chunk.delta:  # ตรวจสอบว่ามี delta หรือไม่
                    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
            
            # ส่งสัญญาณว่าสิ้นสุดการ stream
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # สำหรับ Nginx
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/stream")
async def chat_completion_stream_get(
    messages: str = Query(..., description="JSON string of messages array"),
    model: str = Query("gpt-3.5-turbo", description="Model to use"),
    openai_service: OpenAIService = Depends(OpenAIService)
):
    """
    Stream chat completion responses using GET (for EventSource)
    """
    try:
        # แปลง messages string เป็น list ของ ChatMessage
        messages_data = json.loads(messages)
        chat_messages = [ChatMessage(**msg) for msg in messages_data]
        
        # สร้าง request object
        request = ChatRequest(
            messages=chat_messages,
            model=model,
            stream=True
        )
        
        async def generate():
            async for chunk in openai_service.chat_completion_stream(request):
                # ส่งข้อมูลในรูปแบบ Server-Sent Events (SSE)
                if chunk.delta:  # ตรวจสอบว่ามี delta หรือไม่
                    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
            
            # ส่งสัญญาณว่าสิ้นสุดการ stream
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # สำหรับ Nginx
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))