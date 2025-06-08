from app.repository.base_repository import BaseRepository
from app.models.merge import Merge


class MergeRepository(BaseRepository):
    def __init__(self, db):
        self.model = Merge
        super().__init__(db)

    def create_merge(
        self,
        *,
        tx_id: str,
        customer_id: int,
        erc20_address: str,
        amounts: str,
    ):
        return self.create(
            tx_id=tx_id,
            customer_id=customer_id,
            erc20_address=erc20_address,
            amounts=amounts,
        )
