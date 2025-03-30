# src/system_integration.py
from .blockchain_handler import BlockchainHandler
from .biometric_auth import BiometricAuth
from .encryption_manager import EncryptionManager
from .merkle_manager import MerkleManager
import hashlib

class VotingSystem:
    def __init__(self, blockchain_provider):
        self.blockchain = BlockchainHandler(blockchain_provider)
        self.biometric = BiometricAuth()
        self.encryption = EncryptionManager()
        self.merkle = MerkleManager()
        self.voter_registry = {}
    
    def register_voter(self, voter_id, image_path):
        self.biometric.register_voter(voter_id, image_path)
        self.encryption.generate_key_pair(voter_id)
    
    def cast_vote(self, voter_id, image_path, vote):
        if not self.biometric.authenticate(voter_id, image_path):
            raise AuthenticationError
        encrypted_vote = self.encryption.encrypt_vote(voter_id, vote)
        contract = self.blockchain.get_contract_instance()
        contract.functions.castVote(encrypted_vote).transact()
    
    def tally_votes(self):
        contract = self.blockchain.get_contract_instance()
        encrypted_votes = contract.functions.getAllVotes().call()
        decrypted_votes = [
            self.encryption.decrypt_vote(voter_id, vote)
            for voter_id, vote in encrypted_votes
        ]
        self.merkle.create_tree("election2023", decrypted_votes)
        return decrypted_votes