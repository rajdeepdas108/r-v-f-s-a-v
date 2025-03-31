from merkletools import MerkleTools
import hashlib

class MerkleManager:
    def __init__(self):
        self.mt = MerkleTools(hash_type='sha256')
        self.vote_hashes = []
    
    def add_vote(self, vote):
        vote_hash = hashlib.sha256(vote.encode()).hexdigest()
        self.mt.add_leaf(vote_hash, True)
        self.mt.make_tree()
        self.vote_hashes.append(vote_hash)
    
    def get_proof(self, index):
        return self.mt.get_proof(index)
    
    def verify_vote(self, vote, index):
        vote_hash = hashlib.sha256(vote.encode()).hexdigest()
        return self.mt.validate_proof(
            self.get_proof(index),
            vote_hash,
            self.mt.get_merkle_root()
        )