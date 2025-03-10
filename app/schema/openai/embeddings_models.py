from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class EmbeddingsRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ embeddings
    """
    input: str | List[str] = Field(..., description="ข้อความที่ต้องการแปลงเป็น embeddings อาจเป็นข้อความเดียวหรือรายการข้อความ")
    model: str = Field("text-embedding-3-small", description="โมเดลที่ใช้สร้าง embeddings")
    encoding_format: Optional[str] = Field("float", description="รูปแบบการเข้ารหัส (float หรือ base64)")
    dimensions: Optional[int] = Field(None, description="จำนวนมิติของ embeddings ที่ต้องการ (ใช้ได้กับบางโมเดลเท่านั้น)")

class EmbeddingData(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูล embedding แต่ละรายการ
    """
    embedding: List[float] = Field(..., description="ค่า embedding vector")
    index: int = Field(..., description="ดัชนีของข้อความใน input")
    object: str = Field("embedding", description="ประเภทของออบเจ็กต์")

class EmbeddingsUsage(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลการใช้งาน token
    """
    prompt_tokens: int = Field(..., description="จำนวน token ที่ใช้ในคำขอ")
    total_tokens: int = Field(..., description="จำนวน token ทั้งหมดที่ใช้")

class EmbeddingsResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลตอบกลับ embeddings
    """
    data: List[EmbeddingData] = Field(..., description="รายการข้อมูล embedding")
    model: str = Field(..., description="โมเดลที่ใช้สร้าง embeddings")
    object: str = Field("list", description="ประเภทของออบเจ็กต์")
    usage: EmbeddingsUsage = Field(..., description="ข้อมูลการใช้งาน token")
