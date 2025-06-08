from web3 import Web3
import json
from eth_abi import decode
from app.config import settings

# Web3 bağlantısı
web3 = Web3(Web3.HTTPProvider(settings.blockchain_rpc_url))
contract_address = Web3.to_checksum_address(settings.contract_address)
wallet_address = Web3.to_checksum_address(settings.wallet_address)
private_key = settings.wallet_private_key

# Ana sözleşme
with open('app/contracts/abi/FNFTCertABI.json') as f:
    abi = json.load(f)
contract = web3.eth.contract(address=contract_address, abi=abi)

# ✅ Güncel nonce alma fonksiyonu
def get_fresh_nonce():
    return web3.eth.get_transaction_count(wallet_address, 'pending')

# ✅ Sertifika oluşturma
def create_new_certificate_onchain(metadata: str):
    nonce = get_fresh_nonce()
    txn = contract.functions.create_new_cert(json.dumps(metadata)).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    event_sig = web3.keccak(text="CertificateCreated(uint256)").hex()
    nft_id = next(
        (Web3.to_int(log.data) for log in receipt.logs if log.topics[0].hex() == event_sig),
        None
    )

    return web3.to_hex(tx_hash), nft_id

# ✅ FNFT oluşturma
def create_new_fnft_onchain(nft_id: int, name: str, symbol: str, supply: int):
    nonce = get_fresh_nonce()
    txn = contract.functions.create_new_fnft(nft_id, name, symbol, supply).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    event_sig = web3.keccak(text="FNFTCreated(uint256,string,string,uint256,address)").hex()
    for log in receipt.logs:
        if log.topics[0].hex() == event_sig:
            decoded = decode(['uint256', 'string', 'string', 'uint256', 'address'], bytes(log.data))
            return web3.to_hex(tx_hash), decoded[4]

    return web3.to_hex(tx_hash), None

# ✅ ERC20 approve işlemi
def approve_fnft_spending(erc20_address: str, amount: int = 0):
    erc20_abi = [
        {
            "name": "approve",
            "type": "function",
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "outputs": [{"name": "", "type": "bool"}],
            "constant": False
        },
        {
            "name": "totalSupply",
            "type": "function",
            "inputs": [],
            "outputs": [{"name": "", "type": "uint256"}],
            "constant": True
        }
    ]

    erc20 = web3.eth.contract(address=Web3.to_checksum_address(erc20_address), abi=erc20_abi)

    if amount == 0:
        amount = erc20.functions.totalSupply().call()

    nonce = get_fresh_nonce()
    txn = erc20.functions.approve(contract_address, amount).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status != 1:
        raise Exception("Approve transaction failed")

    return web3.to_hex(tx_hash)

# ✅ FNFT redeem işlemi
def redeem_all_nft_with_fnft_onchain(erc20_address: str):
    approve_fnft_spending(erc20_address)

    nonce = get_fresh_nonce()
    txn = contract.functions.redeem_all_nft_with_fnft(Web3.to_checksum_address(erc20_address)).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    event_sig = web3.keccak(text="Redeemed(address,uint256)").hex()
    token_id = next(
        (Web3.to_int(log.data) for log in receipt.logs if log.topics[0].hex() == event_sig),
        None
    )

    return {
        "tx_hash": web3.to_hex(tx_hash),
        "token_id": token_id
    }

# ✅ FNFT merge işlemi
def merge_fnft_onchain(erc20_addresses: list[str], amounts: list[int], metadata: str, is_sbt: bool):
    checksummed = [Web3.to_checksum_address(addr) for addr in erc20_addresses]

    for i, addr in enumerate(checksummed):
        approve_fnft_spending(addr, amounts[i])

    nonce = get_fresh_nonce()
    txn = contract.functions.merge_fnft(checksummed, amounts, metadata, is_sbt).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 3000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    event_sig = web3.keccak(text="FNFTMerged(uint256,bool)").hex()
    token_id = None
    sbt_flag = None

    for log in receipt.logs:
        if log.topics[0].hex() == event_sig:
            decoded = decode(['uint256', 'bool'], bytes(log.data))
            token_id = decoded[0]
            sbt_flag = decoded[1]
            break

    if token_id is None:
        raise Exception("FNFTMerged event not found")

    return {
        "tx_hash": web3.to_hex(tx_hash),
        "token_id": token_id,
        "is_sbt": sbt_flag
    }
