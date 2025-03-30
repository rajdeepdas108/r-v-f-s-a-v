# src/merkle_manager.py
from merkletools import MerkleTools
import hashlib

class MerkleManager:
    def __init__(self):
        self.trees = {}
    
    def create_tree(self, election_id, votes):
        mt = MerkleTools(hash_type='sha256')
        for vote in votes:
            mt.add_leaf(hashlib.sha256(vote.encode()).hexdigest())
        mt.make_tree()
        self.trees[election_id] = mt
    
    def verify_vote(self, election_id, vote):
        mt = self.trees.get(election_id)
        vote_hash = hashlib.sha256(vote.encode()).hexdigest()
        if mt and vote_hash in mt.leaves:
            index = mt.leaves.index(vote_hash)
            return mt.validate_proof(mt.get_proof(index), vote_hash, mt.get_merkle_root())
        return False