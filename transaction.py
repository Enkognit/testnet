from web3 import Web3
import solcx

rpc_url = "http://127.0.0.1:32769"
web3 = Web3(Web3.HTTPProvider(rpc_url))

accounts = [
    ["0xd72145f272558133D085F91A3bC3029298e6FD05", 
        "e97bbf262d938813a5b743a85fd0386ce0a663a997562a84c1abfc9ad26991ba"],
    ["0x6545a087bA1eD4D5F036e750f4624612613b61AE",
        "cd8d8d1f733043f30d251485d4b892f0d90e866d51911ceb4a9e226611be83dd"],
    ["0x78502606558154029c24295F09E5C77c7E813B6c", 
        "74750f387bdb9cc3bffb5a59f0cd463023c540fd0ed5d1c181fac2602e176139"]
]

contract_addr = "0xd0F28BFECd65618A2680eFd440d9605bB6f2CF70"
contract_abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'buyer', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'price', 'type': 'uint256'}], 'name': 'BoughtTicket', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'winner', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'prize', 'type': 'uint256'}], 'name': 'EndLottery', 'type': 'event'}, {'inputs': [], 'name': 'buyLotteryTicket', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'newLotteryTime', 'type': 'uint256'}], 'name': 'changeLotteryTime', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'currentPrize', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'endLottery', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'endLotteryTime', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'keys', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'lotteryTime', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}]
contract_instance = web3.eth.contract(address=contract_addr, abi=contract_abi)

def sign_and_send(transaction, key):
    signed_tx = web3.eth.account.sign_transaction(transaction, key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"Transaction sent. Hash: {web3.to_hex(tx_hash)}")
    
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def send_eth_transaction(sender_addr, receiver_addr, private_key, eth_am):
    nonce = web3.eth.get_transaction_count(sender_addr);
    transaction = {
        'nonce': nonce,
        'to': receiver_addr,
        'value': web3.to_wei(eth_am, 'ether'),
        'gas': 21000,
        'gasPrice': web3.eth.gas_price * 2,
        'chainId': web3.eth.chain_id
    }
    
    tx_receipt = sign_and_send(transaction, private_key)
    if tx_receipt['status'] == 1:
        print("Transaction accepted")
    else:
        print("Transaction discarded")


def SendTransaction():
    print("Accounts:")
    for i in range(len(accounts)):
        print(' ', i + 1, '. ', accounts[i][0], sep='')
    print("From account: ", end = '')
    acc_n = input()
    if not acc_n.isdigit() or int(acc_n) < 1 or int(acc_n) > len(accounts):
        print("Wrong account number!")
        return
    [acc, key] = accounts[int(acc_n) - 1]
        
    print("To account: ", end = '')
    to_acc = input()
    if to_acc[:2] != "0x":
        n = int(to_acc)
        if not to_acc.isdigit():
            print("Wrong account number")
            return
        n = int(to_acc)
        if n < 1 or n > len(accounts):
            print("Wrong account number")
            return
        to_acc = accounts[n - 1][0]
    
    print("ETH amount: ", end='')
    eth_am = int(input())
    
    if eth_am == 0:
        raise Exception("ETH amount must not be 0")
        
    send_eth_transaction(acc, to_acc, key, eth_am)
    
    
def GetBalance():
    print("Accounts:")
    for i in range(len(accounts)):
        print(' ', i + 1, '. ', accounts[i][0], sep='')
    print("Account: ", end = '')
    acc = input()
    if acc[:2] == "0x":
        print(web3.eth.get_balance(acc), "wei")
    else:
        if not acc.isdigit():
            print("Wrong account number")
            return
        n = int(acc)
        if n < 1 or n > len(accounts):
            print("Wrong account number")
            return
        print(web3.eth.get_balance(accounts[n - 1][0]), "wei")
        
def GetAllBalances():
    for i, [k, v] in enumerate(accounts):
        print(i + 1, '. ', k, ' : ', web3.eth.get_balance(accounts[i][0]), ' wei', sep='')

