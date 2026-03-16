from iao_lab1 import Blockchain
from uuid import uuid4
from json import loads as json_loads

from flask import Flask, jsonify, request

app_IAO = Flask(__name__)

node_identifier_IAO = str(uuid4()).replace("-", "")

blockchain_IAO = Blockchain()


@app_IAO.route("/mine", methods = ["GET"])
def mine_IAO():
    last_block_IAO = blockchain_IAO.last_block_IAO
    last_proof_IAO = last_block_IAO['proof']
    proof_IAO = blockchain_IAO.proof_of_work_IAO(last_proof_IAO)

    blockchain_IAO.new_transaction_IAO(sender_IAO='0', recipient_IAO=node_identifier_IAO, amount_IAO=1)
    previous_hash_IAO = blockchain_IAO.hash_IAO(last_block_IAO)
    block_IAO = blockchain_IAO.new_block_IAO(proof_IAO, previous_hash_IAO)

    response_IAO = {
        'message': "New block forged",
        'index': block_IAO['index'],
        'transactions': block_IAO['transactions'],
        'proof': block_IAO['proof'],
        'previous_hash': previous_hash_IAO
    }

    return jsonify(response_IAO), 200


@app_IAO.route("/transactions/new", methods = ["POST"])
def new_transaction_IAO():
    values_IAO = json_loads(request.get_json())

    required_IAO = ['sender', 'recipient', 'amount']
    if not all(k in values_IAO for k in required_IAO):
        return 'Missing values', 400
    
    index_IAO = blockchain_IAO.new_transaction_IAO(values_IAO['sender'], values_IAO['recipient'], values_IAO['amount'])

    response_IAO = {
        'message': f'Transaction will be added to Block {index_IAO}'
    }
    return jsonify(response_IAO), 201


@app_IAO.route("/chain", methods = ["GET"])
def full_chain():
    response_IAO = {
        'chain': blockchain_IAO.chain_IAO,
        'length': len(blockchain_IAO.chain_IAO)
    }
    return jsonify(response_IAO), 200

if __name__ == "__main__":
    app_IAO.run(host="0.0.0.0", port=5000)