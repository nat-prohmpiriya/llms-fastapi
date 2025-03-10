from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DocumentRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลเอกสารที่ต้องการเพิ่ม
    """
    content: str = Field(..., description="เนื้อหาของเอกสาร")
    metadata: Optional[Dict[str, Any]] = Field(None, description="ข้อมูลเพิ่มเติมของเอกสาร")
    model: str = Field("text-embedding-3-small", description="โมเดลที่ใช้สร้าง embeddings")

class DocumentResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลเอกสารที่เพิ่มแล้ว
    """
    document_id: int = Field(..., description="ID ของเอกสาร")
    content: str = Field(..., description="เนื้อหาของเอกสาร")
    metadata: Optional[Dict[str, Any]] = Field(None, description="ข้อมูลเพิ่มเติมของเอกสาร")
    model: str = Field(..., description="โมเดลที่ใช้สร้าง embeddings")

class SearchRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำค้นหา
    """
    query: str = Field(..., description="คำค้นหา")
    model: str = Field("text-embedding-3-small", description="โมเดลที่ใช้สร้าง embeddings")
    top_k: int = Field(5, description="จำนวนผลลัพธ์ที่ต้องการ")

class SearchResult(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลผลลัพธ์การค้นหาแต่ละรายการ
    """
    document_id: int = Field(..., description="ID ของเอกสาร")
    content: str = Field(..., description="เนื้อหาของเอกสาร")
    metadata: Optional[Dict[str, Any]] = Field(None, description="ข้อมูลเพิ่มเติมของเอกสาร")
    similarity: float = Field(..., description="ค่าความคล้ายคลึง (0-1)")

class SearchResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลผลลัพธ์การค้นหา
    """
    results: List[SearchResult] = Field(..., description="รายการผลลัพธ์การค้นหา")
    query: str = Field(..., description="คำค้นหา")
    model: str = Field(..., description="โมเดลที่ใช้สร้าง embeddings")
