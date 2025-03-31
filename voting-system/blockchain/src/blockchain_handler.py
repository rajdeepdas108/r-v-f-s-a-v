from web3 import Web3
import json
import os

class BlockchainHandler:
    def __init__(self, provider_url):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = None
        self._load_contract()
    
    def _load_contract(self):
        contract_path = os.path.join(os.path.dirname(__file__), '../contracts/VotingContract.json')
        with open(contract_path) as f:
            contract_data = json.load(f)
        
        self.contract = self.w3.eth.contract(
            address=contract_data['networks']['5777']['address'],
            abi=contract_data['abi']
        )
    
    def submit_vote(self, voter_hash, encrypted_vote, zk_proof):
        return self.contract.functions.castVote(
            voter_hash,
            encrypted_vote,
            zk_proof
        ).transact()
    
    def get_votes(self):
        return self.contract.functions.getVotes().call()