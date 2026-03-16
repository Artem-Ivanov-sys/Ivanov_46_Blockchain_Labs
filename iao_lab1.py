from time import time
from hashlib import sha256
from json import dumps

class Blockchain(object):
    def __init__(self):
        self.chain_IAO = []
        self.current_transactions_IAO = []

        self.new_block_IAO(3022005, sha256("Ivanov".encode()).hexdigest())

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