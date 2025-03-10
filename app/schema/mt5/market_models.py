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

class TickFlag(str, Enum):
    """
    คลาสสำหรับกำหนดประเภทของ Tick
    """
    ALL = "ALL"    # ทั้งหมด
    INFO = "INFO"  # ข้อมูล
    TRADE = "TRADE"  # การซื้อขาย
    BUY = "BUY"    # การซื้อ
    SELL = "SELL"  # การขาย
    LAST = "LAST"  # ล่าสุด

# Request Models
class SymbolsRequest(BaseModel):
    """
    คลาสสำหรับ request รายการสัญลักษณ์
    """
    group: Optional[str] = Field(None, description="กลุ่มสัญลักษณ์ (เช่น '*' หรือ 'EUR*')")

class SymbolInfoRequest(BaseModel):
    """
    คลาสสำหรับ request ข้อมูลสัญลักษณ์
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")

class LastTickRequest(BaseModel):
    """
    คลาสสำหรับ request ข้อมูล tick ล่าสุด
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")

class CopyRatesRequest(BaseModel):
    """
    คลาสสำหรับ request ข้อมูลแท่งเทียน
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    from_date: Optional[datetime] = Field(None, description="วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD HH:MM:SS)")
    to_date: Optional[datetime] = Field(None, description="วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD HH:MM:SS)")
    count: Optional[int] = Field(None, description="จำนวนแท่งเทียนที่ต้องการ")

class CopyTicksRequest(BaseModel):
    """
    คลาสสำหรับ request ข้อมูล tick
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    from_date: datetime = Field(..., description="วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD HH:MM:SS)")
    to_date: datetime = Field(..., description="วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD HH:MM:SS)")
    flags: TickFlag = Field(TickFlag.ALL, description="ประเภทของ tick ที่ต้องการ")

# Response Models
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
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความ")
    symbols: List[str] = Field(..., description="รายการชื่อสัญลักษณ์")
    total: int = Field(..., description="จำนวนสัญลักษณ์ทั้งหมด")

class SymbolInfoResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลสัญลักษณ์
    """
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความ")
    info: Optional[SymbolInfo] = Field(None, description="ข้อมูลสัญลักษณ์")

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

class LastTickResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูล tick ล่าสุด
    """
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความ")
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    tick: Optional[TickData] = Field(None, description="ข้อมูล tick ล่าสุด")

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

class CopyRatesResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลแท่งเทียน
    """
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความ")
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    timeframe: str = Field(..., description="กรอบเวลา")
    candles: List[CandleData] = Field([], description="รายการข้อมูลแท่งเทียน")
    count: int = Field(0, description="จำนวนแท่งเทียนทั้งหมด")

class CopyTicksResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูล tick
    """
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความ")
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    ticks: List[TickData] = Field([], description="รายการข้อมูล tick")
    count: int = Field(0, description="จำนวน tick ทั้งหมด")
