from passlib.context import CryptContext


"""
[패스워드 암호화]
$ poetry add "passlib[bcrypt]" # PassLib 패키지 & Bcrypt 암호화 알고리즘 사용 

Passlib를 이용해 평문을 암호화
암호화된 문자열이 주어진 평문에서 생성된 것인지 검증하는 모듈 구현
"""

class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, secret):
        return self.pwd_context.hash(secret)
    
    def verify(self, secret, hash):
        return self.pwd_context.verify(secret, hash)

        