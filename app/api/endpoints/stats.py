from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repository.session import get_db
from app.utils.auth import get_current_user
from app.service.stats_service import get_stats as stats_service

router = APIRouter()


@router.get("/get_stats")
def get_stats(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return stats_service(db)
