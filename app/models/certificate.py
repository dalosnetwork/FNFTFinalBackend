from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.repository.session import Base


class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gram = Column(Integer, nullable=False)
    nft_id = Column(Integer, nullable=False, index=True)
    erc20_address = Column(String, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
