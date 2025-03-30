# src/encryption_manager.py
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

class EncryptionManager:
    def __init__(self):
        self.keys = {}
    
    def generate_key_pair(self, voter_id):
        key = RSA.generate(2048)
        self.keys[voter_id] = {
            'private': key.export_key(),
            'public': key.publickey().export_key()
        }
    
    def encrypt_vote(self, voter_id, vote_data):
        public_key = RSA.import_key(self.keys[voter_id]['public'])
        # ... rest of encryption logic from previous example
        return encrypted_data
    
    def decrypt_vote(self, voter_id, encrypted_data):
        private_key = RSA.import_key(self.keys[voter_id]['private'])
        # ... rest of decryption logic
        return decrypted_data