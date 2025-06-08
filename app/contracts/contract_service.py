from web3 import Web3
import json
from app.config import settings
from eth_abi import decode

web3 = Web3(Web3.HTTPProvider(settings.blockchain_rpc_url))
contract_address = settings.contract_address

with open('app/contracts/abi/FNFTCertABI.json') as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)

def create_new_certificate_onchain(metadata: str):
    wallet_address = settings.wallet_address
    private_key = settings.wallet_private_key

    nonce = web3.eth.get_transaction_count(wallet_address)
    txn = contract.functions.create_new_cert(json.dumps(metadata)).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Get NFT ID
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    event_signature_hash = web3.keccak(text="CertificateCreated(uint256)").hex()
    nft_id = None

    for log in receipt.logs:
        if log.topics[0].hex() == event_signature_hash:
            nft_id = Web3.to_int(log.data)
            break

    return web3.to_hex(tx_hash), nft_id

def create_new_fnft_onchain(nft_id: int, token_name: str, token_symbol: str, total_supply: int):
    wallet_address = settings.wallet_address
    private_key = settings.wallet_private_key

    nonce = web3.eth.get_transaction_count(wallet_address)
    txn = contract.functions.create_new_fnft(nft_id, token_name, token_symbol, total_supply).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    event_signature_hash = web3.keccak(text="FNFTCreated(uint256,string,string,uint256,address)").hex()

    erc20_address = None

    for log in receipt.logs:
        if log.topics[0].hex() == event_signature_hash:
            decoded = decode(
                ['uint256', 'string', 'string', 'uint256', 'address'],
                bytes(log.data)  # strip "0x" and decode hex
            )
            erc20_address = decoded[4]
            break

    return web3.to_hex(tx_hash), erc20_address


def approve_fnft_spending(erc20_address: str, amount=0):
    wallet_address = settings.wallet_address
    private_key = settings.wallet_private_key

    erc20_abi = [
        {
            "constant": False,
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        }
    ]

    erc20_contract = web3.eth.contract(
        address=Web3.to_checksum_address(erc20_address),
        abi=erc20_abi
    )

    if amount == 0:
        # ✅ 1. totalSupply kadar onay ver
        amount = erc20_contract.functions.totalSupply().call()
    else:
        amount = amount

    nonce = web3.eth.get_transaction_count(wallet_address)

    txn = erc20_contract.functions.approve(
        Web3.to_checksum_address(settings.contract_address),  # spender = Router
        amount
    ).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status != 1:
        raise Exception("Approve transaction failed")

    return tx_hash.hex()


def redeem_all_nft_with_fnft_onchain(erc20_address: str):
    wallet_address = settings.wallet_address
    private_key = settings.wallet_private_key

    # ✅ 1. Önce approve ver
    approve_fnft_spending(erc20_address)

    # ✅ 2. Sonra redeem işlemi
    nonce = web3.eth.get_transaction_count(wallet_address)
    txn = contract.functions.redeem_all_nft_with_fnft(Web3.to_checksum_address(erc20_address)).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    event_signature_hash = web3.keccak(text="Redeemed(address,uint256)").hex()
    token_id = None

    for log in receipt.logs:
        if log["topics"][0].hex() == event_signature_hash:
            token_id = Web3.to_int(log["data"])

    return {
        "tx_hash": web3.to_hex(tx_hash),
        "token_id": token_id
    }

def merge_fnft_onchain(erc20_addresses: list[str], amounts: list[int], metadata: str, is_sbt: bool):
    wallet_address = settings.wallet_address
    private_key = settings.wallet_private_key

    for i in range(len(erc20_addresses)):
        erc20_addresses[i] = Web3.to_checksum_address(erc20_addresses[i])
        approve_fnft_spending(erc20_addresses[i], amounts[i])

    nonce = web3.eth.get_transaction_count(wallet_address)

    txn = contract.functions.merge_fnft(
        erc20_addresses,
        amounts,
        metadata,
        is_sbt
    ).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 3000000,
        'gasPrice': web3.to_wei('5', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # 🔎 Receipt ile FNFTMerged eventini dinle
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    event_signature = web3.keccak(text="FNFTMerged(uint256,bool)").hex()

    token_id = None
    is_sbt_value = None

    for log in receipt.logs:
        if log["topics"][0].hex() == event_signature:
            decoded = decode(['uint256', 'bool'], bytes(log["data"]))
            token_id = decoded[0]
            is_sbt_value = decoded[1]
            break

    if token_id is None:
        raise Exception("FNFTMerged event not found")

    return {
        "tx_hash": web3.to_hex(tx_hash),
        "token_id": token_id,
        "is_sbt": is_sbt_value
    }
