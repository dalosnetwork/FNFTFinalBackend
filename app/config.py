import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 🔥 .env dosyasını bulunduğu yerden kesin olarak yükle
env_path = os.path.join(os.path.dirname(__file__), ".env")
print("[DEBUG] ENV path:", env_path)
print("[DEBUG] ENV exists:", os.path.exists(env_path))
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    blockchain_rpc_url: str
    contract_address: str
    wallet_address: str
    wallet_private_key: str

    class Config:
        env_file = env_path  # ← burada da tam yolu veriyoruz

settings = Settings()
