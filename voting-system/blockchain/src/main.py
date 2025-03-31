from .system_integration import VotingSystem
import hashlib

def main():
    system = VotingSystem("http://localhost:8545")
    
    # Voter registration
    system.register_voter("voter1", "path/to/voter1_photo.jpg")
    system.register_voter("voter2", "path/to/voter2_photo.jpg")
    
    # Voting process
    system.cast_vote("voter1", "path/to/current_photo1.jpg", "CandidateA")
    system.cast_vote("voter2", "path/to/current_photo2.jpg", "CandidateB")
    
    # Tally votes
    results = system.tally_votes()
    print(f"Final Results: {results['results']}")
    print(f"Merkle Root: {results['merkle_root']}")

if __name__ == "__main__":
    main()