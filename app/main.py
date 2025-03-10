from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from services.opeai_service import OpenAIService
from schema.openai.chat_models import ChatRequest, ChatResponse
from routes.tourism.tourism_router import router as tourism_router
from routes.openai.chat_route import router as openai_router
from routes.mt5.connection_route import router as mt5_connection_router
from routes.mt5.account_route import router as mt5_account_router
from routes.mt5.market_route import router as mt5_market_router
from routes.mt5.trade_route import router as mt5_trade_router
from routes.mt5.technical_route import router as mt5_technical_router

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
app.include_router(mt5_connection_router)  # เพิ่ม router สำหรับการเชื่อมต่อ MT5
app.include_router(mt5_account_router)  # เพิ่ม router สำหรับบัญชี MT5
app.include_router(mt5_market_router)  # เพิ่ม router สำหรับข้อมูลตลาด MT5
app.include_router(mt5_trade_router)  # เพิ่ม router สำหรับการเทรด MT5
app.include_router(mt5_technical_router)  # เพิ่ม router สำหรับการวิเคราะห์ทางเทคนิค MT5

# เพิ่มเส้นทางหน้าแรก
@app.get("/")
async def root():
    return {
        "message": "ยินดีต้อนรับสู่ API บริการ AI",
        "services": [
            {"name": "OpenAI Chat", "endpoint": "/api/v1/openai/chat"},
            {"name": "Tourism Planning", "endpoint": "/api/v1/tourism/travel-plan"},
            {"name": "MT5 Connection", "endpoint": "/api/mt5/connection"},
            {"name": "MT5 Account", "endpoint": "/api/mt5/account"},
            {"name": "MT5 Market", "endpoint": "/api/mt5/market"},
            {"name": "MT5 Trade", "endpoint": "/api/mt5/trade"},
            {"name": "MT5 Technical Analysis", "endpoint": "/api/mt5/technical"}
        ]
    }

# หากต้องการรันแอปพลิเคชันโดยตรงจากไฟล์นี้
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)