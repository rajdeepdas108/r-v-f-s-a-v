from py_ecc.bn128 import G1, G2, pairing, add, multiply
import random

class ZKProofSystem:
    def __init__(self):
        self.params = None
    
    def setup(self):
        a = random.randint(1, 1000000)
        b = random.randint(1, 1000000)
        self.params = {
            'A': multiply(G1, a),
            'B': multiply(G2, b)
        }
    
    def generate_proof(self, secret):
        if not self.params:
            raise ValueError("Run setup first")
        return multiply(G1, self.params['A'][0] * secret)
    
    def verify_proof(self, proof, public_input):
        lhs = pairing(self.params['B'], proof)
        rhs = pairing(multiply(G2, public_input), self.params['A'])
        return lhs == rhs