import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from schema.openai.chat_models import ChatRequest, ChatResponse, ChatMessage, ChatStreamResponse
from schema.openai.embeddings_models import EmbeddingsRequest, EmbeddingsResponse, EmbeddingData, EmbeddingsUsage
from typing import List, AsyncGenerator

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def chat_completion(self, request: ChatRequest) -> ChatResponse:
        # เพิ่ม system message เริ่มต้นหากต้องการ
        messages = list(request.messages)
        
        # ตรวจสอบว่ามี system message อยู่แล้วหรือไม่
        has_system_message = any(msg.role == "system" for msg in messages)
        
        # เพิ่ม system message เริ่มต้นหากยังไม่มีและ default_system_message เป็น True
        if not has_system_message and request.default_system_message:
            messages.insert(0, ChatMessage(
                role="system",
                content="คุณเป็นผู้ช่วยที่เป็นประโยชน์และตอบคำถามเป็นภาษาไทยเสมอ ให้คำตอบที่ครบถ้วนและมีประโยชน์"
            ))
        
        response = await self.client.chat.completions.create(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False  # ไม่ใช้ stream ในฟังก์ชันนี้
        )
        
        # สร้าง ChatMessage จากการตอบกลับของ OpenAI
        assistant_message = ChatMessage(
            role="assistant",
            content=response.choices[0].message.content
        )
        
        return ChatResponse(
            message=assistant_message,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
    
    async def chat_completion_stream(self, request: ChatRequest) -> AsyncGenerator[ChatStreamResponse, None]:
        """
        สร้างการตอบกลับแบบ stream จาก OpenAI API
        
        Args:
            request: ข้อมูลคำขอ chat completion
            
        Yields:
            ChatStreamResponse: ข้อมูลตอบกลับแบบ stream
        """
        # ตรวจสอบและปรับแต่ง messages
        messages = request.messages.copy()
        has_system_message = any(msg.role == "system" for msg in messages)
        
        # เพิ่ม system message เริ่มต้นหากยังไม่มีและ default_system_message เป็น True
        if not has_system_message and request.default_system_message:
            messages.insert(0, ChatMessage(
                role="system",
                content="คุณเป็นผู้ช่วยที่เป็นประโยชน์และตอบคำถามเป็นภาษาไทยเสมอ ให้คำตอบที่ครบถ้วนและมีประโยชน์"
            ))
        
        # เรียกใช้ API แบบ stream
        stream = await self.client.chat.completions.create(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        )
        
        # สำหรับจัดการข้อความภาษาไทย
        buffer = ""
        buffer_size_limit = 10  # กำหนดขนาดบัฟเฟอร์สูงสุด
        
        # ส่งข้อมูลแบบ stream
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                buffer += content
                
                # เงื่อนไขในการส่งข้อมูล:
                # 1. ถ้าบัฟเฟอร์มีขนาดเกินกำหนด
                # 2. ถ้าในข้อความมีเครื่องหมายวรรคตอน
                # 3. ถ้ามีช่องว่าง (เว้นวรรค)
                should_send = (
                    len(buffer) >= buffer_size_limit or 
                    any(p in buffer for p in [".", ",", "!", "?", "\n"]) or
                    " " in buffer
                )
                
                if should_send:
                    yield ChatStreamResponse(
                        delta=buffer,
                        finish_reason=chunk.choices[0].finish_reason,
                        index=chunk.choices[0].index
                    )
                    buffer = ""  # ล้างบัฟเฟอร์
        
        # ส่งข้อมูลที่เหลือในบัฟเฟอร์ (ถ้ามี)
        if buffer:
            yield ChatStreamResponse(
                delta=buffer,
                finish_reason=None,
                index=0
            )
    
    async def create_embeddings(self, request: EmbeddingsRequest) -> EmbeddingsResponse:
        """
        สร้าง embeddings จากข้อความที่ได้รับ
        
        Args:
            request: ข้อมูลคำขอ embeddings
            
        Returns:
            EmbeddingsResponse: ข้อมูลตอบกลับที่มี embeddings
        """
        # สร้างพารามิเตอร์สำหรับการเรียก API
        params = {
            "model": request.model,
            "input": request.input,
            "encoding_format": request.encoding_format
        }
        
        # เพิ่ม dimensions ถ้ามีการระบุ
        if request.dimensions:
            params["dimensions"] = request.dimensions
            
        # เรียกใช้ API
        response = await self.client.embeddings.create(**params)
        
        # สร้างข้อมูลตอบกลับ
        embedding_data = [
            EmbeddingData(
                embedding=item.embedding,
                index=item.index,
                object=item.object
            ) for item in response.data
        ]
        
        return EmbeddingsResponse(
            data=embedding_data,
            model=response.model,
            object=response.object,
            usage=EmbeddingsUsage(
                prompt_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens
            )
        )