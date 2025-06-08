from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.repository.session import Base, engine
from app.api.endpoints import (
    login,
    login_with_api,
    create_fnft,
    redeem_all_nft_with_fnft,
    merge_fnft,
    stats,
    transactions,
    certificates,
)

app = FastAPI(title="FNFT API", version="1.0.0", docs_url="/fnft-swagger")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ----------------- Router kayıtları -----------------
app.include_router(login.router, tags=["Login"])
app.include_router(login_with_api.router, tags=["Login With API"])
app.include_router(create_fnft.router, tags=["Create FNFT"])
app.include_router(redeem_all_nft_with_fnft.router, tags=["Redeem All NFT with FNFT"])
app.include_router(merge_fnft.router, tags=["Merge FNFT"])
app.include_router(stats.router, tags=["Stats"])
app.include_router(transactions.router, tags=["Transactions"])
app.include_router(certificates.router, tags=["Certificates"])
# ----------------------------------------------------


@app.get("/api-docs", response_class=HTMLResponse, include_in_schema=False)
def custom_docs():
    """Statik HTML – tüm endpoint kullanım örnekleri."""
    return """
    <html>
    <head>
        <title>FNFT API Dökümanı</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                max-width: 960px;
                margin: auto;
                padding: 40px 30px;
                background-color: #f9fafb;
                color: #2c3e50;
                line-height: 1.6;
            }
            h1 { font-size: 2em; border-bottom: 2px solid #eaecef; padding-bottom: 0.3em; }
            h2 { color: #1e3a8a; margin-top: 2em; }
            h3 { color: #0f172a; }
            code {
                background: #e2e8f0;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 0.95em;
            }
            pre {
                background-color: #f3f4f6;
                padding: 12px;
                border-radius: 8px;
                overflow-x: auto;
                font-size: 0.9em;
                border: 1px solid #e5e7eb;
            }
            ul { padding-left: 20px; }
            hr {
                margin: 50px 0;
                border: none;
                border-top: 1px solid #d1d5db;
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>📖 FNFT REST API – Hızlı Rehber</h1>
        <p>Swagger: <a href="/fnft-swagger" target="_blank">/fnft-swagger</a></p>
        <p><strong>⚠️ Not:</strong> Tüm korumalı endpoint’lerde <code>Authorization: Bearer &lt;jwt&gt;</code> başlığı zorunludur.</p>

        <hr>

        <h2>🔐 1. Token Al</h2>
        <h3>1.1 API Anahtarıyla</h3>
        <p><strong>POST</strong> <code>/login_with_api</code></p>
        <pre>{
  "api_key": "YOUR_API_KEY"
}</pre>
        <h4>Yanıt</h4>
        <pre>{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}</pre>

        <h3>1.2 Kullanıcı Adı / Şifre / 2FA</h3>
        <p><strong>POST</strong> <code>/login</code></p>
        <pre>{
  "username": "alice",
  "password": "sha256lenmiş_parola",
  "two_fa_code": "123456"
}</pre>

        <hr>

        <h2>🧩 2. FNFT Operasyonları</h2>

        <h3>2.1 FNFT Oluştur</h3>
        <p><strong>POST</strong> <code>/create_fnft</code></p>
        <pre>{
  "name": "Altın FNFT",
  "description": "1 gram altın teminatlı",
  "token_name": "GOLDFNFT",
  "token_symbol": "GFN",
  "total_supply": 1000,
  "metadata": "ipfs://Qm..."
}</pre>

        <h3>2.2 FNFT’leri Birleştir</h3>
        <p><strong>POST</strong> <code>/merge_fnft</code></p>
        <pre>{
  "name": "Birleşik FNFT",
  "description": "Portföy birleştirme",
  "customer_id": 42,
  "erc20_addresses": ["0xAbc...", "0xDef..."],
  "amounts": [100, 200],
  "metadata": "ipfs://Qm...",
  "isSBT": false
}</pre>

        <h3>2.3 FNFT ile NFT Geri Al</h3>
        <p><strong>POST</strong> <code>/redeem_nft_with_fnft</code></p>
        <pre>{
  "erc20_address": "0xAbc..."
}</pre>

        <hr>

        <h2>📊 3. Analitik & Listeleme</h2>

        <h3>3.1 Genel İstatistikler</h3>
        <p><strong>GET</strong> <code>/get_stats</code></p>
        <h4>Örnek Yanıt</h4>
        <pre>{
  "total_certificates": 18,
  "total_gram": 24500,
  "total_transactions": 31,
  "unique_customers": 7
}</pre>

        <h3>3.2 İşlem (Merge) Listesi</h3>
        <p><strong>GET</strong> <code>/get_transactions</code></p>
        <p><u>Sorgu parametreleri</u>:</p>
        <ul>
            <li><code>page</code> (>=1, varsayılan 1)</li>
            <li><code>per_page</code> (<=100, varsayılan 10)</li>
            <li><code>date_from / date_to</code> → ISO tarih (YYYY-MM-DD)</li>
            <li><code>gram_min / gram_max</code> → int</li>
            <li><code>search</code> → herhangi bir metin (tx_id, adres, vs)</li>
        </ul>
        <h4>Örnek</h4>
        <code>/get_transactions?page=1&search=0xAbc&gram_min=500</code>

        <h4>Örnek Yanıt</h4>
        <pre>{
  "page": 1,
  "per_page": 10,
  "total_pages": 2,
  "total_items": 15,
  "data": [
    {
      "id": 9,
      "date": "2025-06-03T12:34:56",
      "gram": 750,
      "certificate": ["0xAbc...", "0xDef..."],
      "tx_id": "0xF123...",
      "customer_id": 42
    }
  ]
}</pre>

        <h3>3.3 Sertifika Listesi</h3>
        <p><strong>GET</strong> <code>/get_certificates</code></p>
        <p><u>Sorgu parametreleri</u>: <code>page</code>, <code>per_page</code>, <code>date_from</code>, <code>date_to</code>, <code>gram_min</code>, <code>gram_max</code>, <code>search</code></p>
        <h4>Örnek</h4>
        <code>/get_certificates?page=2&gram_max=1000&search=0xabc</code>

        <h4>Örnek Yanıt</h4>
        <pre>{
  "page": 2,
  "per_page": 10,
  "total_pages": 3,
  "total_items": 22,
  "data": [
    {
      "id": 17,
      "gram": 500,
      "nft_id": 101,
      "erc20_address": "0xAbc...",
      "date": "2025-05-30T09:12:00"
    }
  ]
}</pre>

        <hr>

        <h2>🔧 Ek Bilgiler</h2>
        <ul>
            <li>Tüm yanıtlar <code>application/json</code>.</li>
            <li>Hata durumunda HTTP kodu + <code>{"detail": "mesaj"}</code> formatı gönderilir.</li>
            <li>Gerçek <em>on-chain</em> işlemler için <code>tx_id</code> sahası Ethereum tx hash’idir.</li>
        </ul>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7070, reload=True)
