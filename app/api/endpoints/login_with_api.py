from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.repository.session import get_db
from app.repository.login_with_api_repository import LoginWithApiRepository
from app.utils.helpers import create_access_token

router = APIRouter()

class ApiLoginRequest(BaseModel):
    api_key: str

@router.post("/login_with_api")
def login_with_api(
    request: ApiLoginRequest,
    db: Session = Depends(get_db)
):
    repo = LoginWithApiRepository(db)
    user_id = repo.authenticate_by_api_key(request.api_key)

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid API key")

    token = create_access_token(user_id=user_id)
    return {"access_token": token}
