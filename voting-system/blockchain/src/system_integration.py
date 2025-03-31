from blockchain.blockchain_handler import BlockchainHandler
from blockchain.biometric_auth import BiometricAuth
from blockchain.encryption_manager import EncryptionManager
from blockchain.merkle_manager import MerkleManager
from blockchain.zk_proofs import ZKProofSystem
import hashlib

class VotingSystem:
    def __init__(self, blockchain_provider):
        self.blockchain = BlockchainHandler(blockchain_provider)
        self.biometric = BiometricAuth()
        self.encryption = EncryptionManager()
        self.merkle = MerkleManager()
        self.zk = ZKProofSystem()
        self.voter_registry = {}
        self.zk.trusted_setup()

    def register_voter(self, voter_id, image_path, public_key):
        self.biometric.register_voter(voter_id, image_path)
        self.encryption.generate_key_pair(voter_id)
        self.voter_registry[voter_id] = public_key

    def cast_vote(self, voter_id, image_path, vote):
        if not self.biometric.authenticate(voter_id, image_path):
            raise ValueError("Biometric verification failed")
        
        # Generate ZK proof
        zk_proof = self.zk.generate_proof(vote)
        
        # Encrypt vote
        encrypted_vote = self.encryption.encrypt_vote(voter_id, vote)
        
        # Submit to blockchain
        contract = self.blockchain.get_contract_instance()
        tx_hash = contract.functions.castVote(
            voter_id,
            encrypted_vote,
            zk_proof
        ).transact()
        
        return tx_hash

    def tally_votes(self):
        contract = self.blockchain.get_contract_instance()
        votes = contract.functions.getAllVotes().call()
        
        decrypted_votes = []
        for vote in votes:
            try:
                decrypted = self.encryption.decrypt_vote(
                    vote['voter_id'], 
                    vote['encrypted_vote']
                )
                decrypted_votes.append(decrypted)
            except:
                continue
        
        self.merkle.create_tree("election", decrypted_votes)
        return {
            "results": Counter(decrypted_votes),
            "merkle_root": self.merkle.get_merkle_root(),
            "total_votes": len(decrypted_votes)
        }