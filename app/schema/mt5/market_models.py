from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TimeFrame(str, Enum):
    """
    คลาสสำหรับกำหนดกรอบเวลา
    """
    M1 = "M1"      # 1 นาที
    M5 = "M5"      # 5 นาที
    M15 = "M15"    # 15 นาที
    M30 = "M30"    # 30 นาที
    H1 = "H1"      # 1 ชั่วโมง
    H4 = "H4"      # 4 ชั่วโมง
    D1 = "D1"      # 1 วัน
    W1 = "W1"      # 1 สัปดาห์
    MN1 = "MN1"    # 1 เดือน

class SymbolInfo(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลสัญลักษณ์
    """
    name: str = Field(..., description="ชื่อสัญลักษณ์")
    description: str = Field(..., description="คำอธิบายสัญลักษณ์")
    path: str = Field(..., description="พาธของสัญลักษณ์ในต้นไม้ Market Watch")
    currency_base: str = Field(..., description="สกุลเงินฐาน")
    currency_profit: str = Field(..., description="สกุลเงินกำไร")
    currency_margin: str = Field(..., description="สกุลเงินมาร์จิ้น")
    digits: int = Field(..., description="จำนวนตำแหน่งทศนิยม")
    spread: int = Field(..., description="สเปรดในจุด")
    trade_mode: int = Field(..., description="ประเภทการซื้อขาย")
    trade_mode_description: str = Field(..., description="คำอธิบายประเภทการซื้อขาย")
    volume_min: float = Field(..., description="ปริมาณการซื้อขายขั้นต่ำ")
    volume_max: float = Field(..., description="ปริมาณการซื้อขายสูงสุด")
    volume_step: float = Field(..., description="ขั้นตอนการเปลี่ยนแปลงปริมาณการซื้อขาย")
    tick_size: float = Field(..., description="ขนาดการเปลี่ยนแปลงราคาขั้นต่ำ")
    tick_value: float = Field(..., description="มูลค่าของการเปลี่ยนแปลงราคาขั้นต่ำ")
    contract_size: float = Field(..., description="ขนาดสัญญา")
    swap_long: float = Field(..., description="ค่าสวอปสำหรับตำแหน่ง Long")
    swap_short: float = Field(..., description="ค่าสวอปสำหรับตำแหน่ง Short")
    margin_initial: float = Field(..., description="มาร์จิ้นเริ่มต้น")
    margin_maintenance: float = Field(..., description="มาร์จิ้นรักษาสภาพ")

class SymbolsResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลรายการสัญลักษณ์
    """
    symbols: List[str] = Field(..., description="รายการชื่อสัญลักษณ์")
    total: int = Field(..., description="จำนวนสัญลักษณ์ทั้งหมด")

class SymbolInfoResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลสัญลักษณ์
    """
    info: SymbolInfo = Field(..., description="ข้อมูลสัญลักษณ์")

class TickData(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูล tick
    """
    time: datetime = Field(..., description="เวลาของ tick")
    bid: float = Field(..., description="ราคาเสนอซื้อ")
    ask: float = Field(..., description="ราคาเสนอขาย")
    last: float = Field(..., description="ราคาซื้อขายล่าสุด")
    volume: float = Field(..., description="ปริมาณ")
    flags: int = Field(..., description="แฟล็ก")

class PriceRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอราคา
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")

class TickRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ tick
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    count: Optional[int] = Field(100, description="จำนวน tick ที่ต้องการ")

class OHLCRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ OHLC
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    count: Optional[int] = Field(100, description="จำนวนแท่งเทียนที่ต้องการ")
    from_date: Optional[datetime] = Field(None, description="วันที่เริ่มต้น")
    to_date: Optional[datetime] = Field(None, description="วันที่สิ้นสุด")

class PriceResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลราคา
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    bid: float = Field(..., description="ราคาเสนอซื้อ")
    ask: float = Field(..., description="ราคาเสนอขาย")
    last: float = Field(..., description="ราคาซื้อขายล่าสุด")
    time: datetime = Field(..., description="เวลาของราคา")

class TickResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูล tick
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    ticks: List[TickData] = Field(..., description="รายการข้อมูล tick")
    count: int = Field(..., description="จำนวน tick ทั้งหมด")

class CandleData(BaseModel):
    """
    คลาสสำหรับเก็บข้อมูลแท่งเทียน
    """
    time: datetime = Field(..., description="เวลาเปิดของแท่งเทียน")
    open: float = Field(..., description="ราคาเปิด")
    high: float = Field(..., description="ราคาสูงสุด")
    low: float = Field(..., description="ราคาต่ำสุด")
    close: float = Field(..., description="ราคาปิด")
    tick_volume: int = Field(..., description="ปริมาณ tick")
    spread: int = Field(..., description="สเปรด")
    real_volume: int = Field(..., description="ปริมาณจริง")

class OHLCResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูล OHLC
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    timeframe: str = Field(..., description="กรอบเวลา")
    candles: List[CandleData] = Field(..., description="รายการข้อมูลแท่งเทียน")
    count: int = Field(..., description="จำนวนแท่งเทียนทั้งหมด")
