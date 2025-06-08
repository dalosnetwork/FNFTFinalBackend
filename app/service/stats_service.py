from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.models.certificate import Certificate
from app.models.transaction import Transaction
from app.models.merge import Merge


def get_stats(db: Session) -> dict:
    """Toplu istatistikleri üretir."""
    total_certificates = db.query(func.count(Certificate.id)).scalar() or 0
    total_gram = db.query(func.coalesce(func.sum(Certificate.gram), 0)).scalar() or 0
    total_transactions = db.query(func.count(Transaction.id)).scalar() or 0
    unique_customers = db.query(func.count(distinct(Merge.customer_id))).scalar() or 0

    return {
        "total_certificates": total_certificates,
        "total_gram": total_gram,
        "total_transactions": total_transactions,
        "unique_customers": unique_customers,
    }
