"""
deploy_contract.py
──────────────────
Deploys KisanInventory.sol to a local Ganache blockchain.

Run AFTER starting Ganache:
  ganache --port 7545

Then:
  python deploy_contract.py

It will print the CONTRACT_ADDRESS to paste into your .env
"""

import json
import os
import sys

try:
    from web3 import Web3
    from solcx import compile_source, install_solc
except ImportError:
    print("Install: pip install web3 py-solc-x")
    sys.exit(1)

GANACHE_URL = "http://127.0.0.1:7545"
SOL_FILE = os.path.join(os.path.dirname(__file__), "blockchain", "KisanInventory.sol")

def deploy():
    # 1. Connect to Ganache
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not w3.is_connected():
        print("❌ Cannot connect to Ganache. Start it first: ganache --port 7545")
        sys.exit(1)

    print(f"✅ Connected to Ganache. Chain ID: {w3.eth.chain_id}")
    accounts = w3.eth.accounts
    deployer = accounts[0]
    print(f"📬 Deploying from: {deployer}")

    # 2. Compile contract
    print("🔧 Compiling KisanInventory.sol …")
    install_solc("0.8.0")
    with open(SOL_FILE) as f:
        source = f.read()

    compiled = compile_source(source, output_values=["abi", "bin"], solc_version="0.8.0")
    contract_id = list(compiled.keys())[0]
    abi = compiled[contract_id]["abi"]
    bytecode = compiled[contract_id]["bin"]

    # 3. Deploy
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({"from": deployer, "gas": 3000000})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    address = receipt.contractAddress

    print(f"\n🎉 CONTRACT DEPLOYED!")
    print(f"   Address : {address}")
    print(f"   TX Hash : {tx_hash.hex()}")
    print(f"\n👉 Add this to your .env:")
    print(f"   CONTRACT_ADDRESS={address}")
    print(f"   DEPLOYER_PRIVATE_KEY=  (leave blank for Ganache unlocked accounts)")

    # Save ABI for reference
    abi_path = os.path.join(os.path.dirname(__file__), "blockchain", "contract_abi.json")
    with open(abi_path, "w") as f:
        json.dump(abi, f, indent=2)
    print(f"\n📄 ABI saved to: {abi_path}")

if __name__ == "__main__":
    deploy()
