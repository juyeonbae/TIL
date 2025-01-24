from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from enum import StrEnum

from dataclasses import dataclass
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from config import get_settings

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


def create_access_token(
    payload: dict,
    role: Role,
    expires_delta: timedelta = timedelta(hours=6),
):
    # python 3.12 버전부터 utcnow() 사용 X
    # expire = datetime.now(timezone.utc) + expires_delta
    expire = datetime.utcnow() + expires_delta
    payload.update(
        {   
            "role": role,
            "exp": expire,
        }
    )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    


@dataclass
class CurrentUser:
    id: str
    role: Role

    # LogRecord 객체의 user 속성은 log_format에서 사용되는 문자열이므로, 
    # 콘텍스트 변수에서 가져온 CurrentUser 객체를 문자열로 변환해주어야 한다. 
    def __str__(self):
        return f"{self.id}({self.role})"
    

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")
    if not user_id or not role or (role != Role.USER and role != Role.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return CurrentUser(user_id, Role(role))


def get_admin_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)

    role = payload.get("role")
    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return CurrentUser("ADMIN_USER_ID", role)