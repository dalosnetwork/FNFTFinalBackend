from app.repository.base_repository import BaseRepository
from app.models.transaction import Transaction


class TransactionRepository(BaseRepository):
    def __init__(self, db):
        self.model = Transaction
        super().__init__(db)

    def log(self, *, action: str, tx_id: str):
        return self.create(action=action, tx_id=tx_id)
