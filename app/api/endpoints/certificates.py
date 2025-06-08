from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.repository.session import get_db
from app.utils.auth import get_current_user
from app.service.certificate_service import get_certificates as cert_service

router = APIRouter()


@router.get("/get_certificates")
def get_certificates(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    gram_min: int | None = Query(None, ge=0),
    gram_max: int | None = Query(None, ge=0),
    search: str | None = Query(None),
):
    return cert_service(
        db,
        page=page,
        per_page=per_page,
        date_from=date_from,
        date_to=date_to,
        gram_min=gram_min,
        gram_max=gram_max,
        search=search,
    )
