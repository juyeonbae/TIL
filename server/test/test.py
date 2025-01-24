import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from user.application.email_service import EmailService
from user.application.user_service import UserService
from utils.crypto import Crypto
from common.auth import Role

# 필요한 객체들 생성
user_repo = UserRepository()

# ID로 사용자 삭제
user_repo.delete("01JJ8W1EA4P87S29BFX45TVR8B")

'''
# 필요한 의존성 객체들 생성
crypto = Crypto()
user_repo = UserRepository()  
email_service = EmailService()

# UserService 인스턴스 생성
user_service = UserService(
    user_repo=user_repo,
    crypto=crypto,
    email_service=email_service
)

# UserService를 통해 관리자 생성
admin = user_service.create_user(
    name="",
    email="",
    password="",
    role=Role.ADMIN
)
'''