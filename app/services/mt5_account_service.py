import MetaTrader5 as mt5
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import time
from services.mt5_service import MT5Service

class MT5AccountService:
    """
    บริการสำหรับจัดการข้อมูลบัญชีใน MetaTrader 5
    """
    
    def __init__(self):
        """
        เริ่มต้นบริการ MT5AccountService
        """
        self.mt5_service = MT5Service()
    
    def get_account_info(self) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        ดึงข้อมูลบัญชี
        
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการดึงข้อมูล, ข้อความ, ข้อมูลบัญชี
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        account_info = mt5.account_info()
        if not account_info:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลบัญชีได้: {error}", None
        
        # แปลงข้อมูลบัญชีเป็นรูปแบบ dict
        account_dict = self._convert_to_dict(account_info)
        
        return True, "ดึงข้อมูลบัญชีสำเร็จ", account_dict
    
    def get_positions(self) -> Tuple[bool, str, Optional[List[Dict[str, Any]]], int]:
        """
        ดึงข้อมูลตำแหน่งที่เปิดอยู่
        
        Returns:
            Tuple[bool, str, Optional[List[Dict[str, Any]]], int]: สถานะการดึงข้อมูล, ข้อความ, รายการตำแหน่ง, จำนวนตำแหน่งทั้งหมด
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None, 0
        
        positions = mt5.positions_get()
        if positions is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลตำแหน่งได้: {error}", None, 0
        
        # แปลงข้อมูลตำแหน่งเป็นรูปแบบ dict
        positions_list = []
        for position in positions:
            position_dict = self._convert_to_dict(position)
            # เพิ่มคำอธิบายประเภทตำแหน่ง
            position_dict["type_description"] = "Buy" if position_dict["type"] == 0 else "Sell"
            positions_list.append(position_dict)
        
        return True, "ดึงข้อมูลตำแหน่งสำเร็จ", positions_list, len(positions_list)
    
    def get_history_orders(self, from_date: datetime, to_date: Optional[datetime] = None, group: Optional[str] = None) -> Tuple[bool, str, Optional[List[Dict[str, Any]]], int]:
        """
        ดึงข้อมูลประวัติออเดอร์
        
        Args:
            from_date: วันที่เริ่มต้น
            to_date: วันที่สิ้นสุด (ถ้าไม่ระบุจะใช้วันที่ปัจจุบัน)
            group: กลุ่มสัญลักษณ์ เช่น '*' สำหรับทั้งหมด หรือ 'EUR*' สำหรับคู่สกุลเงินที่ขึ้นต้นด้วย EUR
            
        Returns:
            Tuple[bool, str, Optional[List[Dict[str, Any]]], int]: สถานะการดึงข้อมูล, ข้อความ, รายการประวัติออเดอร์, จำนวนออเดอร์ทั้งหมด
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None, 0
        
        # แปลงวันที่เป็น timestamp
        from_timestamp = int(from_date.timestamp())
        to_timestamp = int(to_date.timestamp()) if to_date else int(time.time())
        
        # ดึงข้อมูลประวัติออเดอร์
        history_orders = mt5.history_orders_get(from_timestamp, to_timestamp, group=group)
        if history_orders is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลประวัติออเดอร์ได้: {error}", None, 0
        
        # แปลงข้อมูลประวัติออเดอร์เป็นรูปแบบ dict
        orders_list = []
        for order in history_orders:
            order_dict = self._convert_to_dict(order)
            # เพิ่มคำอธิบายประเภทและสถานะออเดอร์
            order_dict["type_description"] = self._get_order_type_description(order_dict["type"])
            order_dict["state_description"] = self._get_order_state_description(order_dict["state"])
            orders_list.append(order_dict)
        
        return True, "ดึงข้อมูลประวัติออเดอร์สำเร็จ", orders_list, len(orders_list)
    
    def get_history_deals(self, from_date: datetime, to_date: Optional[datetime] = None, group: Optional[str] = None) -> Tuple[bool, str, Optional[List[Dict[str, Any]]], int]:
        """
        ดึงข้อมูลประวัติดีล
        
        Args:
            from_date: วันที่เริ่มต้น
            to_date: วันที่สิ้นสุด (ถ้าไม่ระบุจะใช้วันที่ปัจจุบัน)
            group: กลุ่มสัญลักษณ์ เช่น '*' สำหรับทั้งหมด หรือ 'EUR*' สำหรับคู่สกุลเงินที่ขึ้นต้นด้วย EUR
            
        Returns:
            Tuple[bool, str, Optional[List[Dict[str, Any]]], int]: สถานะการดึงข้อมูล, ข้อความ, รายการประวัติดีล, จำนวนดีลทั้งหมด
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None, 0
        
        # แปลงวันที่เป็น timestamp
        from_timestamp = int(from_date.timestamp())
        to_timestamp = int(to_date.timestamp()) if to_date else int(time.time())
        
        # ดึงข้อมูลประวัติดีล
        history_deals = mt5.history_deals_get(from_timestamp, to_timestamp, group=group)
        if history_deals is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลประวัติดีลได้: {error}", None, 0
        
        # แปลงข้อมูลประวัติดีลเป็นรูปแบบ dict
        deals_list = []
        for deal in history_deals:
            deal_dict = self._convert_to_dict(deal)
            # เพิ่มคำอธิบายประเภทและทิศทางการเข้า
            deal_dict["type_description"] = self._get_deal_type_description(deal_dict["type"])
            deal_dict["entry_description"] = self._get_deal_entry_description(deal_dict["entry"])
            deals_list.append(deal_dict)
        
        return True, "ดึงข้อมูลประวัติดีลสำเร็จ", deals_list, len(deals_list)
    
    def _convert_to_dict(self, named_tuple) -> Dict[str, Any]:
        """
        แปลง named tuple เป็น dict
        
        Args:
            named_tuple: named tuple ที่ต้องการแปลง
            
        Returns:
            Dict[str, Any]: dict ที่แปลงแล้ว
        """
        return {key: getattr(named_tuple, key) for key in dir(named_tuple) if not key.startswith('_')}
    
    def _get_order_type_description(self, order_type: int) -> str:
        """
        แปลงรหัสประเภทออเดอร์เป็นคำอธิบาย
        
        Args:
            order_type: รหัสประเภทออเดอร์
            
        Returns:
            str: คำอธิบายประเภทออเดอร์
        """
        order_types = {
            0: "Buy",
            1: "Sell",
            2: "Buy Limit",
            3: "Sell Limit",
            4: "Buy Stop",
            5: "Sell Stop",
            6: "Buy Stop Limit",
            7: "Sell Stop Limit",
            8: "Close By"
        }
        return order_types.get(order_type, f"Unknown ({order_type})")
    
    def _get_order_state_description(self, order_state: int) -> str:
        """
        แปลงรหัสสถานะออเดอร์เป็นคำอธิบาย
        
        Args:
            order_state: รหัสสถานะออเดอร์
            
        Returns:
            str: คำอธิบายสถานะออเดอร์
        """
        order_states = {
            0: "Started",
            1: "Placed",
            2: "Canceled",
            3: "Partial",
            4: "Filled",
            5: "Rejected",
            6: "Expired",
            7: "Request Add",
            8: "Request Modify",
            9: "Request Cancel"
        }
        return order_states.get(order_state, f"Unknown ({order_state})")
    
    def _get_deal_type_description(self, deal_type: int) -> str:
        """
        แปลงรหัสประเภทดีลเป็นคำอธิบาย
        
        Args:
            deal_type: รหัสประเภทดีล
            
        Returns:
            str: คำอธิบายประเภทดีล
        """
        deal_types = {
            0: "Buy",
            1: "Sell",
            2: "Balance",
            3: "Credit",
            4: "Charge",
            5: "Correction",
            6: "Bonus",
            7: "Commission",
            8: "Commission Daily",
            9: "Commission Monthly",
            10: "Commission Agent Daily",
            11: "Commission Agent Monthly",
            12: "Interest",
            13: "Buy Canceled",
            14: "Sell Canceled",
            15: "Dividend",
            16: "Dividend Franked",
            17: "Tax"
        }
        return deal_types.get(deal_type, f"Unknown ({deal_type})")
    
    def _get_deal_entry_description(self, deal_entry: int) -> str:
        """
        แปลงรหัสทิศทางการเข้าเป็นคำอธิบาย
        
        Args:
            deal_entry: รหัสทิศทางการเข้า
            
        Returns:
            str: คำอธิบายทิศทางการเข้า
        """
        deal_entries = {
            0: "In",
            1: "Out",
            2: "InOut",
            3: "Out By"
        }
        return deal_entries.get(deal_entry, f"Unknown ({deal_entry})")
