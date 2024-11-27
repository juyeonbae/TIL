from dataclasses import dataclass
from datetime import datetime

@dataclass  # 도메인 객체를 다루기 쉽도록 하기 위해 
class Profile:  # 값 객체: 데이터만 갖고 있는 도메인 객체
    name: str
    email: str

@dataclass
class User:
    id: str  # 리소스 구분자 
    profile: Profile
    password: str
    created_at: datetime
    updated_at: datetime


