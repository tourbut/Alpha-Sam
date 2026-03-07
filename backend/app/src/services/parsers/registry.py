from typing import Dict, Type
from app.src.schemas.transaction_common import CommonTransaction
from app.src.services.parsers.base import BaseParser

class ParserEngine:
    """
    다양한 BaseParser 플러그인을 관리하고 동적으로 제공하는 엔진(Registry).
    새로운 파서를 만들면 이곳에 등록합니다.
    """
    _parsers: Dict[str, BaseParser] = {}

    @classmethod
    def register_parser(cls, parser_instance: BaseParser) -> None:
        """
        엔진에 파서 인스턴스를 등록합니다.
        보통 앱 시작 시(startup)나 파서 모듈 임포트 시 호출됩니다.
        """
        cls._parsers[parser_instance.provider_name] = parser_instance

    @classmethod
    def get_parser(cls, provider: str) -> BaseParser:
        """
        provider_name(제공자) 이름으로 파서를 가져옵니다.
        
        Raises:
            ValueError: 등록되지 않은(지원하지 않는) provider인 경우
        """
        parser = cls._parsers.get(provider)
        if not parser:
            raise ValueError(f"지원하지 않는 거래내역 포맷 또는 증권사입니다: {provider}")
        return parser

    @classmethod
    def list_providers(cls) -> list[str]:
        """등록된 모든 파서 식별자 목록을 반환합니다."""
        return list(cls._parsers.keys())
