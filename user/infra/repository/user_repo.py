from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO  # 데이터베이스 모델과 클래스명 동일 
from user.infra.db_models.user import User

from fastapi import HTTPException
from utils.db_utils import row_to_dict

class UserRepository(IUserRepository):
    def save(self, user: UserVO):
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        
        # 세션 객체를 생성해서 사용할 때 세션이 자동으로 닫히도록 한다. (데베에 에러가 발생했을 때 세션이 제대로 안 닫힐 수 있기 때문)
        with SessionalLocal() as db:
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()
            
    def find_by_email(self, email:str) -> UserVO:
        with SesionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
            
        if not user:
            raise HTTPException(status_code=422)
        
        return UserVO(**row_to_dict(user))