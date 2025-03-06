from fastapi import APIRouter, Depends
from schema.tourism.travel_models import TravelRequest, TravelResponse
from services.tourism_service import TourismService

router = APIRouter(
    prefix="/api/v1/tourism",
    tags=["tourism"],
)

@router.post("/travel-plan", response_model=TravelResponse)
async def generate_travel_plan(request: TravelRequest, service: TourismService = Depends()):
    """
    สร้างแผนการท่องเที่ยวตามความต้องการของผู้ใช้
    
    - **query**: คำถามหรือความต้องการเกี่ยวกับการท่องเที่ยว
    - **destination**: จุดหมายปลายทางที่สนใจ (ถ้ามี)
    - **budget**: งบประมาณโดยประมาณ (บาท)
    - **duration**: ระยะเวลาการเดินทาง (วัน)
    - **interests**: ความสนใจเฉพาะด้าน เช่น อาหาร, ธรรมชาติ, วัฒนธรรม
    
    ตัวอย่างคำขอ:
    ```json
    {
      "query": "อยากไปเที่ยวเชียงใหม่ช่วงปลายปี",
      "destination": "เชียงใหม่",
      "budget": 10000,
      "duration": 3,
      "interests": ["อาหาร", "ธรรมชาติ", "วัฒนธรรม"]
    }
    ```
    """
    return await service.generate_travel_plan(request)
