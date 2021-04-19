from hashlib import sha256
import json
from time import time
from urllib.parse import urlparse
import requests
from constants import *

"""
single block structure

single_block = {
    'index': <int>,
    'timestamp': <unix time>,
    'transactions': [
        {
            'sender': <sender hash>,
            'recipient': <recipient hash>,
            'total': <float> - money, total amount (can be any data)
        }
    ],
    'pow': <int> - Proof of Work
    'prev_hash': <str> - hash of previous block
}
"""


class Blockchain:
    def __init__(self):
        # lst for storing blockchain
        self.block_chain = []
        # list for storing transactions
        self.transactions = []
        # create a first block in a chain
        self.add_block(proof=100, prev_hash="1")
        # set of nodes
        self.nodes = set()

    @property
    def latest_block(self):
        # return latest block in a chain
        return self.block_chain[-1]

    def add_block(self, proof: int, prev_hash: str = None) -> dict:
        """
        create a new block, add to a chain

        :param proof: Proof of Work
        :param prev_hash: previous block hash (optional)
        :return: new block
        """
        if prev_hash is None:
            prev_hash = self.hash_block(self.block_chain[-1])

        block = {
            INDEX: len(self.block_chain) + 1,
            TIMESTAMP: time(),
            TRANSACTIONS: self.transactions,
            PROOF: proof,
            PREV_HASH: prev_hash
        }

        # clear transactions list
        self.transactions = []

        self.block_chain.append(block)

        return block

    def add_new_transaction(self, sender: str, recipient: str, total: int) -> int:
        """
        add new transaction to a list

        :param sender: sender address
        :param recipient: recipient address
        :param total: sum
        :return: index of a new block
        """
        self.transactions.append({
            SENDER: sender,
            RECIPIENT: recipient,
            TOTAL: total
        })

        return self.latest_block[INDEX] + 1

    def proof_of_work(self, prev_proof: int) -> int:
        """
        simple PoW:
        search such number N that hash(prevNumberN) start with '0123'
        where prevN is previous proof, N - new proof
        :param prev_proof: previous proof
        :return: new proof
        """
        proof = 0
        while not self.proof_validation(prev_proof, proof):
            proof += 1

        return proof

    def node_register(self, node_address: str):
        """
        Adding a new node to a set

        :param node_address: url address of a new node
        :return: None
        """
        self.nodes.add(
            urlparse(node_address).netloc
        )

    def is_chain_valid(self, block_chain: list) -> bool:
        """
        are hashes and PoW valid?

        :param block_chain: list of blocks - blockchain
        :return: True if chain is valid, False otherwise
        """
        prev_block = block_chain[0]
        cur_indx = 1

        while cur_indx < len(block_chain):
            cur_block = block_chain[cur_indx]
            # check if hash is correct
            if cur_block[PREV_HASH] != self.hash_block(prev_block):
                return False
            # check if proof of work is correct
            if not self.proof_validation(prev_block[PROOF], cur_block[PROOF]):
                return False

            prev_block = cur_block
            cur_indx += 1

        return True

    def consensus_algorithm(self) -> bool:
        """
        Consensus Algorithm
        Solves conflict by choosing a longest blockchain in network

        :return: True if a current chain was changed to a longer, False otherwise
        """
        max_chain_length = len(self.block_chain)
        longest_chain = None

        # check chains of every node in network
        for node in self.nodes:
            resp = requests.get(f'http://{node}/fullchain')

            if resp.status_code == 200:
                length = resp.json()[CHAIN_LENGTH]
                chain = resp.json()[BLOCK_CHAIN]

                # check that a chain is longer than current and is valid
                if length > max_chain_length and self.is_chain_valid(chain):
                    max_chain_length = length
                    longest_chain = chain

        if longest_chain:
            self.block_chain = longest_chain
            return True

        return False

    @staticmethod
    def hash_block(single_block: dict) -> str:
        """
        create sha-256 hash for single block

        :param single_block: block
        :return: hex hash representation
        """

        # dict must be sorted by key
        single_block_str = json.dumps(single_block, sort_keys=True).encode()
        return sha256(single_block_str).hexdigest()

    @staticmethod
    def proof_validation(prev_proof: int, curr_proof: int) -> bool:
        """
        validation of a proof: hash(prev_proof, curr_proof) start with '0123'

        :param prev_proof: previous proof
        :param curr_proof: current proof
        :return: True if proved, False otherwise
        """
        return sha256(f'{prev_proof}{curr_proof}'.encode()).hexdigest()[:4] == "0123"
