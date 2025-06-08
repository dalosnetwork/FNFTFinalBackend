from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.utils.auth import get_current_user
from app.repository.session import get_db
from app.contracts.contract_service import merge_fnft_onchain

from app.repository.merge_repository import MergeRepository
from app.repository.transaction_repository import TransactionRepository

router = APIRouter()

class MergeRequest(BaseModel):
    name: str
    description: str
    customer_id: int
    erc20_addresses: List[str]
    amounts: List[int]
    metadata: str
    isSBT: bool

@router.post("/merge_fnft")
def redeem_nft(request: MergeRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = merge_fnft_onchain(request.erc20_addresses, request.amounts, request.metadata, request.isSBT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")

    # merges tablosu
    MergeRepository(db).create_merge(
            tx_id=result["tx_hash"],
            customer_id=request.customer_id,
            erc20_address=",".join(request.erc20_addresses),
            amounts=",".join(map(str, request.amounts)),
        )

    # Genel transactions tablosu
    TransactionRepository(db).log(action="merge_fnft", tx_id=result["tx_hash"])

    return {
        "message": "NFT redeemed successfully",
        "metadata": request.metadata,
        "isSBT": request.isSBT,
        "tx_hash": result["tx_hash"],
        "token_id": result["token_id"]
    }
