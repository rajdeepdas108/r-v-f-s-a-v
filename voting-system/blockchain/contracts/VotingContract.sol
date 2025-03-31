// contracts/VotingContract.sol
pragma solidity ^0.8.0;

contract VotingSystem {
    struct Vote {
        bytes32 voterHash;
        bytes encryptedVote;
        bytes zkProof;
        uint256 timestamp;
    }
    
    Vote[] private votes;
    bytes32 public merkleRoot;
    address public admin;
    
    event VoteCast(bytes32 indexed voterHash, uint256 timestamp);
    event MerkleRootUpdated(bytes32 newRoot);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not authorized");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function castVote(
        bytes32 _voterHash,
        bytes memory _encryptedVote,
        bytes memory _zkProof
    ) external {
        votes.push(Vote(_voterHash, _encryptedVote, _zkProof, block.timestamp));
        emit VoteCast(_voterHash, block.timestamp);
    }

    function updateMerkleRoot(bytes32 _newRoot) external onlyAdmin {
        merkleRoot = _newRoot;
        emit MerkleRootUpdated(_newRoot);
    }

    function getTotalVotes() external view returns (uint256) {
        return votes.length;
    }

    function getVote(uint256 index) external view returns (
        bytes32 voterHash,
        bytes memory encryptedVote,
        bytes memory zkProof,
        uint256 timestamp
    ) {
        require(index < votes.length, "Invalid index");
        Vote storage vote = votes[index];
        return (vote.voterHash, vote.encryptedVote, vote.zkProof, vote.timestamp);
    }
}