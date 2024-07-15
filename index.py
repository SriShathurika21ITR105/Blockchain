import hashlib
import json
from time import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4 # Adjust the difficulty of PoW
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.create_block(0, "0", int(time()), "Genesis Block", 0)
        self.chain.append(genesis_block)

    def create_block(self, index, previous_hash, timestamp, data, nonce):
        block_data = f"{index}{previous_hash}{timestamp}{data}{nonce}"
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()
        return Block(index, previous_hash, timestamp, data, block_hash, nonce)

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = self.mine_block(len(self.chain), last_block.hash, int(time()), data)
        self.chain.append(new_block)

    def mine_block(self, index, previous_hash, timestamp, data):
        nonce = 0
        while True:
            block = self.create_block(index, previous_hash, timestamp, data, nonce)
            if block.hash[:self.difficulty] == "0" * self.difficulty:
                return block
            nonce += 1

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != hashlib.sha256(f"{current_block.index}{current_block.previous_hash}{current_block.timestamp}{current_block.data}{current_block.nonce}".encode()).hexdigest():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f" Previous Hash: {block.previous_hash}")
            print(f" Timestamp: {block.timestamp}")
            print(f" Data: {block.data}")
            print(f" Hash: {block.hash}")
            print(f" Nonce: {block.nonce}\n")

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block("First Block after Genesis")
    blockchain.add_block("Second Block after Genesis")

    blockchain.print_chain()
    print(f"Is blockchain valid? {blockchain.is_chain_valid()}")

    