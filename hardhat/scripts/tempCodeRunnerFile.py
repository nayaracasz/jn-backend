import json
import os
from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware


load_dotenv()
print("PRIVATE_KEY LOADED:", os.getenv("TEST_PRIVATE_KEY"))