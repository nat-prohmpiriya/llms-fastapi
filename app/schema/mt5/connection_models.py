from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class MT5ConnectionRequest(BaseModel):
    """
    คลาสสำหรับรับข้อมูลการเชื่อมต่อกับ MT5
    """
    server: str = Field(..., description="ชื่อเซิร์ฟเวอร์ MT5")
    login: int = Field(..., description="หมายเลขบัญชี (login)")
    password: str = Field(..., description="รหัสผ่าน")
    timeout: Optional[int] = Field(60000, description="ระยะเวลาหมดเวลาในการเชื่อมต่อ (มิลลิวินาที)")
    path: Optional[str] = Field(None, description="พาธไปยังโฟลเดอร์ติดตั้ง MetaTrader 5 (ถ้าไม่ระบุจะใช้ค่าเริ่มต้น)")

class MT5ConnectionResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลผลลัพธ์การเชื่อมต่อกับ MT5
    """
    connected: bool = Field(..., description="สถานะการเชื่อมต่อ")
    message: str = Field(..., description="ข้อความแสดงผลลัพธ์")
    account_info: Optional[Dict[str, Any]] = Field(None, description="ข้อมูลบัญชี (ถ้าเชื่อมต่อสำเร็จ)")

class MT5StatusResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลสถานะการเชื่อมต่อกับ MT5
    """
    connected: bool = Field(..., description="สถานะการเชื่อมต่อ")
    message: str = Field(..., description="ข้อความแสดงผลลัพธ์")
    terminal_info: Optional[Dict[str, Any]] = Field(None, description="ข้อมูลเทอร์มินัล (ถ้าเชื่อมต่ออยู่)")

class MT5DisconnectResponse(BaseModel):
    """
    คลาสสำหรับส่งข้อมูลผลลัพธ์การปิดการเชื่อมต่อกับ MT5
    """
    success: bool = Field(..., description="สถานะการปิดการเชื่อมต่อ")
    message: str = Field(..., description="ข้อความแสดงผลลัพธ์")
