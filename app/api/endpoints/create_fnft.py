from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.utils.auth import get_current_user
from app.repository.session import get_db
from app.contracts.contract_service import (
    create_new_certificate_onchain,
    create_new_fnft_onchain,
)

from app.repository.certificate_repository import CertificateRepository
from app.repository.transaction_repository import TransactionRepository

router = APIRouter()

class FNFTRequest(BaseModel):
    name: str
    description: str
    token_name: str
    token_symbol: str
    total_supply: int
    metadata: str

@router.post("/create_fnft")
def create_fnft(request: FNFTRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    nft_tx_hash, nft_id = create_new_certificate_onchain(request.metadata)

    try:
        fnft_tx_hash, erc20_address = create_new_fnft_onchain(
            nft_id=nft_id,
            token_name=request.token_name,
            token_symbol=request.token_symbol,
            total_supply=request.total_supply
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")

    # certificates tablosu
    CertificateRepository(db).create_certificate(
        gram=request.total_supply,
        nft_id=nft_id,
        erc20_address=erc20_address,
    )

    # Genel transactions tablosu
    TransactionRepository(db).log(action="create_fnft", tx_id=fnft_tx_hash)

    return {"message": "FNFT created successfully", "fnft_tx_hash": fnft_tx_hash,
            "metadata": request.metadata, "nft_tx_hash": nft_tx_hash,
            "nft_id": nft_id,
            "erc20_address": erc20_address}
