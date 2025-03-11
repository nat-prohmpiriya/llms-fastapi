from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = "user"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = Field(default="gpt-3.5-turbo")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=500, ge=1, description="จำนวน token สูงสุดในการตอบกลับ ควรตั้งค่าอย่างน้อย 100 เพื่อให้ได้คำตอบที่สมบูรณ์")
    stream: Optional[bool] = Field(default=False)
    default_system_message: Optional[bool] = Field(default=True, description="เพิ่ม system message เริ่มต้นหรือไม่")

class ChatResponse(BaseModel):
    message: ChatMessage
    usage: Optional[Dict[str, int]] = None

class ChatStreamResponse(BaseModel):
    delta: str
    finish_reason: Optional[str] = None
    index: int = 0