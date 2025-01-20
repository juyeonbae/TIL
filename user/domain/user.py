from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str  # 리소스 구분자 
    name: str
    email: str
    password: str
    memo: str | None  # 시스템 관리자가 유저에 대한 정보를 남기고 싶을 때 메모 
    created_at: datetime
    updated_at: datetime


