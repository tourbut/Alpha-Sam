from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class CommonTransaction(BaseModel):
    """
    모든 파서(토스증권, 키움증권 등)가 변환 결과로 반환해야 하는 공통 거래내역 DTO입니다.
    또한, 사용자가 공통 CSV/Excel 양식으로 직접 업로드할 때의 스키마 역할도 수행합니다.
    """
    date: datetime = Field(..., description="거래 일자 및 시간 (예: 2023-10-01T12:00:00)")
    type: Literal["BUY", "SELL"] = Field(..., description="거래 유형 (BUY 또는 SELL)")
    ticker: str = Field(..., description="종목 티커 (예: AAPL, BTC-USD)")
    name: str = Field("", description="종목명 (선택사항, 사용자가 확인하기 위한 보조 용도)")
    quantity: float = Field(..., description="거래 수량 (매수/매도 수량)")
    price: float = Field(..., description="체결 단가 (단일 자산 기준)")
    currency: str = Field("USD", description="거래 통화 (기본값: USD)")
    fee: float = Field(0.0, description="수수료 (기본값: 0.0)")
