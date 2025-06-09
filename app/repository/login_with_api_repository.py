from sqlalchemy.orm import Session
from app.models.login_info import LoginInfo  # model adı buysa

class LoginWithApiRepository:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_by_api_key(self, api_key: str) -> int | None:
        user = self.db.query(LoginInfo).filter(LoginInfo.api_key == api_key).first()
        return user.id if user else None
