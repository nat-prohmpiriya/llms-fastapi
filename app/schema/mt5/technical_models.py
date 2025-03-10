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
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class MovingAverageRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ Moving Average
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    period: int = Field(..., description="จำนวนช่วงเวลาสำหรับคำนวณ MA")
    ma_type: MAMethod = Field(MAMethod.SMA, description="ประเภท MA (SMA, EMA, SMMA, LWMA)")
    applied_price: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)")
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class RSIRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ Relative Strength Index
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    period: int = Field(..., description="จำนวนช่วงเวลาสำหรับคำนวณ RSI")
    applied_price: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)")
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class MACDRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ MACD
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    fast_ema: int = Field(12, description="จำนวนช่วงเวลาสำหรับ Fast EMA")
    slow_ema: int = Field(26, description="จำนวนช่วงเวลาสำหรับ Slow EMA")
    signal_period: int = Field(9, description="จำนวนช่วงเวลาสำหรับ Signal Line")
    applied_price: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)")
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class BollingerBandsRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ Bollinger Bands
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    period: int = Field(20, description="จำนวนช่วงเวลาสำหรับคำนวณ")
    deviation: float = Field(2.0, description="จำนวนเท่าของส่วนเบี่ยงเบนมาตรฐาน")
    applied_price: PriceType = Field(PriceType.CLOSE, description="ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)")
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class StochasticRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ Stochastic Oscillator
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    k_period: int = Field(5, description="จำนวนช่วงเวลาสำหรับ %K")
    d_period: int = Field(3, description="จำนวนช่วงเวลาสำหรับ %D")
    slowing: int = Field(3, description="ค่าการชะลอตัว")
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class IchimokuRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลคำขอ Ichimoku Kinko Hyo
    """
    symbol: str = Field(..., description="ชื่อสัญลักษณ์ (เช่น 'EURUSD')")
    timeframe: TimeFrame = Field(..., description="กรอบเวลา")
    tenkan_period: int = Field(9, description="จำนวนช่วงเวลาสำหรับ Tenkan-sen (Conversion Line)")
    kijun_period: int = Field(26, description="จำนวนช่วงเวลาสำหรับ Kijun-sen (Base Line)")
    senkou_span_b_period: int = Field(52, description="จำนวนช่วงเวลาสำหรับ Senkou Span B (Leading Span B)")
    shift: Optional[int] = Field(0, description="จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน")

class IndicatorValue(BaseModel):
    """
    คลาสสำหรับเก็บค่าอินดิเคเตอร์
    """
    time: datetime = Field(..., description="เวลาของค่า")
    value: Union[float, List[float]] = Field(..., description="ค่าของอินดิเคเตอร์")

class BaseIndicatorResponse(BaseModel):
    """
    คลาสพื้นฐานสำหรับส่งข้อมูลอินดิเคเตอร์
    """
    success: bool = Field(..., description="สถานะความสำเร็จ")
    message: str = Field(..., description="ข้อความ")
    symbol: str = Field(..., description="ชื่อสัญลักษณ์")
    timeframe: str = Field(..., description="กรอบเวลา")

class MovingAverageResponse(BaseIndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Moving Average
    """
    value: Optional[float] = Field(None, description="ค่า Moving Average")
    period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้ในการคำนวณ")
    ma_type: str = Field(..., description="ประเภทของ Moving Average")
    applied_price: str = Field(..., description="ประเภทราคาที่ใช้")

class RSIResponse(BaseIndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Relative Strength Index
    """
    value: Optional[float] = Field(None, description="ค่า RSI")
    period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้ในการคำนวณ")
    applied_price: str = Field(..., description="ประเภทราคาที่ใช้")

class MACDResponse(BaseIndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล MACD
    """
    macd: Optional[float] = Field(None, description="ค่า MACD")
    signal: Optional[float] = Field(None, description="ค่า Signal Line")
    histogram: Optional[float] = Field(None, description="ค่า Histogram")
    fast_ema: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ Fast EMA")
    slow_ema: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ Slow EMA")
    signal_period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ Signal Line")
    applied_price: str = Field(..., description="ประเภทราคาที่ใช้")

class BollingerBandsResponse(BaseIndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Bollinger Bands
    """
    upper: Optional[float] = Field(None, description="ค่าเส้นบน")
    middle: Optional[float] = Field(None, description="ค่าเส้นกลาง")
    lower: Optional[float] = Field(None, description="ค่าเส้นล่าง")
    period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้ในการคำนวณ")
    deviation: float = Field(..., description="จำนวนเท่าของส่วนเบี่ยงเบนมาตรฐาน")
    applied_price: str = Field(..., description="ประเภทราคาที่ใช้")

class StochasticResponse(BaseIndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Stochastic Oscillator
    """
    k: Optional[float] = Field(None, description="ค่า %K")
    d: Optional[float] = Field(None, description="ค่า %D")
    k_period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ %K")
    d_period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ %D")
    slowing: int = Field(..., description="ค่าการชะลอตัว")

class IchimokuResponse(BaseIndicatorResponse):
    """
    คลาสสำหรับส่งข้อมูล Ichimoku Kinko Hyo
    """
    tenkan_sen: Optional[float] = Field(None, description="ค่า Tenkan-sen (Conversion Line)")
    kijun_sen: Optional[float] = Field(None, description="ค่า Kijun-sen (Base Line)")
    senkou_span_a: Optional[float] = Field(None, description="ค่า Senkou Span A (Leading Span A)")
    senkou_span_b: Optional[float] = Field(None, description="ค่า Senkou Span B (Leading Span B)")
    chikou_span: Optional[float] = Field(None, description="ค่า Chikou Span (Lagging Span)")
    tenkan_period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ Tenkan-sen")
    kijun_period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ Kijun-sen")
    senkou_span_b_period: int = Field(..., description="จำนวนช่วงเวลาที่ใช้สำหรับ Senkou Span B")
