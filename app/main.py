from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from services.opeai_service import OpenAIService
from schema.openai.chat_models import ChatRequest, ChatResponse

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI(
    title="Chat with OpenAI API",
    description="API สำหรับแชทกับ OpenAI",
    version="1.0.0"
)

# กำหนดค่า CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ในการใช้งานจริง ควรระบุโดเมนที่อนุญาตเท่านั้น
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# สร้างฟังก์ชันสำหรับเรียกใช้ OpenAIService
def get_openai_service():
    return OpenAIService()

# สร้าง APIRouter สำหรับ OpenAI
openai_router = APIRouter(
    prefix="/api/v1/openai",
    tags=["OpenAI"]
)

# สร้างเส้นทาง API สำหรับการแชท
@openai_router.post("/chat", response_model=ChatResponse)
async def chat_with_openai(
    request: ChatRequest,
    openai_service: OpenAIService = Depends(get_openai_service)
):
    """
    ส่งข้อความไปยัง OpenAI และรับการตอบกลับ
    """
    return await openai_service.chat_completion(request)

# เพิ่ม router เข้าไปในแอปพลิเคชัน
app.include_router(openai_router)

# เพิ่มเส้นทางหน้าแรก
@app.get("/")
async def root():
    return {"message": "ยินดีต้อนรับสู่ API แชทกับ OpenAI"}

# หากต้องการรันแอปพลิเคชันโดยตรงจากไฟล์นี้
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)