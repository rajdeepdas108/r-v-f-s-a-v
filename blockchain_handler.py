# src/blockchain_handler.py
from web3 import Web3
import json

class BlockchainHandler:
    def __init__(self, provider_url, contract_address=None):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.contract_abi = self._load_abi()
        
    def _load_abi(self):
        with open('contracts/VotingContract.abi', 'r') as f:
            return json.load(f)
    
    def deploy_contract(self, account_address, private_key):
        contract = self.w3.eth.contract(
            abi=self.contract_abi,
            bytecode=self._load_bytecode()
        )
        tx_hash = contract.constructor().transact({
            'from': account_address
        })
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract_address = tx_receipt.contractAddress
        return self.contract_address
    
    def get_contract_instance(self):
        return self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )