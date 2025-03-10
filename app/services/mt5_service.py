import MetaTrader5 as mt5
from typing import Dict, Any, Optional, Tuple
import time

class MT5Service:
    """
    บริการสำหรับเชื่อมต่อและจัดการกับ MetaTrader 5
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        สร้างอินสแตนซ์เดียวของ MT5Service (Singleton pattern)
        """
        if cls._instance is None:
            cls._instance = super(MT5Service, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        เริ่มต้นบริการ MT5
        """
        if not MT5Service._initialized:
            self._connected = False
            MT5Service._initialized = True
    
    def connect(self, server: str, login: int, password: str, timeout: int = 60000, path: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        เชื่อมต่อกับเทอร์มินัล MT5
        
        Args:
            server: ชื่อเซิร์ฟเวอร์ MT5
            login: หมายเลขบัญชี (login)
            password: รหัสผ่าน
            timeout: ระยะเวลาหมดเวลาในการเชื่อมต่อ (มิลลิวินาที)
            path: พาธไปยังโฟลเดอร์ติดตั้ง MetaTrader 5 (ถ้าไม่ระบุจะใช้ค่าเริ่มต้น)
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการเชื่อมต่อ, ข้อความ, ข้อมูลบัญชี (ถ้าเชื่อมต่อสำเร็จ)
        """
        # ปิดการเชื่อมต่อที่มีอยู่ก่อน (ถ้ามี)
        if self._connected:
            mt5.shutdown()
            self._connected = False
        
        # เริ่มต้น MT5
        init_result = mt5.initialize(path=path, login=login, password=password, server=server, timeout=timeout)
        
        if not init_result:
            error = mt5.last_error()
            return False, f"การเชื่อมต่อล้มเหลว: {error}", None
        
        # ตรวจสอบการเชื่อมต่อ
        if not mt5.terminal_info():
            error = mt5.last_error()
            return False, f"การเชื่อมต่อล้มเหลว: {error}", None
        
        # ตรวจสอบการอนุญาต
        if not mt5.login(login, password, server, timeout):
            error = mt5.last_error()
            mt5.shutdown()
            return False, f"การเข้าสู่ระบบล้มเหลว: {error}", None
        
        # ดึงข้อมูลบัญชี
        account_info = mt5.account_info()
        if not account_info:
            error = mt5.last_error()
            mt5.shutdown()
            return False, f"ไม่สามารถดึงข้อมูลบัญชีได้: {error}", None
        
        # แปลงข้อมูลบัญชีเป็นรูปแบบ dict
        account_dict = self._convert_to_dict(account_info)
        
        self._connected = True
        return True, "เชื่อมต่อสำเร็จ", account_dict
    
    def get_status(self) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        ตรวจสอบสถานะการเชื่อมต่อกับ MT5
        
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการเชื่อมต่อ, ข้อความ, ข้อมูลเทอร์มินัล (ถ้าเชื่อมต่ออยู่)
        """
        if not self._connected:
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        # ตรวจสอบการเชื่อมต่อ
        terminal_info = mt5.terminal_info()
        if not terminal_info:
            error = mt5.last_error()
            self._connected = False
            return False, f"การเชื่อมต่อถูกตัดขาด: {error}", None
        
        # แปลงข้อมูลเทอร์มินัลเป็นรูปแบบ dict
        terminal_dict = self._convert_to_dict(terminal_info)
        
        return True, "เชื่อมต่ออยู่", terminal_dict
    
    def disconnect(self) -> Tuple[bool, str]:
        """
        ปิดการเชื่อมต่อกับ MT5
        
        Returns:
            Tuple[bool, str]: สถานะการปิดการเชื่อมต่อ, ข้อความ
        """
        if not self._connected:
            return True, "ไม่ได้เชื่อมต่อกับ MT5 อยู่แล้ว"
        
        # ปิดการเชื่อมต่อ
        shutdown_result = mt5.shutdown()
        
        if shutdown_result:
            self._connected = False
            return True, "ปิดการเชื่อมต่อสำเร็จ"
        else:
            error = mt5.last_error()
            return False, f"ปิดการเชื่อมต่อล้มเหลว: {error}"
    
    def _convert_to_dict(self, named_tuple) -> Dict[str, Any]:
        """
        แปลง named tuple เป็น dict
        
        Args:
            named_tuple: named tuple ที่ต้องการแปลง
            
        Returns:
            Dict[str, Any]: dict ที่แปลงแล้ว
        """
        return {key: getattr(named_tuple, key) for key in dir(named_tuple) if not key.startswith('_')}
    
    def is_connected(self) -> bool:
        """
        ตรวจสอบว่ากำลังเชื่อมต่อกับ MT5 อยู่หรือไม่
        
        Returns:
            bool: True ถ้ากำลังเชื่อมต่ออยู่, False ถ้าไม่ได้เชื่อมต่อ
        """
        return self._connected
