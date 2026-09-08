from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import UserORM

class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get(self, user_id: int) -> UserORM | None:    
        # user_find = (
        #     select(UserORM)
        #     .where(UserORM.id == user_id)
        # )
        # return self.db.execute(user_find).scalar_one_or_none()
        return self.db.get(UserORM, user_id)
    
    def get_user_by_email(self, email: str) -> UserORM | None:
        user_find = (
            select(UserORM)
            .where(UserORM.email == email)
        )
        return self.db.execute(user_find).scalar_one_or_none()
    
    def create_user(self, email: str, hashed_password: str, full_name: str | None) -> UserORM:
        new_user = UserORM(email=email, hashed_password=hashed_password, full_name=full_name)
        
        self.db.add(new_user)
        self.db.flush()
        self.db.refresh(new_user)
        return new_user
        
    def set_role(self, user: UserORM, role: str) -> UserORM:
        user.role = role
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user