from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schema.mt5.technical_models import (
    MovingAverageRequest, MovingAverageResponse,
    RSIRequest, RSIResponse,
    MACDRequest, MACDResponse,
    BollingerBandsRequest, BollingerBandsResponse,
    StochasticRequest, StochasticResponse,
    IchimokuRequest, IchimokuResponse
)
from services.mt5_technical_service import MT5TechnicalService

router = APIRouter(
    prefix="/api/v1/mt5/technical",
    tags=["MT5 Technical Analysis"]
)

# สร้าง instance ของ MT5TechnicalService
def get_technical_service():
    return MT5TechnicalService()

@router.post("/ma", response_model=MovingAverageResponse)
async def get_moving_average(request: MovingAverageRequest, service: MT5TechnicalService = Depends(get_technical_service)):
    """
    คำนวณค่าเฉลี่ยเคลื่อนที่ (Moving Average)
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **period**: จำนวนช่วงเวลาสำหรับคำนวณ MA
    - **ma_type**: ประเภท MA (SMA, EMA, SMMA, LWMA)
    - **applied_price**: ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)
    - **shift**: จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน
    
    Returns:
    - **MovingAverageResponse**: ผลลัพธ์ของค่าเฉลี่ยเคลื่อนที่
    """
    response = service.get_moving_average(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/rsi", response_model=RSIResponse)
async def get_rsi(request: RSIRequest, service: MT5TechnicalService = Depends(get_technical_service)):
    """
    คำนวณค่า Relative Strength Index (RSI)
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **period**: จำนวนช่วงเวลาสำหรับคำนวณ RSI
    - **applied_price**: ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)
    - **shift**: จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน
    
    Returns:
    - **RSIResponse**: ผลลัพธ์ของ RSI
    """
    response = service.get_rsi(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/macd", response_model=MACDResponse)
async def get_macd(request: MACDRequest, service: MT5TechnicalService = Depends(get_technical_service)):
    """
    คำนวณค่า Moving Average Convergence Divergence (MACD)
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **fast_ema**: จำนวนช่วงเวลาสำหรับ Fast EMA (ค่าเริ่มต้น 12)
    - **slow_ema**: จำนวนช่วงเวลาสำหรับ Slow EMA (ค่าเริ่มต้น 26)
    - **signal_period**: จำนวนช่วงเวลาสำหรับ Signal Line (ค่าเริ่มต้น 9)
    - **applied_price**: ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)
    - **shift**: จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน
    
    Returns:
    - **MACDResponse**: ผลลัพธ์ของ MACD
    """
    response = service.get_macd(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/bollinger", response_model=BollingerBandsResponse)
async def get_bollinger_bands(request: BollingerBandsRequest, service: MT5TechnicalService = Depends(get_technical_service)):
    """
    คำนวณค่า Bollinger Bands
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **period**: จำนวนช่วงเวลาสำหรับคำนวณ (ค่าเริ่มต้น 20)
    - **deviation**: จำนวนเท่าของส่วนเบี่ยงเบนมาตรฐาน (ค่าเริ่มต้น 2.0)
    - **applied_price**: ประเภทราคาที่ใช้ (CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED)
    - **shift**: จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน
    
    Returns:
    - **BollingerBandsResponse**: ผลลัพธ์ของ Bollinger Bands
    """
    response = service.get_bollinger_bands(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/stochastic", response_model=StochasticResponse)
async def get_stochastic(request: StochasticRequest, service: MT5TechnicalService = Depends(get_technical_service)):
    """
    คำนวณค่า Stochastic Oscillator
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **k_period**: จำนวนช่วงเวลาสำหรับ %K (ค่าเริ่มต้น 5)
    - **d_period**: จำนวนช่วงเวลาสำหรับ %D (ค่าเริ่มต้น 3)
    - **slowing**: จำนวนช่วงเวลาสำหรับ Slowing (ค่าเริ่มต้น 3)
    - **shift**: จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน
    
    Returns:
    - **StochasticResponse**: ผลลัพธ์ของ Stochastic Oscillator
    """
    response = service.get_stochastic(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/ichimoku", response_model=IchimokuResponse)
async def get_ichimoku(request: IchimokuRequest, service: MT5TechnicalService = Depends(get_technical_service)):
    """
    คำนวณค่า Ichimoku Cloud
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **tenkan_period**: จำนวนช่วงเวลาสำหรับ Tenkan-sen (ค่าเริ่มต้น 9)
    - **kijun_period**: จำนวนช่วงเวลาสำหรับ Kijun-sen (ค่าเริ่มต้น 26)
    - **senkou_span_b_period**: จำนวนช่วงเวลาสำหรับ Senkou Span B (ค่าเริ่มต้น 52)
    - **shift**: จำนวนแท่งที่ต้องการถอยกลับจากแท่งปัจจุบัน
    
    Returns:
    - **IchimokuResponse**: ผลลัพธ์ของ Ichimoku Cloud
    """
    response = service.get_ichimoku(request)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response
