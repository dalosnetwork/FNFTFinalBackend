from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from datetime import datetime
from typing import List, Dict

from app.models.merge import Merge


def _str_to_date(date_str: str | None) -> datetime | None:
    if date_str:
        return datetime.fromisoformat(date_str)
    return None


def get_transactions(
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
    """Merge işlemlerini filtre + arama + sıralama + pagination ile döner."""
    q = db.query(Merge)

    # tarih filtreleri
    dt_from = _str_to_date(date_from)
    dt_to = _str_to_date(date_to)
    if dt_from:
        q = q.filter(Merge.date >= dt_from)
    if dt_to:
        q = q.filter(Merge.date <= dt_to)

    # search filtresi
    if search:
        search_like = f"%{search.lower()}%"
        q = q.filter(
            or_(
                cast(Merge.id, String).ilike(search_like),
                cast(Merge.date, String).ilike(search_like),
                cast(Merge.amounts, String).ilike(search_like),
                cast(Merge.erc20_address, String).ilike(search_like),
                cast(Merge.tx_id, String).ilike(search_like),
                cast(Merge.customer_id, String).ilike(search_like),
            )
        )

    all_items: List[Merge] = q.all()

    results: List[Dict] = []
    for m in all_items:
        amounts_list = list(map(int, m.amounts.split(",")))
        gram_total = sum(amounts_list)

        # gram aralığı filtrelemesi
        if gram_min is not None and gram_total < gram_min:
            continue
        if gram_max is not None and gram_total > gram_max:
            continue

        results.append(
            {
                "id": m.id,
                "date": m.date,
                "gram": gram_total,
                "certificate": m.erc20_address.split(","),
                "tx_id": m.tx_id,
                "customer_id": m.customer_id,
            }
        )

    # sıralama
    reverse = sort_order.lower() == "desc"

    if sort_by == "date":
        results.sort(key=lambda x: x["date"], reverse=reverse)
    elif sort_by == "gram":
        results.sort(key=lambda x: x["gram"], reverse=reverse)
    else:  # default to id
        results.sort(key=lambda x: x["id"], reverse=True)

    total_items = len(results)
    total_pages = (total_items + per_page - 1) // per_page
    paged_results = results[(page - 1) * per_page : page * per_page]

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_items": total_items,
        "data": paged_results,
    }
