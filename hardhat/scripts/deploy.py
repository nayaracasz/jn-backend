import json
import os
from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware


load_dotenv()

def deploy():
    sepolia = Web3(Web3.HTTPProvider(os.getenv("API_KEY")))
    sepolia.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    private_key = os.getenv("TEST_PRIVATE_KEY")
    account = Account.from_key(private_key)

    abi_path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', 'contracts', 'Ticket.sol', 'Ticket.json')
    with open(os.path.abspath(abi_path)) as f:
        artifact = json.load(f)

    abi = artifact["abi"]
    bytecode = artifact["bytecode"]

    contract = sepolia.eth.contract(abi=abi, bytecode=bytecode)

    gas_estimate = contract.constructor().estimate_gas({
        "from": account.address
    })
    gas_limit = int(gas_estimate * 1.2)

    tx = contract.constructor().build_transaction({
        "from": account.address,
        "nonce": sepolia.eth.get_transaction_count(account.address),
        "gas": gas_limit,
        "gasPrice": sepolia.to_wei('20', 'gwei')
    })

    signed_tx = sepolia.eth.account.sign_transaction(tx, private_key)
    tx_hash = sepolia.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = sepolia.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract deployed at address: {receipt.contractAddress}")

if __name__ == "__main__":
    deploy()