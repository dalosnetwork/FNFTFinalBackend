from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.repository.session import Base


class Transaction(Base):
    """Her kritik endpoint için tek satırlık özet"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String, nullable=False, index=True)   # 'create_fnft' / ...
    tx_id = Column(String, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
