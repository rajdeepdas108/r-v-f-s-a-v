# src/main.py
from system_integration import VotingSystem

def main():
    system = VotingSystem("https://mainnet.infura.io/v3/YOUR_PROJECT_ID")
    
    # Deploy contract
    contract_address = system.blockchain.deploy_contract(
        "0xYourAccountAddress",
        "your_private_key"
    )
    
    # Voter registration
    system.register_voter("voter1", "path/to/voter1_photo.jpg")
    
    # Voting process
    system.cast_vote(
        "voter1",
        "path/to/current_photo.jpg",
        "Candidate A"
    )
    
    # Tally votes
    results = system.tally_votes()
    print(f"Election results: {results}")

if __name__ == "__main__":
    main()