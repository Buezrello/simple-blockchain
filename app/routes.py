from app import app, blockchain, node_id
from flask import jsonify, request
import sys
import json
from constants import *


@app.route('/mining')
def mining():
    # find new proof by previous proof
    latest_block = blockchain.latest_block
    prev_proof = latest_block[PROOF]
    new_proof = blockchain.proof_of_work(prev_proof)

    # get reward for found a proof
    blockchain.add_new_transaction(
        sender="0",  # sender=0 means that recipient got an award
        recipient=node_id,
        total=1
    )

    # create a new block, add to a chain
    prev_hash = blockchain.hash_block(latest_block)
    new_block = blockchain.add_block(new_proof, prev_hash)

    resp = {
        MESSAGE: "New Block created",
        INDEX: new_block[INDEX],
        TRANSACTIONS: new_block[TRANSACTIONS],
        PROOF: new_block[PROOF],
        PREV_HASH: new_block[PREV_HASH]
    }

    return jsonify(resp), 200


@app.route('/transactions/add', methods=['POST'])
def add_transaction():
    # get a new transaction as json
    values = request.get_json()

    # create a new transaction
    indx = blockchain.add_new_transaction(values[SENDER], values[RECIPIENT], values[TOTAL])

    resp = {MESSAGE: f'Transaction will be added to a Block {indx}'}

    return jsonify(resp), 201


@app.route('/fullchain')
def chain():
    resp = {
        BLOCK_CHAIN: blockchain.block_chain,
        CHAIN_LENGTH: len(blockchain.block_chain)
    }
    return jsonify(resp), 200


@app.route('/nodes/register', methods=['POST'])
def nodes_registration():
    # registration nodes from a neighbourhoods

    values = request.get_json()
    nodes = values.get(NODES)

    if not nodes:
        return "Error: list of nodes is empty", 400

    for node in nodes:
        blockchain.node_register(node)

    resp = {
        MESSAGE: 'New node added',
        LIST_NODES: list(blockchain.nodes)
    }

    return jsonify(resp), 201


@app.route('/nodes/conflict_resolving')
def conflict_resolving():
    # resolving conflicts using consensus algorithm
    if blockchain.consensus_algorithm():
        resp = {
            MESSAGE: 'Current chain was replaced by longest',
            NEW_CHAIN: blockchain.block_chain
        }
    else:
        resp = {
            MESSAGE: 'Current chain is longest and was not replaced',
            CHAIN: blockchain.block_chain
        }

    return jsonify(resp), 200



