from iao_lab1 import Blockchain
from pprint import pprint
from datetime import datetime

(block:=Blockchain()).new_transaction_IAO("Artem", "Vlad", 100)

pprint(block.last_block_IAO, indent=4)

proof = block.proof_of_work_IAO(block.last_block_IAO['previous_hash'])
print(proof)