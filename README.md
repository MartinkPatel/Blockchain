smart_contract='''// Solidity Smart Contract for Blockchain Layer
pragma solidity ^0.8.0;

contract FederatedLearning {
    struct Update {
        address node;
        bytes32 modelHash; // Hash of the model update
        uint timestamp;
        uint ethSent;      // Amount of ETH sent with the update
    }

    Update[] public updates;
    mapping(address => uint) public rewards; // Logical token rewards
    mapping(address => uint) public ethBalance; // ETH balance for each participant

    event NewUpdate(address indexed node, bytes32 modelHash, uint timestamp, uint ethSent);
    event RewardSent(address indexed node, uint amount);
    event ValidationFailed(address indexed node, uint amount);

    // Submit an update with optional ETH
    function submitUpdate(bytes32 _modelHash) public payable {
        // Check if the sender has enough balance to send ETH
        require(msg.value > 0, "Must send ETH with the update");
        require(address(msg.sender).balance >= msg.value, "Insufficient balance to send ETH");

        updates.push(Update(msg.sender, _modelHash, block.timestamp, msg.value));
        rewards[msg.sender] += 1e19; // Reward 10 tokens
        ethBalance[msg.sender] += msg.value; // Track ETH sent
        emit NewUpdate(msg.sender, _modelHash, block.timestamp, msg.value);
    }

    
    
    function withdrawRewards() public {
        uint amount = rewards[msg.sender];
        require(amount > 0, "No ETH rewards to withdraw");

        ethBalance[msg.sender] = 0; // Reset balance before transfer to prevent re-entrancy
        rewards[msg.sender]=0;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit RewardSent(msg.sender, amount);
    }

    // Get total ETH balance of the contract (for testing purposes)
    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }
    
    function NoReward() public {
        rewards[msg.sender] -= 1e19;

        emit ValidationFailed(msg.sender,0);
    }
    

    // Get token rewards for the participant
    function getReward() public view returns (uint) {
        return rewards[msg.sender];
    }
}
'''