def PushContract():
    print("Accounts:")
    for i in range(len(accounts)):
        print(' ', i + 1, '. ', accounts[i][0], sep='')
    print("Account: ", end = '')
    acc = input()
    if not acc.isdigit():
        print("Wrong account number")
        return
    n = int(acc)
    if n < 1 or n > len(accounts):
        print("Wrong account number")
        return
    
    [acc, key] = accounts[n - 1]
    
    solcx.install_solc('0.8.28', show_progress=True)
    solcx.set_solc_version('0.8.28')
    compiled_contract = solcx.compile_files(["Lottery.sol"])
    
    contract_abi = compiled_contract["Lottery.sol:Lottery"]['abi']
    contract_bytecode = compiled_contract["Lottery.sol:Lottery"]['bin']
    
    contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    
    transaction = contract.constructor().build_transaction({
        "chainId": web3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price * 2,
        'nonce': web3.eth.get_transaction_count(acc)
    })
    
    tx_receipt = sign_and_send(transaction, key)
    
    if tx_receipt['status'] == 1:
        print("Transaction accepted")
    else:
        print("Transaction discarded")
        return
    
    print("Address:", tx_receipt.contractAddress)
    print("Contract ABI:" , contract_abi)

def BuyTicket():
    print("Accounts:")
    for i in range(len(accounts)):
        print(' ', i + 1, '. ', accounts[i][0], sep='')
    print("Account: ", end = '')
    acc = input()
    if not acc.isdigit():
        print("Wrong account number")
        return
    n = int(acc)
    if n < 1 or n > len(accounts):
        print("Wrong account number")
        return
    
    print("ETH amount: ", end = '')
    sval = input()
    if not sval.isdigit():
        print("Wrong ETH amount")
        return
    val = int(sval)
    
    [addr, key] = accounts[n - 1]
    global contract_instance
    transaction = contract_instance.functions.buyLotteryTicket().build_transaction({
        'from': addr,
        'nonce': web3.eth.get_transaction_count(addr),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'value': web3.to_wei(val, 'ether')
    })
    
    tx_receipt = sign_and_send(transaction, key)
    
    if tx_receipt['status'] == 1:
        print("Transaction accepted")
    else:
        print("Transaction discarded")
        return
    
def EndLottery():
    print("Accounts:")
    for i in range(len(accounts)):
        print(' ', i + 1, '. ', accounts[i][0], sep='')
    print("Account: ", end = '')
    acc = input()
    if not acc.isdigit():
        print("Wrong account number")
        return
    n = int(acc)
    if n < 1 or n > len(accounts):
        print("Wrong account number")
        return
    
    
    [addr, key] = accounts[n - 1]
    global contract_instance
    transaction = contract_instance.functions.endLottery().build_transaction({
        'from': addr,
        'nonce': web3.eth.get_transaction_count(addr),
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price * 2
    })
    
    tx_receipt = sign_and_send(transaction, key)
    
    if tx_receipt['status'] == 1:
        print("Transaction accepted")
    else:
        print("Transaction discarded")
        return


options = [
    ["Send transaction", SendTransaction],
    ["Get balance", GetBalance],
    ["Get all balances", GetAllBalances],
    ["Push contract", PushContract],
    ["Buy lottery ticket", BuyTicket],
    ["End lottery", EndLottery],
    ["Exit", exit]
]

def main():    
    if web3.is_connected():
        print("Connected successfully")
    else:
        print("Connection failed")
        return
    
    while True:
        try:
            print("Options:");
            for i, [v, f] in enumerate(options):
                print(i + 1, ". ", v, sep="")
            print('> ', end='')
            inp = str(input())
            if not inp.isdigit():
                print("Wrong option! Try again.")
                continue
            
            opt = int(inp)
            if opt < 1 or opt > len(options):
                print("Wrong option! Try again.")
            
            options[opt - 1][1]()
                
        except Exception as e:
            print("Exception:", str(e))
                    
                


if __name__ == "__main__":
    main()
