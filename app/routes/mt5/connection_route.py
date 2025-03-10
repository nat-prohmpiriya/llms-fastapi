from fastapi import APIRouter, Depends, HTTPException
from schema.mt5.connection_models import MT5ConnectionRequest, MT5ConnectionResponse, MT5StatusResponse, MT5DisconnectResponse
from services.mt5_service import MT5Service

router = APIRouter(
    prefix="/api/v1/mt5/connection",
    tags=["MT5 Connection"]
)

@router.post("/connect", response_model=MT5ConnectionResponse)
async def connect_to_mt5(request: MT5ConnectionRequest):
    """
    เชื่อมต่อกับเทอร์มินัล MT5
    
    Args:
        request: ข้อมูลการเชื่อมต่อกับ MT5
        
    Returns:
        MT5ConnectionResponse: ผลลัพธ์การเชื่อมต่อ
    """
    try:
        mt5_service = MT5Service()
        connected, message, account_info = mt5_service.connect(
            server=request.server,
            login=request.login,
            password=request.password,
            timeout=request.timeout,
            path=request.path
        )
        
        return MT5ConnectionResponse(
            connected=connected,
            message=message,
            account_info=account_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=MT5StatusResponse)
async def get_mt5_status():
    """
    ตรวจสอบสถานะการเชื่อมต่อกับ MT5
    
    Returns:
        MT5StatusResponse: สถานะการเชื่อมต่อ
    """
    try:
        mt5_service = MT5Service()
        connected, message, terminal_info = mt5_service.get_status()
        
        return MT5StatusResponse(
            connected=connected,
            message=message,
            terminal_info=terminal_info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/disconnect", response_model=MT5DisconnectResponse)
async def disconnect_from_mt5():
    """
    ปิดการเชื่อมต่อกับ MT5
    
    Returns:
        MT5DisconnectResponse: ผลลัพธ์การปิดการเชื่อมต่อ
    """
    try:
        mt5_service = MT5Service()
        success, message = mt5_service.disconnect()
        
        return MT5DisconnectResponse(
            success=success,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
