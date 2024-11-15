from web3 import Web3
from web3._utils.encoding import to_hex
from solcx import compile_source, install_solc

smart_contract="""
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
} """




contract_adress=None
web3 = None
contract_id = 0
contract_interface = None
def update_model(text,id,value=5):

    sender_address = web3.eth.accounts[id]


    contract = web3.eth.contract(address=contract_address, abi=contract_interface["abi"])
    try:
        model_hash = web3.keccak(text=text)
        tx = contract.functions.submitUpdate(model_hash).transact({
            'from': sender_address,
            'value':web3.to_wei(value,'ether')  # Use the first account provided by Ganache
        })
        web3.eth.wait_for_transaction_receipt(tx) 
    except Exception as e:
        return 0
    
    return 1

def init_contract(amount_in_ether,val=8):
    for i in range(val):
        sender_address = web3.eth.accounts[0]  # Replace with a valid account
        return update_model("init",0,amount_in_ether)

def server_update_model(text,id):

    check = update_model(text,id)
    if(not check):
        return "Insufficient Balance"
    
    return "Succefully Uploaded Model"

def b_init():
    global web3
    global contract_interface
    blockchain_url = "http://127.0.0.1:7545"  # Ganache or any Ethereum node
    web3 = Web3(Web3.HTTPProvider(blockchain_url))
    # contract_address = contract_address

    # Load contract
    # contract = web3.eth.contract(address=contract_address, abi=abi)
    web3.eth.default_account = web3.eth.accounts[contract_id]

    compiled_sol = compile_source(smart_contract, solc_version="0.8.0")
    contract_interface = compiled_sol["<stdin>:FederatedLearning"]

    # Deploy the contract
    FederatedLearning = web3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
    tx_hash = FederatedLearning.constructor().transact({
        'from': web3.eth.accounts[contract_id]  # Use the first account provided by Ganache
    })
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Contract deployed at this address
    global contract_address
    contract_address = tx_receipt.contractAddress
    print("Contract deployed at address:", contract_address)


def check_current_balance(id):
    sender_address = web3.eth.accounts[id]  # sender's address


    balance = web3.eth.get_balance(sender_address)
    balance_eth = Web3.from_wei(balance, 'ether')

    return balance_eth

def check_reward(id):
    
    contract = web3.eth.contract(address=contract_address, abi=contract_interface["abi"])
    sender_address = web3.eth.accounts[id]

    tx_hash = contract.functions.getReward().call({
        'from' : sender_address
    })
    reward = web3.from_wei(tx_hash,'ether')
    return reward

def withdraw_rewards(id):
    
    contract = web3.eth.contract(address=contract_address, abi=contract_interface["abi"])
    sender_address = web3.eth.accounts[id]

    try:
        tx = contract.functions.withdrawRewards.transact({
            'from': sender_address
        })
        web3.eth.wait_for_transaction_receipt(tx)
        
        return f'''Succesfully withdrawn''' 
    except Exception as e:

        print(e)
        return "0 Balance or withdrawal Failed"

def check_contract_balance():
    # Get balance of the contract in Wei
    balance_wei = web3.eth.get_balance(contract_address)
    
    # Convert Wei to Ether for readability
    balance_eth = Web3.from_wei(balance_wei, 'ether')
    
    print(f"Contract Balance: {balance_eth} ETH")
    return balance_eth

# b_init()
# print(init_contract(10))