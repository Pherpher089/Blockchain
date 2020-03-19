# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'proof': proof,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True)

        '''
        this function turns a json object into a string. This allows us
        to hash the object.
        '''
        string_in_bytes = block_string.encode()
        print(f'String in bytes = {string_in_bytes}')
        '''
        This function turns our json block into bytes. 
        See the print?
        '''
        # TODO: Hash this string using sha256
        hash_obj = hashlib.sha256(string_in_bytes)
        '''This function hashes our string in bytes'''
        hash_string = hash_obj.hexdigest()
        '''This function turns our hash into a hexadecimal number'''
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hash_string

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     block_string = json.dumps(block, sort_keys=True)
    #     proof = 1
    #     while self.valid_proof(block_string, proof) == False:
    #         proof += 1

    #     return proof
    #     # return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == '000000'
        # return True or False
        '''
        $$$ This method will check the proof that is passed into it and return
        true or false. 
       '''


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/last_block', methods=['GET'])
def last_block():
    block = blockchain.chain[-1]
    responce = {
        'block': block
    }
    return jsonify(responce), 200


@app.route('/mine', methods=['POST'])
def mine():
    # Run the proof of work algorithm to get the next proof
    block = blockchain.last_block
    data = request.get_json()
    proof = data['proof']
    block_string = json.dumps(block, sort_keys=True)
    if blockchain.valid_proof(block_string, proof):
        # Forge the new Block by adding it to the chain with the proof
        block_hash = blockchain.hash(block)
        new_block = blockchain.new_block(proof, block_hash)
        response = {
            # TODO: Send a JSON response with the new block
            'message': 'block forged',
            'index': new_block['index'],
            'transactions': new_block['transactions'],
            'proof': new_block['proof'],
            'previous_hash': new_block['previous_hash']
        }

        return jsonify(response), 200
    else:
        responce = {
            'message': f'{proof} is not valid proof. Try again.'
        }
        return jsonify(responce), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'chain_length': len(blockchain.chain)
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
