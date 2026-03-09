from abc import ABC, abstractmethod
from typing import List, BinaryIO
from fastapi import UploadFile
from app.src.schemas.transaction_common import CommonTransaction

class BaseParser(ABC):
    """
    파서 엔진의 플러그인 인터페이스.
    모든 증권사 전용 파서는 이 클래스를 상속받아 구현해야 향후 엔진이 동적으로 로드 및 실행할 수 있습니다.
    """
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        플러그인 고유 식별자 (예: 'toss', 'kiwoom', 'common_csv')
        어떤 증권사의 파일인지 구분하는 용도로 사용됩니다.
        """
        pass
        
    @abstractmethod
    async def parse(self, file: UploadFile, **kwargs) -> List[CommonTransaction]:
        """
        업로드된 파일을 읽어 공통 포맷(`CommonTransaction`)의 리스트로 변환합니다.
        
        Args:
            file (UploadFile): 사용자가 업로드한 원본 파일 객체
            **kwargs: 비밀번호, 옵션 파라미터 등
            
        Returns:
            List[CommonTransaction]: 공통 양식으로 변환된 거래내역 리스트
            
        Raises:
            ValueError: 변환 실패나 지원하지 않는 파일 형식인 경우 예외 발생
        """
        pass
