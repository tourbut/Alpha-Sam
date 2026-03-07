from typing import List, Dict, Any
import re
from datetime import datetime
import pdfplumber
import tempfile
from fastapi import UploadFile
from pydantic import BaseModel

class ParsedTransaction(BaseModel):
    date: datetime
    type: str # 'BUY' or 'SELL'
    name: str
    ticker: str
    quantity: float
    price: float

TICKER_MAP = {
    "JP모건 커버드콜 옵션 ETF": "JEPI",
    "JP모건 나스닥 프리미엄 인컴 ETF": "JEPQ",
    "라운드힐 S&P 500 0DTE 커버드콜 전략": "XDTE", # 긴 이름 처리 위해 일부만 매칭되도록 할 수 있음
    "라운드힐 S&P 500 0DTE 커버드콜 전략 ETF": "XDTE",
    "라운드힐 N-100 0DTE 커버드콜 전략 ETF": "QDTE",
    "브로드컴": "AVGO",
    "프로셰어즈 QQQ 3배 ETF": "TQQQ",
    "골드만삭스 나스닥 100 코어 프리미엄 인컴": "GPIQ",
    "골드만삭스 나스닥 100 코어 프리미엄 인컴 ETF": "GPIQ",
    "앰플리파이 배당 수익 ETF": "DIVO", 
    "앰플리파이 CWP 성장 & 인컴 ETF": "DIVO", # 둘 다 DIVO일 가능성 또는 하나는 IDVO 등일 수 있음. 일단 이름 매핑
    "글로벌엑스 DOW30 커버드콜 ETF": "DJIA",
    "클라우드플레어": "NET"
}

class TossParserService:
    @staticmethod
    def guess_ticker(name: str) -> str:
        for key, ticker in TICKER_MAP.items():
            if key in name:
                return ticker
        return "UNKNOWN"

    @staticmethod
    async def parse_pdf(file: UploadFile) -> List[ParsedTransaction]:
        """
        UploadFile 객체를 임시 파일로 저장한 다음 pdfplumber로 파싱하여 텍스트를 추출하고 거래 내역을 반환합니다.
        """
        parsed_transactions = []
        
        # 임시 파일로 저장하여 pdfplumber가 읽을 수 있도록 처리
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
            # 임시 파일 삭제 로직
            import os
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
                
        lines = text.split("\n")
        
        # 첫번째 줄 정규식 패턴: 
        # 2025.06.02 구매 JP모건 나스닥 프리미엄 인컴 ETF 1,375.70 5 362,978 72,595 357 0 0 25 1,663,028
        # 날짜(yyyy.mm.dd) 구분(구매/판매) 종목명 환율 수량 ...
        line1_pattern = re.compile(r"^(\d{4}\.\d{2}\.\d{2})\s+(구매|판매)\s+(.*?)\s+([\d,]+(?:\.\d+)?)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)")
        
        # 두번째 줄 정규식 패턴:
        # (US46654Q2030) ($ 263.85) ($ 52.77) ($ 0.26) ... 단가는 세번째 USD 금액 ($ 52.77)
        line2_pattern = re.compile(r"^\([A-Z0-9]+\)\s+\(\$\s+[\d,.]+\)\s+\(\$\s+([\d,.]+)\)")

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            m1 = line1_pattern.search(line)
            if m1:
                date_str = m1.group(1)
                type_str = m1.group(2)
                name_str = m1.group(3).strip()
                quantity_str = m1.group(5).replace(",", "")
                
                # 다음 줄(혹은 다다음줄)에 달러 단가가 있는지 탐색
                price_usd = 0.0
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    # 종목명이 길어서 두 줄로 나뉘는 경우가 있음!
                    # 두 번째 달러값이 단가인 경우가 많음
                    m2 = re.search(r"\(\$\s*([\d,.]+)\)", next_line)
                    if m2:
                        usd_amounts = re.findall(r"\(\$\s*([\d,.]+)\)", next_line)
                        if len(usd_amounts) >= 2:
                            price_usd = float(usd_amounts[1].replace(",", ""))
                    
                    # 티커 찾기
                    if "US" in next_line and "(" in next_line:
                        # 같이 넘어간 이름 부분이 있으면 합침
                        name_part = re.sub(r"\(US[A-Z0-9]+\).*$", "", next_line).strip()
                        if name_part and name_part != "ETF":
                            name_str += " " + name_part

                ticker = TossParserService.guess_ticker(name_str)
                
                tx_type = "BUY" if type_str == "구매" else "SELL"
                
                parsed_transactions.append(ParsedTransaction(
                    date=datetime.strptime(date_str, "%Y.%m.%d"),
                    type=tx_type,
                    name=name_str,
                    ticker=ticker,
                    quantity=float(quantity_str),
                    price=price_usd
                ))
            i += 1
            
        return parsed_transactions
