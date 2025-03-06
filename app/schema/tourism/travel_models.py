from pydantic import BaseModel, Field
from typing import List, Optional

class TravelRequest(BaseModel):
    query: str = Field(..., description="คำถามหรือความต้องการเกี่ยวกับการท่องเที่ยว")
    destination: Optional[str] = Field(None, description="จุดหมายปลายทางที่สนใจ (ถ้ามี)")
    budget: Optional[float] = Field(None, description="งบประมาณโดยประมาณ (บาท)")
    duration: Optional[int] = Field(None, description="ระยะเวลาการเดินทาง (วัน)")
    interests: Optional[List[str]] = Field(None, description="ความสนใจเฉพาะด้าน เช่น อาหาร, ธรรมชาติ, วัฒนธรรม")

class Attraction(BaseModel):
    name: str
    description: str
    category: str
    estimated_time: str
    estimated_cost: float
    recommended_time_of_day: Optional[str] = None

class Activity(BaseModel):
    name: str
    description: str
    duration: str
    estimated_cost: float
    location: str

class DailyItinerary(BaseModel):
    day: int
    attractions: List[Attraction]
    activities: List[Activity]
    meals: List[str]
    transportation: List[str]
    daily_cost_estimate: float

class TravelPlan(BaseModel):
    destination: str
    duration: int
    overview: str
    daily_itinerary: List[DailyItinerary]
    total_cost_estimate: float
    tips: List[str]
    best_time_to_visit: str
    local_customs: Optional[List[str]] = None

class TravelResponse(BaseModel):
    travel_plan: TravelPlan
