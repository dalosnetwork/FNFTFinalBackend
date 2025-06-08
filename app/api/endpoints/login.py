from fastapi import APIRouter, Depends, HTTPException
from app.repository.login_repository import LoginRepository
from app.utils.helpers import create_access_token
from app.utils.auth import get_current_user
from pydantic import BaseModel
from app.repository.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    two_fa_code: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    repo = LoginRepository(db)

    user = repo.authenticate_user(
        username=request.username,
        password=request.password,
        two_fa_code=request.two_fa_code
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials or 2FA")

    token = create_access_token(user_id=user.id)
    return {"access_token": token}

