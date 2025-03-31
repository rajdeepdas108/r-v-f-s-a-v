import face_recognition
import numpy as np

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
        current_image = face_recognition.load_image_file(image_path)
        current_encoding = face_recognition.face_encodings(current_image)
        if not current_encoding:
            return False
        return face_recognition.compare_faces(
            [self.voter_db[voter_id]], 
            current_encoding[0]
        )[0]