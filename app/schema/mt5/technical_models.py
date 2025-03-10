from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime
from schema.mt5.market_models import TimeFrame

class MAMethod(int, Enum):
    """
    คลาสสำหรับกำหนดวิธีการคำนวณ Moving Average
    """
    SMA = 0    # Simple Moving Average
    EMA = 1    # Exponential Moving Average
    SMMA = 2   # Smoothed Moving Average
    LWMA = 3   # Linear Weighted Moving Average

class PriceType(int, Enum):
    """
    คลาสสำหรับกำหนดประเภทราคาที่ใช้ในการคำนวณ
    """
    CLOSE = 0  # ราคาปิด
    OPEN = 1   # ราคาเปิด
    HIGH = 2   # ราคาสูงสุด
    LOW = 3    # ราคาต่ำสุด
    MEDIAN = 4 # ราคากลาง (high+low)/2
    TYPICAL = 5 # ราคาทั่วไป (high+low+close)/3
    WEIGHTED = 6 # ราคาถ่วงน้ำหนัก (high+low+close+close)/4

class IndicatorRequest(BaseModel):
    """
    คลาสพื้นฐานสำหรับคำขอข้อมูลอินดิเคเตอร์
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    count: Optional[int] = Field(100, description="จำนวนค่าที่ต้องการ")
    from_date: Optional[datetime] = Field(None, description="วันที่เริ่มต้น")
    to_date: Optional[datetime] = Field(None, description="วันที่สิ้นสุด")

class MARequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Moving Average
    """
    period: int = Field(..., description="จำนวนช่วงเวลา")
    ma_method: MAMethod = Field(MAMethod.SMA, description="วิธีการคำนวณ MA")
    price_type: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้")
    shift: Optional[int] = Field(0, description="การเลื่อนค่า")

class RSIRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Relative Strength Index
    """
    period: int = Field(..., description="จำนวนช่วงเวลา")
    price_type: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้")

class MACDRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ MACD
    """
    fast_period: int = Field(..., description="จำนวนช่วงเวลาสั้น")
    slow_period: int = Field(..., description="จำนวนช่วงเวลายาว")
    signal_period: int = Field(..., description="จำนวนช่วงเวลาสัญญาณ")
    price_type: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้")

class BollingerBandsRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Bollinger Bands
    """
    period: int = Field(..., description="จำนวนช่วงเวลา")
    deviation: float = Field(..., description="จำนวนเท่าของค่าเบี่ยงเบนมาตรฐาน")
    price_type: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้")

class StochasticRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Stochastic Oscillator
    """
    k_period: int = Field(..., description="จำนวนช่วงเวลา %K")
    d_period: int = Field(..., description="จำนวนช่วงเวลา %D")
    slowing: int = Field(..., description="ค่าการชะลอตัว")
    ma_method: MAMethod = Field(MAMethod.SMA, description="วิธีการคำนวณ MA")
    price_field: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้")

class ADXRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Average Directional Index
    """
    period: int = Field(..., description="จำนวนช่วงเวลา")

class ATRRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Average True Range
    """
    period: int = Field(..., description="จำนวนช่วงเวลา")

class IchimokuRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Ichimoku Kinko Hyo
    """
    tenkan_sen: int = Field(..., description="จำนวนช่วงเวลา Tenkan-sen (Conversion Line)")
    kijun_sen: int = Field(..., description="จำนวนช่วงเวลา Kijun-sen (Base Line)")
    senkou_span_b: int = Field(..., description="จำนวนช่วงเวลา Senkou Span B (Leading Span B)")

class FibonacciRequest(IndicatorRequest):
    """
    คลาสสำหรับรับข้อมูลคำขอ Fibonacci Retracement
    """
    high_price: float = Field(..., description="ราคาสูงสุด")
    low_price: float = Field(..., description="ราคาต่ำสุด")
    is_retracement: bool = Field(True, description="เป็น Retracement หรือ Extension")

class IndicatorValue(BaseModel):
    """
    คลาสสำหรับเก็บค่าอินดิเคเตอร์
    """
    time: datetime = Field(..., description="เวลาของค่า")
    value: Union[float, List[float]] = Field(..., description="ค่าของอินดิเคเตอร์")

class IndicatorResponse(BaseModel):
    """
    คลาสพื้นฐานสำหรับส่งข้อมูลอินดิเคเตอร์
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    timeframe: str = Field(..., description="กรอบเวลา")
    indicator: str = Field(..., description="ชื่ออินดิเคเตอร์")
    values: List[IndicatorValue] = Field(..., description="ค่าของอินดิเคเตอร์")
    count: int = Field(..., description="จำนวนค่าทั้งหมด")
    parameters: Dict[str, Any] = Field(..., description="พารามิเตอร์ที่ใช้ในการคำนวณ")

class MAResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Moving Average
    """
    pass

class RSIResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Relative Strength Index
    """
    pass

class MACDResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล MACD
    """
    pass

class BollingerBandsResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Bollinger Bands
    """
    pass

class StochasticResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Stochastic Oscillator
    """
    pass

class ADXResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Average Directional Index
    """
    pass

class ATRResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Average True Range
    """
    pass

class IchimokuResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Ichimoku Kinko Hyo
    """
    pass

class FibonacciResponse(IndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Fibonacci Retracement
    """
    pass
