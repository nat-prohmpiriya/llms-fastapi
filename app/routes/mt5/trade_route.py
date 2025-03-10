from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from schema.mt5.trade_models import (
    OrderRequest, OrderResponse,
    ModifyOrderRequest, CancelOrderRequest,
    CloseOrderRequest, CloseAllRequest,
    TrailingStopRequest
)
from services.mt5_trade_service import MT5TradeService

router = APIRouter(
    prefix="/api/v1/mt5/trade",
    tags=["MT5 Trade Operations"]
)

# สร้าง instance ของ MT5TradeService
def get_trade_service():
    return MT5TradeService()

@router.post("/open", response_model=OrderResponse)
async def open_order(request: OrderRequest, service: MT5TradeService = Depends(get_trade_service)):
    """
    เปิดออเดอร์ใหม่
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (เช่น "EURUSD")
    - **order_type**: ประเภทออเดอร์ (BUY, SELL, BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP, BUY_STOP_LIMIT, SELL_STOP_LIMIT)
    - **volume**: ปริมาณ (เช่น 0.1)
    - **price**: ราคา (จำเป็นสำหรับออเดอร์ลิมิตและสต็อป)
    - **sl**: ราคา Stop Loss (ถ้ามี)
    - **tp**: ราคา Take Profit (ถ้ามี)
    - **deviation**: ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)
    - **magic**: หมายเลข Magic
    - **comment**: ความคิดเห็น
    - **type_filling**: ประเภทการเติมเต็มออเดอร์ (FOK, IOC, RETURN)
    - **type_time**: ประเภทเวลาออเดอร์ (GTC, DAY, SPECIFIED, SPECIFIED_DAY)
    - **expiration**: เวลาหมดอายุ (สำหรับ SPECIFIED และ SPECIFIED_DAY)
    
    Returns:
    - **OrderResponse**: ผลลัพธ์ของการเปิดออเดอร์
    """
    success, message, result = service.open_order(
        symbol=request.symbol,
        order_type=request.order_type,
        volume=request.volume,
        price=request.price,
        sl=request.sl,
        tp=request.tp,
        deviation=request.deviation,
        magic=request.magic,
        comment=request.comment,
        type_filling=request.type_filling,
        type_time=request.type_time,
        expiration=request.expiration
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return OrderResponse(
        success=success,
        message=message,
        ticket=result.get("ticket") if result else None,
        volume=result.get("volume") if result else None,
        price=result.get("price") if result else None,
        comment=result.get("comment") if result else None,
        request_id=result.get("request_id") if result else None,
        retcode=result.get("retcode") if result else None,
        retcode_description=result.get("retcode_description") if result else None
    )

@router.post("/close", response_model=OrderResponse)
async def close_order(request: CloseOrderRequest, service: MT5TradeService = Depends(get_trade_service)):
    """
    ปิดออเดอร์
    
    Parameters:
    - **ticket**: หมายเลขตำแหน่ง
    - **volume**: ปริมาณที่ต้องการปิด (ถ้าไม่ระบุจะปิดทั้งหมด)
    - **deviation**: ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)
    - **comment**: ความคิดเห็น
    
    Returns:
    - **OrderResponse**: ผลลัพธ์ของการปิดออเดอร์
    """
    success, message, result = service.close_order(
        ticket=request.ticket,
        volume=request.volume,
        deviation=request.deviation,
        comment=request.comment
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return OrderResponse(
        success=success,
        message=message,
        ticket=result.get("ticket") if result else None,
        volume=result.get("volume") if result else None,
        price=result.get("price") if result else None,
        comment=result.get("comment") if result else None,
        request_id=result.get("request_id") if result else None,
        retcode=result.get("retcode") if result else None,
        retcode_description=result.get("retcode_description") if result else None
    )

@router.post("/modify", response_model=OrderResponse)
async def modify_order(request: ModifyOrderRequest, service: MT5TradeService = Depends(get_trade_service)):
    """
    แก้ไขออเดอร์
    
    Parameters:
    - **ticket**: หมายเลขตำแหน่งหรือออเดอร์
    - **price**: ราคาใหม่
    - **sl**: ราคา Stop Loss ใหม่
    - **tp**: ราคา Take Profit ใหม่
    - **deviation**: ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)
    - **type_time**: ประเภทเวลาออเดอร์ใหม่
    - **expiration**: เวลาหมดอายุใหม่
    - **comment**: ความคิดเห็นใหม่
    
    Returns:
    - **OrderResponse**: ผลลัพธ์ของการแก้ไขออเดอร์
    """
    success, message, result = service.modify_order(
        ticket=request.ticket,
        price=request.price,
        sl=request.sl,
        tp=request.tp,
        deviation=request.deviation,
        type_time=request.type_time,
        expiration=request.expiration,
        comment=request.comment
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return OrderResponse(
        success=success,
        message=message,
        ticket=request.ticket,
        retcode=result.get("retcode") if result else None,
        retcode_description=result.get("retcode_description") if result else None
    )

@router.post("/cancel", response_model=OrderResponse)
async def cancel_order(request: CancelOrderRequest, service: MT5TradeService = Depends(get_trade_service)):
    """
    ยกเลิกออเดอร์ที่รอดำเนินการ
    
    Parameters:
    - **ticket**: หมายเลขออเดอร์
    
    Returns:
    - **OrderResponse**: ผลลัพธ์ของการยกเลิกออเดอร์
    """
    success, message, result = service.cancel_order(
        ticket=request.ticket
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return OrderResponse(
        success=success,
        message=message,
        ticket=request.ticket,
        retcode=result.get("retcode") if result else None,
        retcode_description=result.get("retcode_description") if result else None
    )

@router.post("/close-all", response_model=OrderResponse)
async def close_all(request: CloseAllRequest, service: MT5TradeService = Depends(get_trade_service)):
    """
    ปิดออเดอร์ทั้งหมด
    
    Parameters:
    - **symbol**: ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะปิดทั้งหมด)
    - **magic**: หมายเลข Magic (ถ้าไม่ระบุจะปิดทั้งหมด)
    - **comment**: ความคิดเห็น
    
    Returns:
    - **OrderResponse**: ผลลัพธ์ของการปิดออเดอร์ทั้งหมด
    """
    success, message, result = service.close_all(
        symbol=request.symbol,
        magic=request.magic,
        comment=request.comment
    )
    
    return OrderResponse(
        success=success,
        message=message,
        success_count=result.get("success") if result else 0,
        failed_count=result.get("failed") if result else 0,
        total_count=result.get("total") if result else 0
    )

@router.post("/trailing-stop", response_model=OrderResponse)
async def set_trailing_stop(request: TrailingStopRequest, service: MT5TradeService = Depends(get_trade_service)):
    """
    ตั้งค่า Trailing Stop
    
    Parameters:
    - **ticket**: หมายเลขตำแหน่ง
    - **distance**: ระยะห่างของ Trailing Stop (ในจุด)
    - **step**: ขั้นตอนการเปลี่ยนแปลง (ในจุด)
    
    Returns:
    - **OrderResponse**: ผลลัพธ์ของการตั้งค่า Trailing Stop
    """
    success, message = service.set_trailing_stop(
        ticket=request.ticket,
        distance=request.distance,
        step=request.step
    )
    
    return OrderResponse(
        success=success,
        message=message
    )
