from ....db.models.users import User , UserCreate
from sqlalchemy.orm import Session

class UserRepository:  # check login & password
    def __init__(self) -> None:
        
        pass


    async def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()


    async def get_user_by_email(db: Session, email: str): #check user  in db by email
        return db.query(User).filter(User.email == email).first()


    async def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()


    async def create_user(db: Session, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


