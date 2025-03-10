import MetaTrader5 as mt5
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from services.mt5_service import MT5Service
from schema.mt5.technical_models import (
    MAMethod, PriceType, TimeFrame, 
    MovingAverageRequest, MovingAverageResponse,
    RSIRequest, RSIResponse,
    MACDRequest, MACDResponse,
    BollingerBandsRequest, BollingerBandsResponse,
    StochasticRequest, StochasticResponse,
    IchimokuRequest, IchimokuResponse
)

class MT5TechnicalService:
    """
    บริการสำหรับการวิเคราะห์ทางเทคนิคใน MetaTrader 5
    """
    
    def __init__(self):
        """
        เริ่มต้นบริการ MT5TechnicalService
        """
        self.mt5_service = MT5Service()
    
    def get_moving_average(self, request: MovingAverageRequest) -> MovingAverageResponse:
        """
        คำนวณค่าเฉลี่ยเคลื่อนที่ (Moving Average)
        
        Args:
            request: คำขอสำหรับ MA
            
        Returns:
            MovingAverageResponse: ผลลัพธ์ของค่าเฉลี่ยเคลื่อนที่
        """
        if not self.mt5_service.is_connected():
            return MovingAverageResponse(
                success=False,
                message="ไม่ได้เชื่อมต่อกับ MT5",
                values=[]
            )
        
        # แปลงพารามิเตอร์
        symbol = request.symbol
        timeframe = int(request.timeframe)
        period = request.period
        ma_type = int(request.ma_type)
        applied_price = int(request.applied_price)
        shift = request.shift
        
        # ดึงข้อมูลราคาเพื่อคำนวณ MA
        try:
            # ดึงข้อมูล OHLC
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + shift + 100)
            if rates is None or len(rates) == 0:
                return MovingAverageResponse(
                    success=False,
                    message=f"ไม่สามารถดึงข้อมูลราคาสำหรับ {symbol}",
                    values=[]
                )
            
            # แปลงเป็น DataFrame
            rates_df = pd.DataFrame(rates)
            
            # เลือกประเภทราคาที่จะใช้
            price_data = None
            if applied_price == PriceType.CLOSE:
                price_data = rates_df['close']
            elif applied_price == PriceType.OPEN:
                price_data = rates_df['open']
            elif applied_price == PriceType.HIGH:
                price_data = rates_df['high']
            elif applied_price == PriceType.LOW:
                price_data = rates_df['low']
            elif applied_price == PriceType.MEDIAN:
                price_data = (rates_df['high'] + rates_df['low']) / 2.0
            elif applied_price == PriceType.TYPICAL:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close']) / 3.0
            elif applied_price == PriceType.WEIGHTED:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close'] * 2) / 4.0
            
            # คำนวณ MA ตามประเภท
            ma_values = None
            if ma_type == MAMethod.SMA:
                ma_values = price_data.rolling(window=period).mean()
            elif ma_type == MAMethod.EMA:
                ma_values = price_data.ewm(span=period, adjust=False).mean()
            elif ma_type == MAMethod.SMMA:
                ma_values = price_data.ewm(alpha=1/period, adjust=False).mean()
            elif ma_type == MAMethod.LWMA:
                weights = np.arange(1, period + 1)
                ma_values = price_data.rolling(window=period).apply(lambda x: np.sum(weights * x) / np.sum(weights), raw=True)
            
            # ตัดข้อมูลตาม shift
            if ma_values is not None:
                ma_values = ma_values.iloc[-(shift+1):]
                result_values = [float(value) for value in ma_values.values if not np.isnan(value)]
                
                return MovingAverageResponse(
                    success=True,
                    message="คำนวณ MA สำเร็จ",
                    values=result_values
                )
            else:
                return MovingAverageResponse(
                    success=False,
                    message="ไม่สามารถคำนวณ MA ได้",
                    values=[]
                )
                
        except Exception as e:
            return MovingAverageResponse(
                success=False,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                values=[]
            )
    
    def get_rsi(self, request: RSIRequest) -> RSIResponse:
        """
        คำนวณค่า Relative Strength Index (RSI)
        
        Args:
            request: คำขอสำหรับ RSI
            
        Returns:
            RSIResponse: ผลลัพธ์ของ RSI
        """
        if not self.mt5_service.is_connected():
            return RSIResponse(
                success=False,
                message="ไม่ได้เชื่อมต่อกับ MT5",
                values=[]
            )
        
        # แปลงพารามิเตอร์
        symbol = request.symbol
        timeframe = int(request.timeframe)
        period = request.period
        applied_price = int(request.applied_price)
        shift = request.shift
        
        try:
            # ดึงข้อมูล OHLC
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + shift + 100)
            if rates is None or len(rates) == 0:
                return RSIResponse(
                    success=False,
                    message=f"ไม่สามารถดึงข้อมูลราคาสำหรับ {symbol}",
                    values=[]
                )
            
            # แปลงเป็น DataFrame
            rates_df = pd.DataFrame(rates)
            
            # เลือกประเภทราคาที่จะใช้
            price_data = None
            if applied_price == PriceType.CLOSE:
                price_data = rates_df['close']
            elif applied_price == PriceType.OPEN:
                price_data = rates_df['open']
            elif applied_price == PriceType.HIGH:
                price_data = rates_df['high']
            elif applied_price == PriceType.LOW:
                price_data = rates_df['low']
            elif applied_price == PriceType.MEDIAN:
                price_data = (rates_df['high'] + rates_df['low']) / 2.0
            elif applied_price == PriceType.TYPICAL:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close']) / 3.0
            elif applied_price == PriceType.WEIGHTED:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close'] * 2) / 4.0
            
            # คำนวณ RSI
            delta = price_data.diff()
            gain = delta.mask(delta < 0, 0)
            loss = -delta.mask(delta > 0, 0)
            
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            # ตัดข้อมูลตาม shift
            rsi = rsi.iloc[-(shift+1):]
            result_values = [float(value) for value in rsi.values if not np.isnan(value)]
            
            return RSIResponse(
                success=True,
                message="คำนวณ RSI สำเร็จ",
                values=result_values
            )
            
        except Exception as e:
            return RSIResponse(
                success=False,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                values=[]
            )
    
    def get_macd(self, request: MACDRequest) -> MACDResponse:
        """
        คำนวณค่า Moving Average Convergence Divergence (MACD)
        
        Args:
            request: คำขอสำหรับ MACD
            
        Returns:
            MACDResponse: ผลลัพธ์ของ MACD
        """
        if not self.mt5_service.is_connected():
            return MACDResponse(
                success=False,
                message="ไม่ได้เชื่อมต่อกับ MT5",
                macd_line=[],
                signal_line=[],
                histogram=[]
            )
        
        # แปลงพารามิเตอร์
        symbol = request.symbol
        timeframe = int(request.timeframe)
        fast_ema = request.fast_ema
        slow_ema = request.slow_ema
        signal_period = request.signal_period
        applied_price = int(request.applied_price)
        shift = request.shift
        
        try:
            # ดึงข้อมูล OHLC
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, slow_ema + signal_period + shift + 100)
            if rates is None or len(rates) == 0:
                return MACDResponse(
                    success=False,
                    message=f"ไม่สามารถดึงข้อมูลราคาสำหรับ {symbol}",
                    macd_line=[],
                    signal_line=[],
                    histogram=[]
                )
            
            # แปลงเป็น DataFrame
            rates_df = pd.DataFrame(rates)
            
            # เลือกประเภทราคาที่จะใช้
            price_data = None
            if applied_price == PriceType.CLOSE:
                price_data = rates_df['close']
            elif applied_price == PriceType.OPEN:
                price_data = rates_df['open']
            elif applied_price == PriceType.HIGH:
                price_data = rates_df['high']
            elif applied_price == PriceType.LOW:
                price_data = rates_df['low']
            elif applied_price == PriceType.MEDIAN:
                price_data = (rates_df['high'] + rates_df['low']) / 2.0
            elif applied_price == PriceType.TYPICAL:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close']) / 3.0
            elif applied_price == PriceType.WEIGHTED:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close'] * 2) / 4.0
            
            # คำนวณ MACD
            fast_ema_values = price_data.ewm(span=fast_ema, adjust=False).mean()
            slow_ema_values = price_data.ewm(span=slow_ema, adjust=False).mean()
            
            macd_line = fast_ema_values - slow_ema_values
            signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
            histogram = macd_line - signal_line
            
            # ตัดข้อมูลตาม shift
            macd_line = macd_line.iloc[-(shift+1):]
            signal_line = signal_line.iloc[-(shift+1):]
            histogram = histogram.iloc[-(shift+1):]
            
            macd_values = [float(value) for value in macd_line.values if not np.isnan(value)]
            signal_values = [float(value) for value in signal_line.values if not np.isnan(value)]
            histogram_values = [float(value) for value in histogram.values if not np.isnan(value)]
            
            return MACDResponse(
                success=True,
                message="คำนวณ MACD สำเร็จ",
                macd_line=macd_values,
                signal_line=signal_values,
                histogram=histogram_values
            )
            
        except Exception as e:
            return MACDResponse(
                success=False,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                macd_line=[],
                signal_line=[],
                histogram=[]
            )
    
    def get_bollinger_bands(self, request: BollingerBandsRequest) -> BollingerBandsResponse:
        """
        คำนวณค่า Bollinger Bands
        
        Args:
            request: คำขอสำหรับ Bollinger Bands
            
        Returns:
            BollingerBandsResponse: ผลลัพธ์ของ Bollinger Bands
        """
        if not self.mt5_service.is_connected():
            return BollingerBandsResponse(
                success=False,
                message="ไม่ได้เชื่อมต่อกับ MT5",
                upper_band=[],
                middle_band=[],
                lower_band=[]
            )
        
        # แปลงพารามิเตอร์
        symbol = request.symbol
        timeframe = int(request.timeframe)
        period = request.period
        deviation = request.deviation
        applied_price = int(request.applied_price)
        shift = request.shift
        
        try:
            # ดึงข้อมูล OHLC
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + shift + 100)
            if rates is None or len(rates) == 0:
                return BollingerBandsResponse(
                    success=False,
                    message=f"ไม่สามารถดึงข้อมูลราคาสำหรับ {symbol}",
                    upper_band=[],
                    middle_band=[],
                    lower_band=[]
                )
            
            # แปลงเป็น DataFrame
            rates_df = pd.DataFrame(rates)
            
            # เลือกประเภทราคาที่จะใช้
            price_data = None
            if applied_price == PriceType.CLOSE:
                price_data = rates_df['close']
            elif applied_price == PriceType.OPEN:
                price_data = rates_df['open']
            elif applied_price == PriceType.HIGH:
                price_data = rates_df['high']
            elif applied_price == PriceType.LOW:
                price_data = rates_df['low']
            elif applied_price == PriceType.MEDIAN:
                price_data = (rates_df['high'] + rates_df['low']) / 2.0
            elif applied_price == PriceType.TYPICAL:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close']) / 3.0
            elif applied_price == PriceType.WEIGHTED:
                price_data = (rates_df['high'] + rates_df['low'] + rates_df['close'] * 2) / 4.0
            
            # คำนวณ Bollinger Bands
            middle_band = price_data.rolling(window=period).mean()
            std_dev = price_data.rolling(window=period).std(ddof=0)
            
            upper_band = middle_band + (std_dev * deviation)
            lower_band = middle_band - (std_dev * deviation)
            
            # ตัดข้อมูลตาม shift
            upper_band = upper_band.iloc[-(shift+1):]
            middle_band = middle_band.iloc[-(shift+1):]
            lower_band = lower_band.iloc[-(shift+1):]
            
            upper_values = [float(value) for value in upper_band.values if not np.isnan(value)]
            middle_values = [float(value) for value in middle_band.values if not np.isnan(value)]
            lower_values = [float(value) for value in lower_band.values if not np.isnan(value)]
            
            return BollingerBandsResponse(
                success=True,
                message="คำนวณ Bollinger Bands สำเร็จ",
                upper_band=upper_values,
                middle_band=middle_values,
                lower_band=lower_values
            )
            
        except Exception as e:
            return BollingerBandsResponse(
                success=False,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                upper_band=[],
                middle_band=[],
                lower_band=[]
            )

    def get_stochastic(self, request: StochasticRequest) -> StochasticResponse:
        """
        คำนวณค่า Stochastic Oscillator
        
        Args:
            request: คำขอสำหรับ Stochastic
            
        Returns:
            StochasticResponse: ผลลัพธ์ของ Stochastic
        """
        if not self.mt5_service.is_connected():
            return StochasticResponse(
                success=False,
                message="ไม่ได้เชื่อมต่อกับ MT5",
                k_line=[],
                d_line=[]
            )
        
        # แปลงพารามิเตอร์
        symbol = request.symbol
        timeframe = int(request.timeframe)
        k_period = request.k_period
        d_period = request.d_period
        slowing = request.slowing
        shift = request.shift
        
        try:
            # ดึงข้อมูล OHLC
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, k_period + d_period + slowing + shift + 100)
            if rates is None or len(rates) == 0:
                return StochasticResponse(
                    success=False,
                    message=f"ไม่สามารถดึงข้อมูลราคาสำหรับ {symbol}",
                    k_line=[],
                    d_line=[]
                )
            
            # แปลงเป็น DataFrame
            rates_df = pd.DataFrame(rates)
            
            # คำนวณ Stochastic
            # %K = (Current Close - Lowest Low) / (Highest High - Lowest Low) * 100
            # %D = 3-day SMA of %K
            
            # คำนวณ Lowest Low ใน k_period แท่ง
            low_min = rates_df['low'].rolling(window=k_period).min()
            
            # คำนวณ Highest High ใน k_period แท่ง
            high_max = rates_df['high'].rolling(window=k_period).max()
            
            # คำนวณ %K
            k_percent = 100 * ((rates_df['close'] - low_min) / (high_max - low_min))
            
            # ปรับ %K ด้วย slowing period
            if slowing > 1:
                k_percent = k_percent.rolling(window=slowing).mean()
            
            # คำนวณ %D (SMA ของ %K)
            d_percent = k_percent.rolling(window=d_period).mean()
            
            # ตัดข้อมูลตาม shift
            k_percent = k_percent.iloc[-(shift+1):]
            d_percent = d_percent.iloc[-(shift+1):]
            
            k_values = [float(value) for value in k_percent.values if not np.isnan(value)]
            d_values = [float(value) for value in d_percent.values if not np.isnan(value)]
            
            return StochasticResponse(
                success=True,
                message="คำนวณ Stochastic สำเร็จ",
                k_line=k_values,
                d_line=d_values
            )
            
        except Exception as e:
            return StochasticResponse(
                success=False,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                k_line=[],
                d_line=[]
            )

    def get_ichimoku(self, request: IchimokuRequest) -> IchimokuResponse:
        """
        คำนวณค่า Ichimoku Cloud
        
        Args:
            request: คำขอสำหรับ Ichimoku
            
        Returns:
            IchimokuResponse: ผลลัพธ์ของ Ichimoku
        """
        if not self.mt5_service.is_connected():
            return IchimokuResponse(
                success=False,
                message="ไม่ได้เชื่อมต่อกับ MT5",
                tenkan_sen=[],
                kijun_sen=[],
                senkou_span_a=[],
                senkou_span_b=[],
                chikou_span=[]
            )
        
        # แปลงพารามิเตอร์
        symbol = request.symbol
        timeframe = int(request.timeframe)
        tenkan_period = request.tenkan_period
        kijun_period = request.kijun_period
        senkou_span_b_period = request.senkou_span_b_period
        shift = request.shift
        
        try:
            # ดึงข้อมูล OHLC (ต้องดึงข้อมูลมากพอ)
            max_period = max(tenkan_period, kijun_period, senkou_span_b_period)
            future_bars = kijun_period  # สำหรับ Senkou Span A และ B ที่วาดในอนาคต
            past_bars = kijun_period  # สำหรับ Chikou Span ที่วาดในอดีต
            total_bars = max_period + future_bars + past_bars + shift + 100
            
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, total_bars)
            if rates is None or len(rates) == 0:
                return IchimokuResponse(
                    success=False,
                    message=f"ไม่สามารถดึงข้อมูลราคาสำหรับ {symbol}",
                    tenkan_sen=[],
                    kijun_sen=[],
                    senkou_span_a=[],
                    senkou_span_b=[],
                    chikou_span=[]
                )
            
            # แปลงเป็น DataFrame
            rates_df = pd.DataFrame(rates)
            
            # Tenkan-sen (Conversion Line) = (highest high + lowest low) / 2 for the past tenkan_period periods
            high_tenkan = rates_df['high'].rolling(window=tenkan_period).max()
            low_tenkan = rates_df['low'].rolling(window=tenkan_period).min()
            tenkan_sen = (high_tenkan + low_tenkan) / 2
            
            # Kijun-sen (Base Line) = (highest high + lowest low) / 2 for the past kijun_period periods
            high_kijun = rates_df['high'].rolling(window=kijun_period).max()
            low_kijun = rates_df['low'].rolling(window=kijun_period).min()
            kijun_sen = (high_kijun + low_kijun) / 2
            
            # Senkou Span A (Leading Span A) = (Tenkan-sen + Kijun-sen) / 2 shifted forward by kijun_period
            senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun_period)
            
            # Senkou Span B (Leading Span B) = (highest high + lowest low) / 2 for the past senkou_span_b_period periods shifted forward by kijun_period
            high_senkou = rates_df['high'].rolling(window=senkou_span_b_period).max()
            low_senkou = rates_df['low'].rolling(window=senkou_span_b_period).min()
            senkou_span_b = ((high_senkou + low_senkou) / 2).shift(kijun_period)
            
            # Chikou Span (Lagging Span) = Current closing price shifted backwards by kijun_period
            chikou_span = rates_df['close'].shift(-kijun_period)
            
            # ตัดข้อมูลตาม shift
            tenkan_sen = tenkan_sen.iloc[-(shift+1+kijun_period):-kijun_period]
            kijun_sen = kijun_sen.iloc[-(shift+1+kijun_period):-kijun_period]
            senkou_span_a = senkou_span_a.iloc[-(shift+1):]
            senkou_span_b = senkou_span_b.iloc[-(shift+1):]
            chikou_span = chikou_span.iloc[-(shift+1+kijun_period):-kijun_period]
            
            tenkan_values = [float(value) for value in tenkan_sen.values if not np.isnan(value)]
            kijun_values = [float(value) for value in kijun_sen.values if not np.isnan(value)]
            senkou_a_values = [float(value) for value in senkou_span_a.values if not np.isnan(value)]
            senkou_b_values = [float(value) for value in senkou_span_b.values if not np.isnan(value)]
            chikou_values = [float(value) for value in chikou_span.values if not np.isnan(value)]
            
            return IchimokuResponse(
                success=True,
                message="คำนวณ Ichimoku Cloud สำเร็จ",
                tenkan_sen=tenkan_values,
                kijun_sen=kijun_values,
                senkou_span_a=senkou_a_values,
                senkou_span_b=senkou_b_values,
                chikou_span=chikou_values
            )
            
        except Exception as e:
            return IchimokuResponse(
                success=False,
                message=f"เกิดข้อผิดพลาด: {str(e)}",
                tenkan_sen=[],
                kijun_sen=[],
                senkou_span_a=[],
                senkou_span_b=[],
                chikou_span=[]
            )
