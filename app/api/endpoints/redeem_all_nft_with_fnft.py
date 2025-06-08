from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from web3 import Web3

from app.utils.auth import get_current_user
from app.repository.session import get_db
from app.contracts.contract_service import redeem_all_nft_with_fnft_onchain

from app.repository.transaction_repository import TransactionRepository

router = APIRouter()

class RedeemRequest(BaseModel):
    erc20_address: str

@router.post("/redeem_nft_with_fnft")
def redeem_nft(request: RedeemRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        checksum_address = Web3.to_checksum_address(request.erc20_address)
        result = redeem_all_nft_with_fnft_onchain(checksum_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")


    TransactionRepository(db).log(
        action="redeem_all_nft_with_fnft", tx_id=result["tx_hash"]
    )

    return {
        "message": "NFT redeemed successfully",
        "tx_hash": result["tx_hash"],
        "token_id": result["token_id"]
    }
