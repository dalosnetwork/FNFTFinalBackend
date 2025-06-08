from sqlalchemy import Column, Integer, String
from app.repository.session import Base

class LoginInfo(Base):
    __tablename__ = "login_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    two_fa_key = Column(String, nullable=False)
    api_key = Column(String, nullable=True)
