import pyotp

def generate_2fa_secret() -> str:
    """
    Rastgele bir Google Authenticator secret üretir.

    Returns:
        str: Base32 ile encode edilmiş secret key
    """
    return pyotp.random_base32()

# Direkt çalıştırıldığında
if __name__ == "__main__":
    secret = generate_2fa_secret()
    print(f"[SECRET] {secret}")
