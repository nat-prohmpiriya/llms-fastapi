from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class AccountInfoResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลบัญชี
    """
    login: int = Field(..., description="หมายเลขบัญชี")
    trade_mode: int = Field(..., description="โหมดการเทรด (0-demo, 1-real)")
    leverage: int = Field(..., description="คันเร่ง (leverage)")
    limit_orders: int = Field(..., description="จำนวนออเดอร์สูงสุดที่อนุญาต")
    margin_so_mode: int = Field(..., description="โหมดการคำนวณมาร์จิ้น")
    trade_allowed: bool = Field(..., description="อนุญาตให้เทรดหรือไม่")
    trade_expert: bool = Field(..., description="อนุญาตให้ใช้ Expert Advisor หรือไม่")
    balance: float = Field(..., description="ยอดเงินในบัญชี")
    credit: float = Field(..., description="เครดิตในบัญชี")
    profit: float = Field(..., description="กำไร/ขาดทุนปัจจุบัน")
    equity: float = Field(..., description="อิควิตี้ (equity)")
    margin: float = Field(..., description="มาร์จิ้นที่ใช้")
    margin_free: float = Field(..., description="มาร์จิ้นที่เหลือ")
    margin_level: float = Field(..., description="ระดับมาร์จิ้น (%)")
    margin_so_call: float = Field(..., description="ระดับมาร์จิ้นคอล (%)")
    margin_so_so: float = Field(..., description="ระดับมาร์จิ้นสต็อป (%)")
    currency: str = Field(..., description="สกุลเงินของบัญชี")
    server: str = Field(..., description="เซิร์ฟเวอร์ที่เชื่อมต่อ")
    name: str = Field(..., description="ชื่อเจ้าของบัญชี")
    company: str = Field(..., description="ชื่อบริษัทโบรกเกอร์")

class HistoryOrderFilter(BaseModel):
    """
    คลาสสำหรับรับพารามิเตอร์การกรองประวัติออเดอร์
    """
    from_date: datetime = Field(..., description="วันที่เริ่มต้น")
    to_date: Optional[datetime] = Field(None, description="วันที่สิ้นสุด (ถ้าไม่ระบุจะใช้วันที่ปัจจุบัน)")
    group: Optional[str] = Field(None, description="กลุ่มสัญลักษณ์ เช่น '*' สำหรับทั้งหมด หรือ 'EUR*' สำหรับคู่สกุลเงินที่ขึ้นต้นด้วย EUR")

class HistoryDealFilter(BaseModel):
    """
    คลาสสำหรับรับพารามิเตอร์การกรองประวัติดีล
    """
    from_date: datetime = Field(..., description="วันที่เริ่มต้น")
    to_date: Optional[datetime] = Field(None, description="วันที่สิ้นสุด (ถ้าไม่ระบุจะใช้วันที่ปัจจุบัน)")
    group: Optional[str] = Field(None, description="กลุ่มสัญลักษณ์ เช่น '*' สำหรับทั้งหมด หรือ 'EUR*' สำหรับคู่สกุลเงินที่ขึ้นต้นด้วย EUR")

class OrderInfo(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลออเดอร์
    """
    ticket: int = Field(..., description="หมายเลขออเดอร์")
    time_setup: datetime = Field(..., description="เวลาที่ตั้งออเดอร์")
    type: int = Field(..., description="ประเภทออเดอร์")
    type_description: str = Field(..., description="คำอธิบายประเภทออเดอร์")
    state: int = Field(..., description="สถานะออเดอร์")
    state_description: str = Field(..., description="คำอธิบายสถานะออเดอร์")
    time_expiration: Optional[datetime] = Field(None, description="เวลาหมดอายุ")
    time_done: Optional[datetime] = Field(None, description="เวลาที่ดำเนินการเสร็จสิ้น")
    symbol: str = Field(..., description="สัญลักษณ์")
    volume: float = Field(..., description="ปริมาณ")
    price_open: float = Field(..., description="ราคาเปิด")
    price_current: float = Field(..., description="ราคาปัจจุบัน")
    price_sl: Optional[float] = Field(None, description="ราคา Stop Loss")
    price_tp: Optional[float] = Field(None, description="ราคา Take Profit")
    position_id: Optional[int] = Field(None, description="ID ของตำแหน่ง")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")

class DealInfo(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลดีล
    """
    ticket: int = Field(..., description="หมายเลขดีล")
    order: int = Field(..., description="หมายเลขออเดอร์ที่เกี่ยวข้อง")
    time: datetime = Field(..., description="เวลาที่ดำเนินการ")
    type: int = Field(..., description="ประเภทดีล")
    type_description: str = Field(..., description="คำอธิบายประเภทดีล")
    entry: int = Field(..., description="ทิศทางการเข้า (0-in, 1-out, 2-inout)")
    entry_description: str = Field(..., description="คำอธิบายทิศทางการเข้า")
    symbol: str = Field(..., description="สัญลักษณ์")
    volume: float = Field(..., description="ปริมาณ")
    price: float = Field(..., description="ราคา")
    profit: float = Field(..., description="กำไร/ขาดทุน")
    commission: float = Field(..., description="ค่าคอมมิชชัน")
    swap: float = Field(..., description="ค่าสวอป")
    fee: float = Field(..., description="ค่าธรรมเนียม")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")

class PositionInfo(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลตำแหน่ง
    """
    ticket: int = Field(..., description="หมายเลขตำแหน่ง")
    time: datetime = Field(..., description="เวลาที่เปิดตำแหน่ง")
    type: int = Field(..., description="ประเภทตำแหน่ง (0-buy, 1-sell)")
    type_description: str = Field(..., description="คำอธิบายประเภทตำแหน่ง")
    magic: int = Field(..., description="หมายเลข Magic")
    identifier: int = Field(..., description="ตัวระบุตำแหน่ง")
    reason: int = Field(..., description="เหตุผลในการเปิดตำแหน่ง")
    symbol: str = Field(..., description="สัญลักษณ์")
    volume: float = Field(..., description="ปริมาณ")
    price_open: float = Field(..., description="ราคาเปิด")
    price_current: float = Field(..., description="ราคาปัจจุบัน")
    price_sl: Optional[float] = Field(None, description="ราคา Stop Loss")
    price_tp: Optional[float] = Field(None, description="ราคา Take Profit")
    profit: float = Field(..., description="กำไร/ขาดทุนปัจจุบัน")
    swap: float = Field(..., description="ค่าสวอปสะสม")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")

class HistoryOrdersResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลประวัติออเดอร์
    """
    orders: List[OrderInfo] = Field(..., description="รายการประวัติออเดอร์")
    total: int = Field(..., description="จำนวนออเดอร์ทั้งหมด")
    from_date: datetime = Field(..., description="วันที่เริ่มต้น")
    to_date: datetime = Field(..., description="วันที่สิ้นสุด")

class HistoryDealsResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลประวัติดีล
    """
    deals: List[DealInfo] = Field(..., description="รายการประวัติดีล")
    total: int = Field(..., description="จำนวนดีลทั้งหมด")
    from_date: datetime = Field(..., description="วันที่เริ่มต้น")
    to_date: datetime = Field(..., description="วันที่สิ้นสุด")

class PositionsResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลตำแหน่งที่เปิดอยู่
    """
    positions: List[PositionInfo] = Field(..., description="รายการตำแหน่งที่เปิดอยู่")
    total: int = Field(..., description="จำนวนตำแหน่งทั้งหมด")
