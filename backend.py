from web3 import Web3
from web3._utils.encoding import to_hex
from solcx import compile_source, install_solc






contract_adress=None
web3 = None
contract_id = 0

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
    except:
        return "0 Balance or withdrawal Failed"

def check_contract_balance():
    # Get balance of the contract in Wei
    balance_wei = web3.eth.get_balance(contract_address)
    
    # Convert Wei to Ether for readability
    balance_eth = Web3.from_wei(balance_wei, 'ether')
    
    print(f"Contract Balance: {balance_eth} ETH")
    return balance_eth