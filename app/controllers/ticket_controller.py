import json
import os
from dotenv import load_dotenv
from web3 import Web3


load_dotenv()

class TicketContract:
    def __init__(self):
        contract_address = os.getenv("CONTRACT_ADDRESS")
        api_key = os.getenv("API_KEY")

        if not contract_address:
            raise ValueError("Missing CONTRACT_ADDRESS in .env")
        if not api_key:
            raise ValueError("Missing API_KEY in .env")

        self.sepolia = Web3(Web3.HTTPProvider(api_key))
        abi_path = os.path.join(os.path.dirname(__file__), '..', '..', 'hardhat', 'artifacts', 'contracts', 'Ticket.sol', 'Ticket.json')
        with open(os.path.abspath(abi_path)) as f:
            artifact = json.load(f)
        
        abi = artifact["abi"]

        self.contract = self.sepolia.eth.contract(
            address=contract_address,
            abi=abi
        )

    def mint_ticket(self, wallet_address: str, event_data: dict):
        tx = self.contract.functions.mintTicket(
            wallet_address,
            event_data['eventName'],
            event_data['date'],
            event_data['zone'],
            event_data['seat'],
            self.sepolia.to_wei(event_data['price'], 'ether')
        ).build_transaction({
            "from": wallet_address,
            "nonce": self.sepolia.eth.get_transaction_count(wallet_address),
            "value": self.sepolia.to_wei(event_data['price'], 'ether')
        })
        return tx

    def get_user_tickets(self, wallet_address: str):
        event_names, dates, zones, seats, prices = self.contract.functions.getUserTickets(wallet_address).call()

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