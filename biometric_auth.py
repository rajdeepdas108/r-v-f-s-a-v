# src/biometric_auth.py
import face_recognition

class BiometricAuth:
    def __init__(self):
        self.voter_db = {}
    
    def register_voter(self, voter_id, image_path):
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        self.voter_db[voter_id] = encoding
    
    def authenticate(self, voter_id, image_path):
        if voter_id not in self.voter_db:
            return False
        unknown_image = face_recognition.load_image_file(image_path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        return face_recognition.compare_faces(
            [self.voter_db[voter_id]], 
            unknown_encoding
        )[0]