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
            role=user.role,
            memo=user.memo
        )
        
        # 세션 객체를 생성해서 사용할 때 세션이 자동으로 닫히도록 한다. (데베에 에러가 발생했을 때 세션이 제대로 안 닫힐 수 있기 때문)
        with SessionLocal() as db:
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()
            
    def find_by_email(self, email:str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
            
        if not user:
            raise HTTPException(status_code=422)
        
        return UserVO(**row_to_dict(user))
    
    def find_by_id(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=422)
        
        return UserVO(**row_to_dict(user))
    
    def update(self, user_vo: UserVO):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()

            if not user:
                raise HTTPException(status_code=422)
            
            user.name = user_vo.name
            user.password = user_vo.password

            db.add(user)
            db.commit()

        return user
    
    def get_users(
            self,
            page: int = 1,
            items_per_page: int = 10,
            ) -> tuple[int, list[UserVO]]:
        with SessionLocal() as db:
            query = db.query(User)
            total_count = query.count()
            
            offset = (page - 1) * items_per_page
            users = query.limit(items_per_page).offset(offset).all()
            
        return total_count, [UserVO(**row_to_dict(user)) for user in users]
    

    def delete(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()
            
            if not user:
                raise HTTPException(status_code=404)
            
            db.delete(user)
            db.commit()