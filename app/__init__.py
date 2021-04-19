from flask import Flask
from uuid import uuid4

from almost_real_blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()
node_id = str(uuid4()).replace('-', '')  # unique node address

from app import routes, blockchain
