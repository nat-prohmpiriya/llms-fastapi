import MetaTrader5 as mt5
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import time
import pytz
from services.mt5_service import MT5Service
from schema.mt5.market_models import TimeFrame

class MT5MarketService:
    """
    บริการสำหรับจัดการข้อมูลตลาดใน MetaTrader 5
    """
    
    def __init__(self):
        """
        เริ่มต้นบริการ MT5MarketService
        """
        self.mt5_service = MT5Service()
        self._timeframe_map = {
            TimeFrame.M1: mt5.TIMEFRAME_M1,
            TimeFrame.M5: mt5.TIMEFRAME_M5,
            TimeFrame.M15: mt5.TIMEFRAME_M15,
            TimeFrame.M30: mt5.TIMEFRAME_M30,
            TimeFrame.H1: mt5.TIMEFRAME_H1,
            TimeFrame.H4: mt5.TIMEFRAME_H4,
            TimeFrame.D1: mt5.TIMEFRAME_D1,
            TimeFrame.W1: mt5.TIMEFRAME_W1,
            TimeFrame.MN1: mt5.TIMEFRAME_MN1
        }
    
    def get_symbols(self) -> Tuple[bool, str, Optional[List[str]], int]:
        """
        ดึงรายการสัญลักษณ์ทั้งหมด
        
        Returns:
            Tuple[bool, str, Optional[List[str]], int]: สถานะการดึงข้อมูล, ข้อความ, รายการสัญลักษณ์, จำนวนสัญลักษณ์ทั้งหมด
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None, 0
        
        symbols = mt5.symbols_get()
        if symbols is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงรายการสัญลักษณ์ได้: {error}", None, 0
        
        # สร้างรายการชื่อสัญลักษณ์
        symbol_names = [symbol.name for symbol in symbols]
        
        return True, "ดึงรายการสัญลักษณ์สำเร็จ", symbol_names, len(symbol_names)
    
    def get_symbol_info(self, symbol: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        ดึงข้อมูลสัญลักษณ์
        
        Args:
            symbol: ชื่อสัญลักษณ์
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการดึงข้อมูล, ข้อความ, ข้อมูลสัญลักษณ์
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลสัญลักษณ์ {symbol} ได้: {error}", None
        
        # แปลงข้อมูลสัญลักษณ์เป็นรูปแบบ dict
        symbol_dict = self._convert_to_dict(symbol_info)
        
        # เพิ่มคำอธิบายประเภทการซื้อขาย
        symbol_dict["trade_mode_description"] = self._get_trade_mode_description(symbol_dict["trade_mode"])
        
        return True, "ดึงข้อมูลสัญลักษณ์สำเร็จ", symbol_dict
    
    def get_price(self, symbol: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        ดึงข้อมูลราคาล่าสุดของสัญลักษณ์
        
        Args:
            symbol: ชื่อสัญลักษณ์
            
        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: สถานะการดึงข้อมูล, ข้อความ, ข้อมูลราคา
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None
        
        symbol_info = mt5.symbol_info_tick(symbol)
        if symbol_info is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลราคาของสัญลักษณ์ {symbol} ได้: {error}", None
        
        # แปลงข้อมูลราคาเป็นรูปแบบ dict
        price_dict = self._convert_to_dict(symbol_info)
        
        # แปลงเวลาเป็น datetime
        price_dict["time"] = datetime.fromtimestamp(price_dict["time"], tz=pytz.UTC)
        
        return True, "ดึงข้อมูลราคาสำเร็จ", price_dict
    
    def get_ticks(self, symbol: str, count: int = 100) -> Tuple[bool, str, Optional[List[Dict[str, Any]]], int]:
        """
        ดึงข้อมูล tick ของสัญลักษณ์
        
        Args:
            symbol: ชื่อสัญลักษณ์
            count: จำนวน tick ที่ต้องการ
            
        Returns:
            Tuple[bool, str, Optional[List[Dict[str, Any]]], int]: สถานะการดึงข้อมูล, ข้อความ, รายการข้อมูล tick, จำนวน tick ทั้งหมด
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None, 0
        
        ticks = mt5.copy_ticks_from(symbol, 0, count, mt5.COPY_TICKS_ALL)
        if ticks is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูล tick ของสัญลักษณ์ {symbol} ได้: {error}", None, 0
        
        # แปลงข้อมูล tick เป็นรูปแบบ dict
        ticks_list = []
        for tick in ticks:
            tick_dict = {
                "time": datetime.fromtimestamp(tick[0], tz=pytz.UTC),
                "bid": tick[1],
                "ask": tick[2],
                "last": tick[3],
                "volume": tick[4],
                "flags": tick[5]
            }
            ticks_list.append(tick_dict)
        
        return True, "ดึงข้อมูล tick สำเร็จ", ticks_list, len(ticks_list)
    
    def get_ohlc(self, symbol: str, timeframe: TimeFrame, count: int = 100, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None) -> Tuple[bool, str, Optional[List[Dict[str, Any]]], int]:
        """
        ดึงข้อมูล OHLC (แท่งเทียน) ของสัญลักษณ์
        
        Args:
            symbol: ชื่อสัญลักษณ์
            timeframe: กรอบเวลา
            count: จำนวนแท่งเทียนที่ต้องการ
            from_date: วันที่เริ่มต้น
            to_date: วันที่สิ้นสุด
            
        Returns:
            Tuple[bool, str, Optional[List[Dict[str, Any]]], int]: สถานะการดึงข้อมูล, ข้อความ, รายการข้อมูลแท่งเทียน, จำนวนแท่งเทียนทั้งหมด
        """
        if not self.mt5_service.is_connected():
            return False, "ไม่ได้เชื่อมต่อกับ MT5", None, 0
        
        # แปลงกรอบเวลาเป็นค่าที่ใช้ใน MT5
        mt5_timeframe = self._timeframe_map.get(timeframe)
        if mt5_timeframe is None:
            return False, f"กรอบเวลา {timeframe} ไม่ถูกต้อง", None, 0
        
        # กำหนดพารามิเตอร์สำหรับการดึงข้อมูล
        if from_date and to_date:
            # ดึงข้อมูลตามช่วงเวลา
            rates = mt5.copy_rates_range(symbol, mt5_timeframe, from_date, to_date)
        elif from_date:
            # ดึงข้อมูลตั้งแต่วันที่เริ่มต้นจนถึงปัจจุบัน
            rates = mt5.copy_rates_from(symbol, mt5_timeframe, from_date, count)
        else:
            # ดึงข้อมูลล่าสุดตามจำนวนที่ต้องการ
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
        
        if rates is None:
            error = mt5.last_error()
            return False, f"ไม่สามารถดึงข้อมูลแท่งเทียนของสัญลักษณ์ {symbol} ได้: {error}", None, 0
        
        # แปลงข้อมูลแท่งเทียนเป็นรูปแบบ dict
        candles_list = []
        for rate in rates:
            candle_dict = {
                "time": datetime.fromtimestamp(rate[0], tz=pytz.UTC),
                "open": rate[1],
                "high": rate[2],
                "low": rate[3],
                "close": rate[4],
                "tick_volume": rate[5],
                "spread": rate[6],
                "real_volume": rate[7]
            }
            candles_list.append(candle_dict)
        
        return True, "ดึงข้อมูลแท่งเทียนสำเร็จ", candles_list, len(candles_list)
    
    def _convert_to_dict(self, named_tuple) -> Dict[str, Any]:
        """
        แปลง named tuple เป็น dict
        
        Args:
            named_tuple: named tuple ที่ต้องการแปลง
            
        Returns:
            Dict[str, Any]: dict ที่แปลงแล้ว
        """
        return {key: getattr(named_tuple, key) for key in dir(named_tuple) if not key.startswith('_')}
    
    def _get_trade_mode_description(self, trade_mode: int) -> str:
        """
        แปลงรหัสประเภทการซื้อขายเป็นคำอธิบาย
        
        Args:
            trade_mode: รหัสประเภทการซื้อขาย
            
        Returns:
            str: คำอธิบายประเภทการซื้อขาย
        """
        trade_modes = {
            0: "Disabled",
            1: "Long Only",
            2: "Short Only",
            3: "Long and Short",
            4: "Close Only"
        }
        return trade_modes.get(trade_mode, f"Unknown ({trade_mode})")
