from typing import List
import re
import json
from pathlib import Path
from datetime import datetime
import pdfplumber
import tempfile
import os
from fastapi import UploadFile

from app.src.schemas.transaction_common import CommonTransaction
from app.src.services.parsers.base import BaseParser
from app.src.services.parsers.registry import ParserEngine

# 종목명 → 티커 매핑을 외부 JSON 파일에서 로드
# 새로운 종목 추가 시 ticker_map.json 파일만 수정하면 됩니다.
_TICKER_MAP_PATH = Path(__file__).parent / "ticker_map.json"
with _TICKER_MAP_PATH.open(encoding="utf-8") as _f:
    TICKER_MAP: dict[str, str] = json.load(_f)

class TossParser(BaseParser):
    @property
    def provider_name(self) -> str:
        return "toss"

    def _guess_ticker(self, name: str) -> str:
        for key, ticker in TICKER_MAP.items():
            if key in name:
                return ticker
        return "UNKNOWN"

    async def parse(self, file: UploadFile, **kwargs) -> List[CommonTransaction]:
        """
        토스증권 거래내역(PDF)을 파싱하여 공통 포맷으로 변환합니다.
        """
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")

        parsed_transactions = []
        
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            with pdfplumber.open(tmp_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
                
        lines = text.split("\n")
        
        # Regex patterns
        line1_pattern = re.compile(r"^(\d{4}\.\d{2}\.\d{2})\s+(구매|판매)\s+(.*?)\s+([\d,]+(?:\.\d+)?)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)")

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            m1 = line1_pattern.search(line)
            if m1:
                date_str = m1.group(1)
                type_str = m1.group(2)
                name_str = m1.group(3).strip()
                quantity_str = m1.group(5).replace(",", "")
                
                price_usd = 0.0
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    m2 = re.search(r"\(\$\s*([\d,.]+)\)", next_line)
                    if m2:
                        usd_amounts = re.findall(r"\(\$\s*([\d,.]+)\)", next_line)
                        if len(usd_amounts) >= 2:
                            price_usd = float(usd_amounts[1].replace(",", ""))
                    
                    if "US" in next_line and "(" in next_line:
                        name_part = re.sub(r"\(US[A-Z0-9]+\).*$", "", next_line).strip()
                        if name_part and name_part != "ETF":
                            name_str += " " + name_part

                ticker = self._guess_ticker(name_str)
                tx_type = "BUY" if type_str == "구매" else "SELL"
                
                parsed_transactions.append(CommonTransaction(
                    date=datetime.strptime(date_str, "%Y.%m.%d"),
                    type=tx_type, # type: ignore
                    ticker=ticker,
                    name=name_str,
                    quantity=float(quantity_str),
                    price=price_usd,
                    currency="USD"
                ))
            i += 1
            
        return parsed_transactions

# 엔진에 Toss 파서 등록
ParserEngine.register_parser(TossParser())
