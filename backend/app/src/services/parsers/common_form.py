import csv
import io
from typing import List
from datetime import datetime
from fastapi import UploadFile

from app.src.schemas.transaction_common import CommonTransaction
from app.src.services.parsers.base import BaseParser
from app.src.services.parsers.registry import ParserEngine

class CommonFormParser(BaseParser):
    @property
    def provider_name(self) -> str:
        return "common"

    async def parse(self, file: UploadFile, **kwargs) -> List[CommonTransaction]:
        """
        알파샘 공통 CSV 거래내역 양식을 파싱하여 변환합니다.
        기대하는 CSV 컬럼 (헤더 존재 فرض):
        Date,Type,Ticker,Name,Quantity,Price,Currency,Fee
        """
        parsed_transactions = []
        
        content = await file.read()
        target_encoding = "utf-8"
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("cp949")
            target_encoding = "cp949"
            
        csv_file = io.StringIO(text)
        reader = csv.DictReader(csv_file)
        
        # DictReader는 첫 줄을 헤더로 인식함
        # 필수 필드 검증 등을 생략하거나 추가할 수 있습니다.
        for row in reader:
            try:
                # 필드명 매핑 (대소문자 무시 혹은 정규화)
                # 간소화를 위해 정확한 키값이 들어왔다고 가정
                date_str = row.get("Date", "").strip()
                t_type = row.get("Type", "BUY").strip().upper()
                ticker = row.get("Ticker", "").strip()
                name = row.get("Name", "").strip()
                qty = float(row.get("Quantity", 0))
                price = float(row.get("Price", 0))
                currency = row.get("Currency", "USD").strip()
                fee = float(row.get("Fee", 0))
                
                if not date_str or not ticker:
                    continue # 필수 데이터 누락시 건너뜀 (현실적으로는 Validation 로직 필요)
                    
                # Date 파싱 (여러 가지 포맷 대비 1차 처리. 기본값은 ISO 8601 YYYY-MM-DD or YYYY.MM.DD)
                date_str = date_str.replace(".", "-")
                if len(date_str) == 10:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    dt = datetime.fromisoformat(date_str)

                parsed_transactions.append(CommonTransaction(
                    date=dt,
                    type=t_type if t_type in ["BUY", "SELL"] else "BUY", # type: ignore
                    ticker=ticker,
                    name=name,
                    quantity=qty,
                    price=price,
                    currency=currency,
                    fee=fee
                ))
            except Exception as e:
                # 파싱 중 에러 발생 시 로깅 또는 예외 처리 강화
                print(f"Row 변환 에러: {row} - Err: {e}")
                pass
                
        return parsed_transactions

# 엔진에 Common 파서 등록
ParserEngine.register_parser(CommonFormParser())
