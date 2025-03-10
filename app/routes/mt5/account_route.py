from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from schema.mt5.account_models import (
    AccountInfoRequest, AccountInfoResponse, 
    HistoryOrdersRequest, HistoryOrdersResponse,
    HistoryDealsRequest, HistoryDealsResponse,
    PositionsRequest, PositionsResponse,
    OrdersRequest, OrdersResponse
)
from services.mt5_account_service import MT5AccountService

router = APIRouter(
    prefix="/api/v1/mt5/account",
    tags=["MT5 Account Information"]
)

# สร้าง instance ของ MT5AccountService
def get_account_service():
    return MT5AccountService()

@router.post("/info", response_model=AccountInfoResponse)
async def get_account_info(request: AccountInfoRequest, service: MT5AccountService = Depends(get_account_service)):
    """
    รับข้อมูลบัญชี MT5
    
    Returns:
    - **AccountInfoResponse**: ข้อมูลบัญชี เช่น เงินคงเหลือ, กำไร, ส่วนต่าง, ชื่อเซิร์ฟเวอร์, เลเวอเรจ, ฯลฯ
    """
    response = service.get_account_info()
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/positions", response_model=PositionsResponse)
async def get_positions(request: PositionsRequest, service: MT5AccountService = Depends(get_account_service)):
    """
    รับข้อมูลตำแหน่งที่เปิดอยู่
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **ticket**: หมายเลขตำแหน่ง (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **magic**: หมายเลข Magic (ถ้าไม่ระบุจะดึงทั้งหมด)
    
    Returns:
    - **PositionsResponse**: รายการตำแหน่งที่เปิดอยู่
    """
    response = service.get_positions(
        symbol=request.symbol,
        ticket=request.ticket,
        magic=request.magic
    )
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/orders", response_model=OrdersResponse)
async def get_orders(request: OrdersRequest, service: MT5AccountService = Depends(get_account_service)):
    """
    รับข้อมูลออเดอร์ที่รอดำเนินการ
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **ticket**: หมายเลขออเดอร์ (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **magic**: หมายเลข Magic (ถ้าไม่ระบุจะดึงทั้งหมด)
    
    Returns:
    - **OrdersResponse**: รายการออเดอร์ที่รอดำเนินการ
    """
    response = service.get_orders(
        symbol=request.symbol,
        ticket=request.ticket,
        magic=request.magic
    )
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/history-orders", response_model=HistoryOrdersResponse)
async def get_history_orders(request: HistoryOrdersRequest, service: MT5AccountService = Depends(get_account_service)):
    """
    รับข้อมูลออเดอร์ในประวัติ
    
    Parameters:
    - **from_date**: วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)
    - **to_date**: วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD) ถ้าไม่ระบุจะใช้วันปัจจุบัน
    - **symbol**: ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **ticket**: หมายเลขออเดอร์ (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **position**: หมายเลขตำแหน่ง (ถ้าไม่ระบุจะดึงทั้งหมด)
    
    Returns:
    - **HistoryOrdersResponse**: รายการประวัติออเดอร์
    """
    response = service.get_history_orders(
        from_date=request.from_date,
        to_date=request.to_date,
        symbol=request.symbol,
        ticket=request.ticket,
        position=request.position
    )
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response

@router.post("/history-deals", response_model=HistoryDealsResponse)
async def get_history_deals(request: HistoryDealsRequest, service: MT5AccountService = Depends(get_account_service)):
    """
    รับข้อมูลการซื้อขายในประวัติ
    
    Parameters:
    - **from_date**: วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)
    - **to_date**: วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD) ถ้าไม่ระบุจะใช้วันปัจจุบัน
    - **symbol**: ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **ticket**: หมายเลขการซื้อขาย (ถ้าไม่ระบุจะดึงทั้งหมด)
    - **position**: หมายเลขตำแหน่ง (ถ้าไม่ระบุจะดึงทั้งหมด)
    
    Returns:
    - **HistoryDealsResponse**: รายการประวัติการซื้อขาย
    """
    response = service.get_history_deals(
        from_date=request.from_date,
        to_date=request.to_date,
        symbol=request.symbol,
        ticket=request.ticket,
        position=request.position
    )
    
    if not response.success:
        raise HTTPException(status_code=400, detail=response.message)
    
    return response
