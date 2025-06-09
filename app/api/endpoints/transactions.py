from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.repository.session import get_db
from app.utils.auth import get_current_user
from app.service.transaction_service import get_transactions as tx_service

router = APIRouter()

@router.get("/get_transactions")
def get_transactions(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    gram_min: int | None = Query(None, ge=0),
    gram_max: int | None = Query(None, ge=0),
    search: str | None = Query(None),
    sort_by: str = Query("id"),  # "id", "date", "gram"
    sort_order: str = Query("desc"),  # "asc", "desc"
):
    return tx_service(
        db,
        page=page,
        per_page=per_page,
        date_from=date_from,
        date_to=date_to,
        gram_min=gram_min,
        gram_max=gram_max,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
