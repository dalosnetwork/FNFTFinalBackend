import pyotp
from app.repository.base_repository import BaseRepository
from app.models.login_info import LoginInfo

class LoginRepository(BaseRepository):
    def __init__(self, db):
        self.model = LoginInfo
        super().__init__(db)

    def authenticate_user(self, username: str, password: str, two_fa_code: str):
        user = self.db.query(LoginInfo).filter_by(username=username, password=password).first()
        if not user:
            return None

        # 2FA doğrulama
        if not pyotp.TOTP(user.two_fa_key).verify(two_fa_code):
            return None

        return user

    def authenticate_by_api_key(self, api_key: str):
        return self.db.query(LoginInfo).filter_by(api_key=api_key).first()
