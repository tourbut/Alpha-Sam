"""
포트폴리오 수익률 계산 서비스
domain_rules.md의 계산 규칙을 정확히 따름
"""
from typing import Optional, List, Dict
from decimal import Decimal


def calculate_position_metrics(
    quantity: float,
    buy_price: float,
    current_price: Optional[float]
) -> Dict[str, Optional[float]]:
    """
    단일 포지션의 평가액, 손익, 수익률 계산
    
    Args:
        quantity: 보유 수량
        buy_price: 매수 단가
        current_price: 현재 가격 (None이면 계산 불가)
    
    Returns:
        {
            "valuation": 평가액 (current_price * quantity),
            "profit_loss": 손익 ((current_price - buy_price) * quantity),
            "return_rate": 수익률 (((current_price - buy_price) / buy_price) * 100)
        }
        current_price가 None이면 모든 값이 None
    """
    if current_price is None:
        return {
            "valuation": None,
            "profit_loss": None,
            "return_rate": None
        }
    
    # 0으로 나누기 방지
    if buy_price <= 0:
        return {
            "valuation": None,
            "profit_loss": None,
            "return_rate": None
        }
    
    # 평가액 = current_price * quantity
    valuation = current_price * quantity
    
    # 손익 = (current_price - buy_price) * quantity
    profit_loss = (current_price - buy_price) * quantity
    
    # 수익률 = ((current_price - buy_price) / buy_price) * 100
    return_rate = ((current_price - buy_price) / buy_price) * 100
    
    return {
        "valuation": round(valuation, 2),
        "profit_loss": round(profit_loss, 2),
        "return_rate": round(return_rate, 2)
    }


def calculate_portfolio_summary(
    positions: List[Dict[str, float]]
) -> Dict[str, Optional[float]]:
    """
    전체 포트폴리오의 총 평가액, 총 손익, 포트폴리오 수익률 계산
    
    Args:
        positions: 포지션 리스트, 각 포지션은 다음 키를 가짐:
            - "quantity": 보유 수량
            - "buy_price": 매수 단가
            - "current_price": 현재 가격 (Optional)
    
    Returns:
        {
            "total_valuation": 총 평가액,
            "total_profit_loss": 총 손익,
            "total_invested": 총 투자 원금,
            "portfolio_return_rate": 포트폴리오 수익률 (원금 가중)
        }
    """
    total_valuation = Decimal("0")
    total_profit_loss = Decimal("0")
    total_invested = Decimal("0")
    
    for position in positions:
        quantity = Decimal(str(position.get("quantity", 0)))
        buy_price = Decimal(str(position.get("buy_price", 0)))
        current_price = position.get("current_price")
        
        # 총 투자 원금 계산
        invested = buy_price * quantity
        total_invested += invested
        
        if current_price is not None and buy_price > 0:
            current_price_decimal = Decimal(str(current_price))
            
            # 총 평가액 계산
            valuation = current_price_decimal * quantity
            total_valuation += valuation
            
            # 총 손익 계산
            profit_loss = (current_price_decimal - buy_price) * quantity
            total_profit_loss += profit_loss
    
    # 포트폴리오 수익률 계산 (원금 가중 수익률)
    # portfolio_return_rate = ((total_valuation - total_invested) / total_invested) * 100
    portfolio_return_rate = None
    if total_invested > 0:
        portfolio_return_rate = float(
            ((total_valuation - total_invested) / total_invested) * Decimal("100")
        )
        portfolio_return_rate = round(portfolio_return_rate, 2)
    
    return {
        "total_valuation": float(total_valuation) if total_valuation > 0 else None,
        "total_profit_loss": float(total_profit_loss),
        "total_invested": float(total_invested) if total_invested > 0 else None,
        "portfolio_return_rate": portfolio_return_rate
    }

