from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class OrderType(int, Enum):
    """
    คลาสสำหรับกำหนดประเภทออเดอร์
    """
    BUY = 0                  # ซื้อตลาด
    SELL = 1                 # ขายตลาด
    BUY_LIMIT = 2            # ซื้อลิมิต
    SELL_LIMIT = 3           # ขายลิมิต
    BUY_STOP = 4             # ซื้อสต็อป
    SELL_STOP = 5            # ขายสต็อป
    BUY_STOP_LIMIT = 6       # ซื้อสต็อปลิมิต
    SELL_STOP_LIMIT = 7      # ขายสต็อปลิมิต
    CLOSE_BY = 8             # ปิดด้วยตำแหน่งตรงข้าม

class OrderFilling(int, Enum):
    """
    คลาสสำหรับกำหนดประเภทการเติมเต็มออเดอร์
    """
    FOK = 0      # Fill or Kill
    IOC = 1      # Immediate or Cancel
    RETURN = 2   # Return

class OrderTime(int, Enum):
    """
    คลาสสำหรับกำหนดประเภทเวลาออเดอร์
    """
    GTC = 0      # Good Till Cancelled
    DAY = 1      # Good Till Day
    SPECIFIED = 2 # Good Till Specified
    SPECIFIED_DAY = 3 # Good Till Specified Day

class OpenOrderRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอเปิดออเดอร์
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    order_type: OrderType = Field(..., description="ประเภทออเดอร์")
    volume: float = Field(..., description="ปริมาณ")
    price: Optional[float] = Field(None, description="ราคา (จำเป็นสำหรับออเดอร์ลิมิตและสต็อป)")
    sl: Optional[float] = Field(None, description="ราคา Stop Loss")
    tp: Optional[float] = Field(None, description="ราคา Take Profit")
    deviation: Optional[int] = Field(10, description="ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)")
    magic: Optional[int] = Field(0, description="หมายเลข Magic")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")
    type_filling: Optional[OrderFilling] = Field(OrderFilling.FOK, description="ประเภทการเติมเต็มออเดอร์")
    type_time: Optional[OrderTime] = Field(OrderTime.GTC, description="ประเภทเวลาออเดอร์")
    expiration: Optional[int] = Field(None, description="เวลาหมดอายุ (สำหรับ SPECIFIED และ SPECIFIED_DAY)")

class CloseOrderRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอปิดออเดอร์
    """
    ticket: int = Field(..., description="หมายเลขตำแหน่ง")
    volume: Optional[float] = Field(None, description="ปริมาณที่ต้องการปิด (ถ้าไม่ระบุจะปิดทั้งหมด)")
    deviation: Optional[int] = Field(10, description="ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")

class ModifyOrderRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอแก้ไขออเดอร์
    """
    ticket: int = Field(..., description="หมายเลขตำแหน่งหรือออเดอร์")
    price: Optional[float] = Field(None, description="ราคาใหม่")
    sl: Optional[float] = Field(None, description="ราคา Stop Loss ใหม่")
    tp: Optional[float] = Field(None, description="ราคา Take Profit ใหม่")
    deviation: Optional[int] = Field(10, description="ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)")
    type_time: Optional[OrderTime] = Field(None, description="ประเภทเวลาออเดอร์ใหม่")
    expiration: Optional[int] = Field(None, description="เวลาหมดอายุใหม่")
    comment: Optional[str] = Field(None, description="ความคิดเห็นใหม่")

class CancelOrderRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอยกเลิกออเดอร์
    """
    ticket: int = Field(..., description="หมายเลขออเดอร์")

class TrailingStopRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอตั้งค่า Trailing Stop
    """
    ticket: int = Field(..., description="หมายเลขตำแหน่ง")
    distance: int = Field(..., description="ระยะห่างของ Trailing Stop (ในจุด)")
    step: Optional[int] = Field(1, description="ขั้นตอนการเปลี่ยนแปลง (ในจุด)")

class CloseAllRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอปิดออเดอร์ทั้งหมด
    """
    symbol: Optional[str] = Field(None, description="ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะปิดทั้งหมด)")
    magic: Optional[int] = Field(None, description="หมายเลข Magic (ถ้าไม่ระบุจะปิดทั้งหมด)")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")

class TradeResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลผลลัพธ์การเทรด
    """
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความแสดงผลลัพธ์")
    ticket: Optional[int] = Field(None, description="หมายเลขตำแหน่งหรือออเดอร์")
    volume: Optional[float] = Field(None, description="ปริมาณ")
    price: Optional[float] = Field(None, description="ราคา")
    bid: Optional[float] = Field(None, description="ราคาเสนอซื้อ")
    ask: Optional[float] = Field(None, description="ราคาเสนอขาย")
    comment: Optional[str] = Field(None, description="ความคิดเห็น")
    request_id: Optional[int] = Field(None, description="ID ของคำขอ")
    retcode: Optional[int] = Field(None, description="รหัสผลลัพธ์")
    retcode_description: Optional[str] = Field(None, description="คำอธิบายรหัสผลลัพธ์")
