import json
import os
from dotenv import load_dotenv
from web3 import Web3


load_dotenv()

class TicketContract:
    def __init__(self):
        contract_address = os.getenv("CONTRACT_ADDRESS")
        api_key = os.getenv("API_KEY")
        self.private_key = os.getenv("TEST_PRIVATE_KEY")

        if not contract_address:
            raise ValueError("Missing CONTRACT_ADDRESS in .env")
        if not api_key:
            raise ValueError("Missing API_KEY in .env")
        if not self.private_key:
            raise ValueError("Missing PRIVATE_KEY in .env")

        self.sepolia = Web3(Web3.HTTPProvider(api_key))
        self.owner_address = self.sepolia.eth.account.from_key(self.private_key).address


        abi_path = os.path.join(os.path.dirname(__file__), '..', '..', 'hardhat', 'artifacts', 'contracts', 'Ticket.sol', 'Ticket.json')
        with open(os.path.abspath(abi_path)) as f:
            artifact = json.load(f)
        
        abi = artifact["abi"]

        self.contract = self.sepolia.eth.contract(
            address=contract_address,
            abi=abi
        )

    def mint_ticket(self, wallet_address: str, event_data: dict):
        gas_estimate = self.contract.functions.mintTicket(
            wallet_address,
            event_data['eventName'],
            event_data['date'],
            event_data['zone'],
            event_data['seat'],
            self.sepolia.to_wei(event_data['price'], 'ether')
        ).estimate_gas({
            "from": self.owner_address,
            "value": self.sepolia.to_wei(event_data['price'], 'ether')
        })

        gas_limit = int(gas_estimate * 1.2)

        nonce = self.sepolia.eth.get_transaction_count(self.owner_address)

        tx = self.contract.functions.mintTicket(
            wallet_address,
            event_data['eventName'],
            event_data['date'],
            event_data['zone'],
            event_data['seat'],
            self.sepolia.to_wei(event_data['price'], 'ether')
        ).build_transaction({
            "from": self.owner_address,
            "nonce": nonce,
            "gas": gas_limit,
            "gasPrice": self.sepolia.to_wei('10', 'gwei'),
            "value": self.sepolia.to_wei(event_data['price'], 'ether')
        })
        signed_tx = self.sepolia.eth.account.sign_transaction(tx, private_key=self.private_key)

        tx_hash = self.sepolia.eth.send_raw_transaction(signed_tx.raw_transaction)

        return tx_hash.hex()

    def get_user_tickets(self, wallet_address: str):
        wallet_address = Web3.to_checksum_address(wallet_address)
        print(f"Consultando tickets para: {wallet_address}")
        event_names, dates, zones, seats, prices = self.contract.functions.getUserTickets(wallet_address).call()

        print(f"Tickets obtenidos: {len(event_names)}")
        tickets = []
        for i in range(len(event_names)):
            ticket = {
                "eventName": event_names[i],
                "date": dates[i],
                "zone": zones[i],
                "seat": seats[i],
                "price": self.sepolia.from_wei(prices[i], 'ether')
            }
            tickets.append(ticket)

        return tickets