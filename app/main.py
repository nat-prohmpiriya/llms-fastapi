from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from services.opeai_service import OpenAIService
from schema.openai.chat_models import ChatRequest, ChatResponse
from routes.tourism.tourism_router import router as tourism_router
from routes.openai.chat_route import router as openai_router

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI(
    title="AI API Services",
    description="API สำหรับบริการ AI ต่างๆ รวมถึงแชทกับ OpenAI และวางแผนการท่องเที่ยว",
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


app.include_router(openai_router)
app.include_router(tourism_router)  # เพิ่ม router สำหรับระบบท่องเที่ยว

# เพิ่มเส้นทางหน้าแรก
@app.get("/")
async def root():
    return {
        "message": "ยินดีต้อนรับสู่ API บริการ AI",
        "services": [
            {"name": "OpenAI Chat", "endpoint": "/api/v1/openai/chat"},
            {"name": "Tourism Planning", "endpoint": "/api/v1/tourism/travel-plan"}
        ]
    }

# หากต้องการรันแอปพลิเคชันโดยตรงจากไฟล์นี้
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)