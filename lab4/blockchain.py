from time import time
from hashlib import sha256
from json import dumps
from urllib.parse import urlparse
from aiohttp import ClientSession
from asyncio import run as async_run
from copy import deepcopy

class Blockchain(object):
    def __init__(self):
        self.chain_IAO = []
        self.current_transactions_IAO = []
        self.nodes = set()

        self.new_block_IAO(3022005, sha256("Ivanov".encode()).hexdigest())
    
    def register_node(self, address):
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)

    def valid_chan(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f"{last_block}")
            print(f"{block}")
            print(f"\n{'-'*10}\n")
            if not self.valid_block(block, last_block):
                return False
            
            last_block = block
            current_index += 1
        return True
    
    def valid_block(self, block, prev_block):
        if block["previous_hash"] != self.hash_IAO(prev_block):
            return False
        if not self.valid_proof_IAO(prev_block["proof"], block["proof"]):
            return False
        return True

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain_IAO)

        for node in neighbors:
            length, chain = async_run(self.get_neighbor_chain(node))
            print(length, chain)
            if length is None or chain is None or not self.valid_chan(chain):
                continue

            if length > max_length:
                max_length = length
                new_chain = chain
        
        if new_chain is not None:
            self.chain_IAO = deepcopy(new_chain)
            return True
        return False
    
    async def get_neighbor_chain(self, neighbor):
        async with ClientSession() as session:
            async with session.get(f"http://{neighbor}/chain") as response:
                if response.status//100 not in [1, 2, 3]:
                    return None, None
                retrieved_data = await response.json()
                length = retrieved_data['length']
                chain = retrieved_data["chain"]
                return length, chain

    def proof_of_work_IAO(self, last_proof_IAO):
        proof_IAO = 0

        while not Blockchain.valid_proof_IAO(last_proof_IAO, proof_IAO):
            proof_IAO += 1
        
        return proof_IAO
    
    @staticmethod
    def valid_proof_IAO(last_proof_IAO, proof_IAO):
        guess_IAO = f"{last_proof_IAO}{proof_IAO}".encode()
        guess_hash_IAO = sha256(guess_IAO).hexdigest()
        return guess_hash_IAO[:2] == "02"
        # return guess_hash_IAO[:7] == "0000000"

    def new_block_IAO(self, proof_IAO, previous_hash_IAO=None):
        block_IAO = {
            'index': len(self.chain_IAO) + 1,
            'timestamp': time(),
            'transactions': [i for i in self.current_transactions_IAO],
            'proof': proof_IAO,
            'previous_hash': previous_hash_IAO or Blockchain.hash_IAO(self.last_block_IAO())
        }

        self.current_transactions_IAO.clear()
        
        self.chain_IAO.append(block_IAO)

        return block_IAO

    @staticmethod
    def hash_IAO(block_IAO):
        block_string_IAO = dumps(block_IAO, sort_keys=True).encode()
        return sha256(block_string_IAO).hexdigest()
    
    def new_transaction_IAO(self, sender_IAO, recipient_IAO, amount_IAO) -> int:
        self.current_transactions_IAO.append({
            'sender': sender_IAO,
            'recipient': recipient_IAO,
            'amount': amount_IAO
        })

        return self.last_block_IAO['index'] + 1

    @property
    def last_block_IAO(self):
        return self.chain_IAO[-1]