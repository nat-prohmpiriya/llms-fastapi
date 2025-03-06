import os
from openai import OpenAI
from schema.tourism.travel_models import TravelRequest, TravelResponse, TravelPlan
import json
from typing import Dict, Any

class TourismService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def generate_travel_plan(self, request: TravelRequest) -> TravelResponse:
        # สร้าง system message ที่กำหนดรูปแบบการตอบกลับเป็น JSON
        system_message = """
        คุณเป็นผู้เชี่ยวชาญด้านการท่องเที่ยวที่มีความรู้เกี่ยวกับสถานที่ท่องเที่ยวทั่วโลก
        โปรดวิเคราะห์คำขอของผู้ใช้และสร้างแผนการเดินทางที่เหมาะสม
        คำตอบของคุณต้องเป็น JSON ที่มีโครงสร้างตาม TravelPlan schema เท่านั้น
        ไม่ต้องใส่คำอธิบายหรือข้อความอื่นๆ นอกเหนือจาก JSON
        ราคาและค่าใช้จ่ายทั้งหมดให้แสดงเป็นสกุลเงินบาทไทย
        
        โครงสร้าง JSON ที่ต้องการ:
        {
          "destination": "ชื่อจุดหมายปลายทาง",
          "duration": จำนวนวัน,
          "overview": "ภาพรวมของแผนการเดินทาง",
          "daily_itinerary": [
            {
              "day": ลำดับวัน,
              "attractions": [
                {
                  "name": "ชื่อสถานที่",
                  "description": "คำอธิบาย",
                  "category": "ประเภท (ธรรมชาติ, วัฒนธรรม, ฯลฯ)",
                  "estimated_time": "เวลาที่ใช้โดยประมาณ",
                  "estimated_cost": ค่าใช้จ่ายโดยประมาณ,
                  "recommended_time_of_day": "ช่วงเวลาที่แนะนำ"
                }
              ],
              "activities": [
                {
                  "name": "ชื่อกิจกรรม",
                  "description": "คำอธิบาย",
                  "duration": "ระยะเวลา",
                  "estimated_cost": ค่าใช้จ่ายโดยประมาณ,
                  "location": "สถานที่"
                }
              ],
              "meals": ["มื้อเช้า: ...", "มื้อกลางวัน: ...", "มื้อเย็น: ..."],
              "transportation": ["วิธีการเดินทาง 1", "วิธีการเดินทาง 2"],
              "daily_cost_estimate": ค่าใช้จ่ายรวมต่อวัน
            }
          ],
          "total_cost_estimate": ค่าใช้จ่ายรวมทั้งหมด,
          "tips": ["คำแนะนำ 1", "คำแนะนำ 2"],
          "best_time_to_visit": "ช่วงเวลาที่ดีที่สุดในการเยี่ยมชม",
          "local_customs": ["ธรรมเนียมท้องถิ่น 1", "ธรรมเนียมท้องถิ่น 2"]
        }
        """
        
        # สร้าง prompt ที่รวมข้อมูลจาก request
        user_prompt = f"ฉันต้องการแผนการท่องเที่ยวสำหรับ: {request.query}"
        
        if request.destination:
            user_prompt += f"\nจุดหมายปลายทาง: {request.destination}"
        if request.budget:
            user_prompt += f"\nงบประมาณ: {request.budget} บาท"
        if request.duration:
            user_prompt += f"\nระยะเวลา: {request.duration} วัน"
        if request.interests:
            user_prompt += f"\nความสนใจ: {', '.join(request.interests)}"
            
        # เรียกใช้ OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # หรือใช้ gpt-4 ถ้ามี
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # แปลงข้อความตอบกลับเป็น JSON
        result_json = json.loads(response.choices[0].message.content)
        
        # แปลง JSON เป็น TravelResponse object
        travel_plan = TravelPlan(**result_json)
        return TravelResponse(travel_plan=travel_plan)
