from app.repository.base_repository import BaseRepository
from app.models.certificate import Certificate


class CertificateRepository(BaseRepository):
    def __init__(self, db):
        self.model = Certificate
        super().__init__(db)

    def create_certificate(self, *, gram: int, nft_id: int, erc20_address: str):
        return self.create(gram=gram, nft_id=nft_id, erc20_address=erc20_address)
