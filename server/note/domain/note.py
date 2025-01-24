from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tag:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Note:
    id: str
    user_id: str  # 어떤 유저가 작성한 것인지 구분 필요
    title: str
    content: str
    memo_date: str
    tags: list[Tag]
    created_at: datetime
    updated_at: datetime
