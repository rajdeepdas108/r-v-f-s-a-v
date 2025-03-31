from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

class EncryptionManager:
    def __init__(self):
        self.keys = {}
    
    def generate_keys(self, voter_id):
        key = RSA.generate(2048)
        self.keys[voter_id] = {
            'private': key.export_key(),
            'public': key.publickey().export_key()
        }
    
    def encrypt_vote(self, voter_id, vote):
        public_key = RSA.import_key(self.keys[voter_id]['public'])
        session_key = get_random_bytes(16)
        
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(vote.encode())
        
        return base64.b64encode(enc_session_key + cipher_aes.nonce + tag + ciphertext).decode()
    
    def decrypt_vote(self, voter_id, encrypted_data):
        private_key = RSA.import_key(self.keys[voter_id]['private'])
        encrypted_data = base64.b64decode(encrypted_data)
        
        enc_session_key = encrypted_data[:private_key.size_in_bytes()]
        nonce = encrypted_data[private_key.size_in_bytes():private_key.size_in_bytes()+16]
        tag = encrypted_data[private_key.size_in_bytes()+16:private_key.size_in_bytes()+32]
        ciphertext = encrypted_data[private_key.size_in_bytes()+32:]
        
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        return cipher_aes.decrypt_and_verify(ciphertext, tag).decode()