// contracts/VotingContract.sol
pragma solidity ^0.8.0;

contract VotingContract {
    struct Vote {
        address voter;
        string encryptedVote;
    }
    
    Vote[] public votes;
    
    function castVote(string memory _encryptedVote) public {
        votes.push(Vote(msg.sender, _encryptedVote));
    }
    
    function getAllVotes() public view returns (Vote[] memory) {
        return votes;
    }
}