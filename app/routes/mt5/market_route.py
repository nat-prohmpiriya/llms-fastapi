from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from schema.mt5.market_models import (
    SymbolInfoRequest, SymbolInfoResponse,
    SymbolsRequest, SymbolsResponse,
    LastTickRequest, LastTickResponse,
    CopyRatesRequest, CopyRatesResponse,
    CopyTicksRequest, CopyTicksResponse
)
from services.mt5_market_service import MT5MarketService

router = APIRouter(
    prefix="/api/v1/mt5/market",
    tags=["MT5 Market Data"]
)

# สร้าง instance ของ MT5MarketService
def get_market_service():
    return MT5MarketService()

@router.post("/symbols", response_model=SymbolsResponse)
async def get_symbols(request: SymbolsRequest, service: MT5MarketService = Depends(get_market_service)):
    """
    รับรายการสัญลักษณ์ (Symbols)
    
    Parameters:
    - **group**: กลุ่มสัญลักษณ์ (ถ้าไม่ระบุจะดึงทั้งหมด เช่น "*, !EURUSD" หมายถึงทั้งหมดยกเว้น EURUSD)
    
    Returns:
    - **SymbolsResponse**: รายการสัญลักษณ์
    """
    response = service.get_symbols(group=request.group)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/symbol-info", response_model=SymbolInfoResponse)
async def get_symbol_info(request: SymbolInfoRequest, service: MT5MarketService = Depends(get_market_service)):
    """
    รับข้อมูลสัญลักษณ์
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    
    Returns:
    - **SymbolInfoResponse**: ข้อมูลของสัญลักษณ์
    """
    response = service.get_symbol_info(symbol=request.symbol)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/last-tick", response_model=LastTickResponse)
async def get_last_tick(request: LastTickRequest, service: MT5MarketService = Depends(get_market_service)):
    """
    รับข้อมูลเทิกล่าสุด
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    
    Returns:
    - **LastTickResponse**: ข้อมูลเทิกล่าสุด
    """
    response = service.get_last_tick(symbol=request.symbol)
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/copy-rates", response_model=CopyRatesResponse)
async def copy_rates(request: CopyRatesRequest, service: MT5MarketService = Depends(get_market_service)):
    """
    รับข้อมูลอัตราแลกเปลี่ยน (OHLC)
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **timeframe**: กรอบเวลา (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
    - **from_date**: วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD HH:MM:SS)
    - **to_date**: วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD HH:MM:SS)
    - **count**: จำนวนแท่งที่ต้องการ
    
    Returns:
    - **CopyRatesResponse**: ข้อมูลอัตราแลกเปลี่ยน (OHLC)
    """
    # ตรวจสอบว่าระบุ count หรือ from_date/to_date
    if request.count is None and (request.from_date is None or request.to_date is None):
        raise HTTPException(status_code=400, detail="ต้องระบุ count หรือ from_date/to_date")
    
    response = None
    if request.count is not None:
        # ใช้ count
        response = service.copy_rates_from_pos(
            symbol=request.symbol,
            timeframe=request.timeframe,
            count=request.count
        )
    else:
        # ใช้ from_date/to_date
        response = service.copy_rates_range(
            symbol=request.symbol,
            timeframe=request.timeframe,
            from_date=request.from_date,
            to_date=request.to_date
        )
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/copy-ticks", response_model=CopyTicksResponse)
async def copy_ticks(request: CopyTicksRequest, service: MT5MarketService = Depends(get_market_service)):
    """
    รับข้อมูลเทิก
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **from_date**: วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD HH:MM:SS)
    - **to_date**: วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD HH:MM:SS)
    - **flags**: ประเภทเทิก (ALL, INFO, TRADE, BUY, SELL, LAST) ค่าเริ่มต้น ALL
    
    Returns:
    - **CopyTicksResponse**: ข้อมูลเทิก
    """
    response = service.copy_ticks_range(
        symbol=request.symbol,
        from_date=request.from_date,
        to_date=request.to_date,
        flags=request.flags
    )
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response
