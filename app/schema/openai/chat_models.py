from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = "user"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = Field(default="gpt-3.5-turbo")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    stream: Optional[bool] = Field(default=False)

class ChatResponse(BaseModel):
    message: str
    usage: Optional[dict] = None