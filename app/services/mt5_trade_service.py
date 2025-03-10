import MetaTrader5 as mt5
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import time
from services.mt5_service import MT5Service
from schema.mt5.trade_models import OrderType, OrderFilling, OrderTime

class MT5TradeService:
    """
    บริการสำหรับการซื้อขายใน MetaTrader 5
    """
    
    def __init__(self):
        """
        เริ่มต้นบริการ MT5TradeService
        """
        self.mt5_service = MT5Service()
    
    def open_order(self, symbol: str, order_type: OrderType, volume: float, price: Optional[float] = None,
                  sl: Optional[float] = None, tp: Optional[float] = None, deviation: int = 10,
                  magic: int = 0, comment: Optional[str] = None, type_filling: OrderFilling = OrderFilling.FOK,
                  type_time: OrderTime = OrderTime.GTC, expiration: Optional[int] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        เปิดออเดอร์
        
        Args:
            symbol: ชื่อสัญลักษณ์
            order_type: ประเภทออเดอร์
            volume: ปริมาณ
            price: ราคา (จำเป็นสำหรับออเดอร์ลิมิตและสต็อป)
            sl: ราคา Stop Loss
            tp: ราคา Take Profit
            deviation: ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)
            magic: หมายเลข Magic
            comment: ความคิดเห็น
            type_filling: ประเภทการเติมเต็มออเดอร์
            type_time: ประเภทเวลาออเดอร์
            expiration: เวลาหมดอายุ (สำหรับ SPECIFIED และ SPECIFIED_DAY)
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการเปิดออเดอร์, ข้อความ, ข้อมูลออเดอร์
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        # ตรวจสอบว่าต้องระบุราคาหรือไม่
        if order_type in [OrderType.BUY_LIMIT, OrderType.SELL_LIMIT, OrderType.BUY_STOP, OrderType.SELL_STOP,
                         OrderType.BUY_STOP_LIMIT, OrderType.SELL_STOP_LIMIT] and price is None:
            return False, "ต้องระบุราคาสำหรับออเดอร์ประเภทนี้", None
        
        # ตรวจสอบว่าสัญลักษณ์มีอยู่หรือไม่
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return False, f"ไม่พบสัญลักษณ์ {symbol}", None
        
        # ตรวจสอบว่าสัญลักษณ์เปิดให้ซื้อขายหรือไม่
        if not symbol_info.visible:
            # เพิ่มสัญลักษณ์ไปยังรายการ
            if not mt5.symbol_select(symbol, True):
                return False, f"ไม่สามารถเลือกสัญลักษณ์ {symbol}", None
        
        # กำหนดการกระทำ
        action = mt5.TRADE_ACTION_DEAL
        if order_type in [OrderType.BUY_LIMIT, OrderType.SELL_LIMIT, OrderType.BUY_STOP, OrderType.SELL_STOP]:
            action = mt5.TRADE_ACTION_PENDING
        elif order_type in [OrderType.BUY_STOP_LIMIT, OrderType.SELL_STOP_LIMIT]:
            action = mt5.TRADE_ACTION_PENDING
        
        # กำหนดชนิด
        order_type_value = int(order_type)
        
        # สร้างคำขอ
        request = {
            "action": action,
            "symbol": symbol,
            "volume": volume,
            "type": order_type_value,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_filling": int(type_filling),
            "type_time": int(type_time)
        }
        
        # เพิ่มพารามิเตอร์ตามประเภทออเดอร์
        if price is not None:
            request["price"] = price
        
        if sl is not None:
            request["sl"] = sl
        
        if tp is not None:
            request["tp"] = tp
        
        if expiration is not None and type_time in [OrderTime.SPECIFIED, OrderTime.SPECIFIED_DAY]:
            request["expiration"] = expiration
        
        # ส่งคำขอ
        result = mt5.order_send(request)
        if result is None:
            error = mt5.last_error()
            return False, f"การเปิดออเดอร์ล้มเหลว: {error}", None
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return False, f"การเปิดออเดอร์ล้มเหลว: {result.retcode} ({self._get_retcode_description(result.retcode)})", None
        
        # สร้าง dict ผลลัพธ์
        result_dict = {
            "ticket": result.order,
            "volume": result.volume,
            "price": result.price,
            "bid": result.bid,
            "ask": result.ask,
            "comment": result.comment,
            "request_id": result.request_id,
            "retcode": result.retcode,
            "retcode_description": self._get_retcode_description(result.retcode)
        }
        
        return True, "เปิดออเดอร์สำเร็จ", result_dict
    
    def close_order(self, ticket: int, volume: Optional[float] = None, deviation: int = 10, comment: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        ปิดออเดอร์
        
        Args:
            ticket: หมายเลขตำแหน่ง
            volume: ปริมาณที่ต้องการปิด (ถ้าไม่ระบุจะปิดทั้งหมด)
            deviation: ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)
            comment: ความคิดเห็น
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการปิดออเดอร์, ข้อความ, ข้อมูลผลลัพธ์
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        # ตรวจสอบว่าตำแหน่งมีอยู่หรือไม่
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            error = mt5.last_error()
            return False, f"ไม่พบตำแหน่ง {ticket}: {error}", None
        
        # ดึงข้อมูลตำแหน่ง
        position_data = position[0]
        
        # กำหนดปริมาณที่จะปิด
        close_volume = volume if volume is not None else position_data.volume
        
        # กำหนดประเภทการซื้อขายตรงข้าม
        close_type = mt5.ORDER_TYPE_SELL if position_data.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        
        # สร้างคำขอ
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position_data.symbol,
            "volume": close_volume,
            "type": close_type,
            "position": ticket,
            "deviation": deviation,
            "magic": position_data.magic,
            "comment": comment,
            "type_filling": mt5.ORDER_FILLING_FOK
        }
        
        # ส่งคำขอ
        result = mt5.order_send(request)
        if result is None:
            error = mt5.last_error()
            return False, f"การปิดออเดอร์ล้มเหลว: {error}", None
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return False, f"การปิดออเดอร์ล้มเหลว: {result.retcode} ({self._get_retcode_description(result.retcode)})", None
        
        # สร้าง dict ผลลัพธ์
        result_dict = {
            "ticket": result.order,
            "volume": result.volume,
            "price": result.price,
            "bid": result.bid,
            "ask": result.ask,
            "comment": result.comment,
            "request_id": result.request_id,
            "retcode": result.retcode,
            "retcode_description": self._get_retcode_description(result.retcode)
        }
        
        return True, "ปิดออเดอร์สำเร็จ", result_dict
    
    def modify_order(self, ticket: int, price: Optional[float] = None, sl: Optional[float] = None, tp: Optional[float] = None,
                    deviation: int = 10, type_time: Optional[OrderTime] = None, expiration: Optional[int] = None,
                    comment: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        แก้ไขออเดอร์
        
        Args:
            ticket: หมายเลขตำแหน่งหรือออเดอร์
            price: ราคาใหม่
            sl: ราคา Stop Loss ใหม่
            tp: ราคา Take Profit ใหม่
            deviation: ความเบี่ยงเบนสูงสุดจากราคาที่ร้องขอ (ในจุด)
            type_time: ประเภทเวลาออเดอร์ใหม่
            expiration: เวลาหมดอายุใหม่
            comment: ความคิดเห็นใหม่
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการแก้ไขออเดอร์, ข้อความ, ข้อมูลผลลัพธ์
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        # ตรวจสอบว่าเป็นตำแหน่งหรือออเดอร์ที่รอดำเนินการ
        position = mt5.positions_get(ticket=ticket)
        pending_order = mt5.orders_get(ticket=ticket)
        
        is_position = position is not None and len(position) > 0
        is_pending = pending_order is not None and len(pending_order) > 0
        
        if not is_position and not is_pending:
            return False, f"ไม่พบตำแหน่งหรือออเดอร์ {ticket}", None
        
        # สร้างคำขอตามประเภท
        if is_position:
            # แก้ไขตำแหน่ง (เฉพาะ SL/TP)
            position_data = position[0]
            
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": position_data.symbol,
                "position": ticket
            }
            
            if sl is not None:
                request["sl"] = sl
            else:
                request["sl"] = position_data.sl
                
            if tp is not None:
                request["tp"] = tp
            else:
                request["tp"] = position_data.tp
                
        else:
            # แก้ไขออเดอร์ที่รอดำเนินการ
            order_data = pending_order[0]
            
            request = {
                "action": mt5.TRADE_ACTION_MODIFY,
                "order": ticket,
                "symbol": order_data.symbol
            }
            
            if price is not None:
                request["price"] = price
            else:
                request["price"] = order_data.price_open
                
            if sl is not None:
                request["sl"] = sl
            else:
                request["sl"] = order_data.sl
                
            if tp is not None:
                request["tp"] = tp
            else:
                request["tp"] = order_data.tp
                
            if type_time is not None:
                request["type_time"] = int(type_time)
                
            if expiration is not None:
                request["expiration"] = expiration
                
            if comment is not None:
                request["comment"] = comment
        
        # ส่งคำขอ
        result = mt5.order_send(request)
        if result is None:
            error = mt5.last_error()
            return False, f"การแก้ไขออเดอร์ล้มเหลว: {error}", None
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return False, f"การแก้ไขออเดอร์ล้มเหลว: {result.retcode} ({self._get_retcode_description(result.retcode)})", None
        
        return True, "แก้ไขออเดอร์สำเร็จ", {"retcode": result.retcode, "retcode_description": self._get_retcode_description(result.retcode)}
    
    def cancel_order(self, ticket: int) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        ยกเลิกออเดอร์ที่รอดำเนินการ
        
        Args:
            ticket: หมายเลขออเดอร์
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการยกเลิกออเดอร์, ข้อความ, ข้อมูลผลลัพธ์
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        # ตรวจสอบว่าออเดอร์มีอยู่หรือไม่
        pending_order = mt5.orders_get(ticket=ticket)
        if pending_order is None or len(pending_order) == 0:
            error = mt5.last_error()
            return False, f"ไม่พบออเดอร์ {ticket}: {error}", None
        
        # สร้างคำขอ
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket
        }
        
        # ส่งคำขอ
        result = mt5.order_send(request)
        if result is None:
            error = mt5.last_error()
            return False, f"การยกเลิกออเดอร์ล้มเหลว: {error}", None
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return False, f"การยกเลิกออเดอร์ล้มเหลว: {result.retcode} ({self._get_retcode_description(result.retcode)})", None
        
        return True, "ยกเลิกออเดอร์สำเร็จ", {"retcode": result.retcode, "retcode_description": self._get_retcode_description(result.retcode)}
    
    def close_all(self, symbol: Optional[str] = None, magic: Optional[int] = None, comment: Optional[str] = None) -> Tuple[bool, str, Dict[str, Any]]:
        """
        ปิดออเดอร์ทั้งหมด
        
        Args:
            symbol: ชื่อสัญลักษณ์ (ถ้าไม่ระบุจะปิดทั้งหมด)
            magic: หมายเลข Magic (ถ้าไม่ระบุจะปิดทั้งหมด)
            comment: ความคิดเห็น
            
        Returns:
            Tuple[bool, str, Dict[str, Any]]: สถานะการปิดออเดอร์, ข้อความ, ข้อมูลผลลัพธ์
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", {"success": 0, "failed": 0, "total": 0}
        
        # ดึงตำแหน่งที่เปิดอยู่
        positions = None
        if symbol is not None and magic is not None:
            positions = mt5.positions_get(symbol=symbol, magic=magic)
        elif symbol is not None:
            positions = mt5.positions_get(symbol=symbol)
        elif magic is not None:
            positions = mt5.positions_get(magic=magic)
        else:
            positions = mt5.positions_get()
        
        if positions is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลตำแหน่งได้: {error}", {"success": 0, "failed": 0, "total": 0}
        
        if len(positions) == 0:
            return True, "ไม่มีตำแหน่งที่ต้องปิด", {"success": 0, "failed": 0, "total": 0}
        
        # ปิดตำแหน่งทั้งหมด
        success_count = 0
        failed_count = 0
        
        for position in positions:
            success, _, _ = self.close_order(position.ticket, comment=comment)
            if success:
                success_count += 1
            else:
                failed_count += 1
        
        total_count = success_count + failed_count
        
        if failed_count == 0:
            return True, f"ปิดตำแหน่งทั้งหมด {success_count} ตำแหน่งสำเร็จ", {"success": success_count, "failed": failed_count, "total": total_count}
        else:
            return False, f"ปิดตำแหน่งสำเร็จ {success_count} ตำแหน่ง, ล้มเหลว {failed_count} ตำแหน่ง จากทั้งหมด {total_count} ตำแหน่ง", {"success": success_count, "failed": failed_count, "total": total_count}
    
    def set_trailing_stop(self, ticket: int, distance: int, step: int = 1) -> Tuple[bool, str]:
        """
        ตั้งค่า Trailing Stop
        
        Args:
            ticket: หมายเลขตำแหน่ง
            distance: ระยะห่างของ Trailing Stop (ในจุด)
            step: ขั้นตอนการเปลี่ยนแปลง (ในจุด)
            
        Returns:
            Tuple[bool, str]: สถานะการตั้งค่า, ข้อความ
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5"
        
        # ตรวจสอบว่าตำแหน่งมีอยู่หรือไม่
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            error = mt5.last_error()
            return False, f"ไม่พบตำแหน่ง {ticket}: {error}"
        
        # ตั้งค่า Trailing Stop
        success = mt5.symbol_info_tick(position[0].symbol)
        if not success:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลราคาได้: {error}"
        
        # ใน MT5 Python API ไม่มีฟังก์ชัน Trailing Stop โดยตรง
        # ในการใช้งานจริงอาจต้องสร้างฟังก์ชันที่ติดตามราคาและปรับ SL ตามระยะห่างที่กำหนด
        
        return False, "ฟังก์ชัน Trailing Stop ไม่สามารถใช้งานผ่าน API ได้โดยตรง"
    
    def _get_retcode_description(self, retcode: int) -> str:
        """
        แปลงรหัสผลลัพธ์เป็นคำอธิบาย
        
        Args:
            retcode: รหัสผลลัพธ์
            
        Returns:
            str: คำอธิบายรหัสผลลัพธ์
        """
        retcodes = {
            10004: "Requote",
            10006: "Request rejected",
            10007: "Request canceled by trader",
            10008: "Order placed",
            10009: "Request executed",
            10010: "Request executed partially",
            10011: "Request error",
            10012: "Request timed out",
            10013: "Invalid request",
            10014: "Invalid volume",
            10015: "Invalid price",
            10016: "Invalid stops",
            10017: "Trade disabled",
            10018: "Market closed",
            10019: "Not enough money",
            10020: "Prices changed",
            10021: "No quotes to process request",
            10022: "Invalid order expiration date",
            10023: "Order state changed",
            10024: "Too many requests",
            10025: "No changes in request",
            10026: "Autotrading disabled by server",
            10027: "Autotrading disabled by client",
            10028: "Request locked for processing",
            10029: "Order or position frozen",
            10030: "Invalid order filling type",
            10031: "No connection with trade server",
            10032: "Operation is allowed only for live accounts",
            10033: "The maximum number of pending orders has been reached",
            10034: "The maximum volume of orders and positions has been reached",
            10035: "Invalid or prohibited order type",
            10036: "Position with the specified identifier already closed",
            10038: "The volume of the total position exceeds the limit",
            10039: "Closed position to be modified is not found",
            10040: "Closed order to be modified is not found",
            10041: "Closed position to be modified is found, but there's mismatch of orders",
            10042: "Position with specified identifier found, but it's already being processed",
            10043: "Order with specified identifier found, but it's already being processed",
            10044: "Pending order has been placed and is accepted for processing",
            10045: "Order has been placed and is accepted for processing",
            10046: "Order or position has been modified and modification is accepted for processing",
            10047: "Order or position has been deleted and deletion is accepted for processing",
            10048: "Order or position has been closed and accepted for processing"
        }
        return retcodes.get(retcode, f"Unknown ({retcode})")
