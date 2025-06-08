from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.repository.session import Base


class Merge(Base):
    """merge_fnft → çoklu ERC-20 birleşimi kaydı"""
    __tablename__ = "merges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tx_id = Column(String, nullable=False, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    erc20_address = Column(String, nullable=False)     # virgülle ayrılmış liste
    amounts = Column(String, nullable=False)           # virgülle ayrılmış liste
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
