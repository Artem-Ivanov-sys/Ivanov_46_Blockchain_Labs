from blockchain import Blockchain
from uuid import uuid4
from json import loads as json_loads
import argparse
from re import match
from urllib.parse import urlparse

from flask import Flask, jsonify, request

app_IAO = Flask(__name__)

node_identifier_IAO = str(uuid4()).replace("-", "")

blockchain_IAO = Blockchain()

@app_IAO.route("/mine", methods = ["GET"])
def mine_IAO():
    last_block_IAO = blockchain_IAO.last_block_IAO
    last_proof_IAO = last_block_IAO['proof']
    proof_IAO = blockchain_IAO.proof_of_work_IAO(last_proof_IAO)

    blockchain_IAO.new_transaction_IAO(sender_IAO='0', recipient_IAO=node_identifier_IAO, amount_IAO=3)
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

@app_IAO.route("/nodes/register", methods = ["POST"])
def register_node():
    values = json_loads(request.get_json())

    nodes = values.get("nodes")
    if nodes is None:
        return "Error: please supply a valid list of nodes.", 400
    
    for node in nodes:
        urlparsed = urlparse(node)
        if not all([urlparsed.scheme, urlparsed.netloc]):
            continue
        blockchain_IAO.register_node(node)
    
    response = {
        "message": "New nodes have been added",
        "total_nodes": list(blockchain_IAO.nodes)
    }

    return response, 201

@app_IAO.route("/nodes/resolve", methods = ["GET"])
def resolve_nodes():
    replaced = blockchain_IAO.resolve_conflicts()

    if replaced:
        response = {
            "message": "Our chain wasreplaced.",
            "new_chain": blockchain_IAO.chain_IAO
        }
    else:
        response = {
            "message": "Our chain is authoritative",
            "chain": blockchain_IAO.chain_IAO
        }
    return response, 200

def run_server_on_port(port: int):
    app_IAO.run(host="127.0.0.1", port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs blockchain on specific port")
    parser.add_argument('-p', '--port', type=int, default=5000, help="port")
    args = parser.parse_args()

    run_server_on_port(args.port)
