from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from datetime import datetime
from typing import List, Dict

from app.models.certificate import Certificate


def _str_to_date(date_str: str | None) -> datetime | None:
    if date_str:
        return datetime.fromisoformat(date_str)
    return None


def get_certificates(
    db: Session,
    *,
    page: int,
    per_page: int,
    date_from: str | None,
    date_to: str | None,
    gram_min: int | None,
    gram_max: int | None,
    search: str | None,
    sort_by: str,
    sort_order: str,
) -> dict:
    """Certificate kayıtlarını filtre + arama + sıralama + pagination ile döner."""
    q = db.query(Certificate)

    # tarih filtreleri
    dt_from = _str_to_date(date_from)
    dt_to = _str_to_date(date_to)
    if dt_from:
        q = q.filter(Certificate.date >= dt_from)
    if dt_to:
        q = q.filter(Certificate.date <= dt_to)

    # gram filtreleri
    if gram_min is not None:
        q = q.filter(Certificate.gram >= gram_min)
    if gram_max is not None:
        q = q.filter(Certificate.gram <= gram_max)

    # search filtresi (tüm sütunlarda arama)
    if search:
        search_like = f"%{search.lower()}%"
        q = q.filter(
            or_(
                cast(Certificate.id, String).ilike(search_like),
                cast(Certificate.gram, String).ilike(search_like),
                cast(Certificate.nft_id, String).ilike(search_like),
                Certificate.erc20_address.ilike(search_like),
                cast(Certificate.date, String).ilike(search_like),
            )
        )

    # sıralama dinamik
    sort_by_field = {
        "id": Certificate.id,
        "date": Certificate.date,
        "gram": Certificate.gram,
    }.get(sort_by, Certificate.id)

    if sort_order == "asc":
        q = q.order_by(sort_by_field.asc())
    else:
        q = q.order_by(sort_by_field.desc())

    total_items = q.count()
    total_pages = (total_items + per_page - 1) // per_page

    items: List[Certificate] = (
        q.offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    results: List[Dict] = [
        {
            "id": c.id,
            "gram": c.gram,
            "nft_id": c.nft_id,
            "erc20_address": c.erc20_address,
            "date": c.date,
        }
        for c in items
    ]

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_items": total_items,
        "data": results,
    }
