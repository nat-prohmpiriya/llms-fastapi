# LLMs FastAPI

ระบบ API สำหรับบริการ AI ต่างๆ พัฒนาด้วย FastAPI และ Python

## รายละเอียดโปรเจค

โปรเจคนี้เป็นระบบ API ที่ให้บริการด้าน AI ต่างๆ ประกอบด้วย:
- บริการแชทกับ OpenAI (GPT)
- บริการวางแผนการท่องเที่ยวโดยใช้ AI

## การติดตั้ง

1. โคลนโปรเจค
```bash
git clone <repository-url>
cd llms-fastapi
```

2. สร้าง Virtual Environment และติดตั้ง Dependencies
```bash
# สร้าง virtual environment
python -m venv venv
# เปิดใช้งาน virtual environment
# สำหรับ Windows
venv\Scripts\activate
# สำหรับ Linux/Mac
source venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

3. ตั้งค่าไฟล์ .env
```
OPENAI_API_KEY=your_openai_api_key_here
```

## การใช้งาน

1. รันเซิร์ฟเวอร์
```bash
# รันด้วย uvicorn โดยตรง
uvicorn app.main:app --reload

# หรือใช้สคริปต์ rundev.sh
bash rundev.sh
```

2. เข้าถึง API ได้ที่
- API Documentation: http://localhost:8000/docs
- API หน้าแรก: http://localhost:8000/

## API Endpoints

### OpenAI Chat
- **Endpoint**: `/api/v1/openai/chat`
- **Method**: POST
- **Description**: ส่งข้อความไปยัง OpenAI และรับการตอบกลับ
- **Request Body**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "สวัสดี"
    }
  ],
  "model": "gpt-3.5-turbo",
  "temperature": 0.7
}
```

### Tourism Planning
- **Endpoint**: `/api/v1/tourism/travel-plan`
- **Method**: POST
- **Description**: สร้างแผนการท่องเที่ยวตามความต้องการของผู้ใช้
- **Request Body**:
```json
{
  "query": "อยากไปเที่ยวเชียงใหม่ช่วงปลายปี",
  "destination": "เชียงใหม่",
  "budget": 10000,
  "duration": 3,
  "interests": ["อาหาร", "ธรรมชาติ", "วัฒนธรรม"]
}
```

## โครงสร้างโปรเจค

```
llms-fastapi/
├── app/
│   ├── main.py                  # Entry point ของแอปพลิเคชัน
│   ├── routes/                  # API routes
│   │   ├── openai/              # OpenAI API routes
│   │   │   └── chat_route.py    # OpenAI chat endpoints
│   │   └── tourism/             # Tourism API routes
│   │       └── tourism_router.py # Tourism planning endpoints
│   ├── schema/                  # Pydantic models
│   │   ├── openai/              # OpenAI schemas
│   │   │   └── chat_models.py   # Chat request/response models
│   │   └── tourism/             # Tourism schemas
│   │       └── travel_models.py # Travel planning models
│   └── services/                # Business logic
│       ├── opeai_service.py     # OpenAI service
│       └── tourism_service.py   # Tourism service
├── docs/                        # เอกสารและตัวอย่าง
│   └── postman/                 # Postman collections
├── .env                         # Environment variables
├── requirements.txt             # Dependencies
└── README.md                    # คุณกำลังอ่านไฟล์นี้อยู่
```

## ข้อกำหนดทางเทคนิค

- Python 3.8+
- FastAPI
- OpenAI Python SDK
- Pydantic
- Uvicorn

## ผู้พัฒนา

[ชื่อผู้พัฒนา]

## License

[ระบุ License ที่ใช้]
