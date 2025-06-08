from fastapi import APIRouter, Depends, HTTPException
from app.repository.login_repository import LoginRepository
from app.utils.helpers import create_access_token
from pydantic import BaseModel

router = APIRouter()

class ApiLoginRequest(BaseModel):
    api_key: str

@router.post("/login_with_api")
#def login_with_api(request: ApiLoginRequest, repo: LoginRepository = Depends()):
def login_with_api(request: ApiLoginRequest):
    # Close if when production
    if request.api_key == "EQKJUEDC324BFDSGFDS":
        #user = repo.authenticate_by_api_key(api_key=request.api_key)
        user = 1
    else:
        raise HTTPException(status_code=400, detail="Invalid API key")

    #if not user:
    #    raise HTTPException(status_code=400, detail="Invalid API key")

    #token = create_access_token(user_id=user.id)
    token = create_access_token(user_id=user)
    return {"access_token": token}
