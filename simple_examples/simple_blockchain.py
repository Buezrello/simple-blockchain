import hashlib
import datetime


class SingleBlock:
    def __init__(self, block_index, timestamp, data, prev_hash):
        self.block_index = block_index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hash_hex()

    def hash_hex(self) -> str:
        sha = hashlib.sha256()
        sha.update(str(self.block_index).encode())
        sha.update(str(self.timestamp).encode())
        sha.update(str.encode(self.data))
        sha.update(str.encode(self.prev_hash))
        return sha.hexdigest()

    def __str__(self):
        return self.data + "\nHash: " + self.hash


def next_block(prev_block: SingleBlock):
    curr_index = prev_block.block_index + 1
    curr_timestamp = datetime.datetime.now()
    curr_data = "This is a block #" + str(curr_index)
    prev_hash = prev_block.prev_hash
    return SingleBlock(curr_index, curr_timestamp, curr_data, prev_hash)


if __name__ == '__main__':
    blockchain = [SingleBlock(0, datetime.datetime.now(), "First block", "0")]

    max_blocks = 10

    for _ in range(max_blocks):
        prev_block = blockchain[-1]
        new_block = next_block(prev_block)
        blockchain.append(new_block)
        print("Add new block #{} to the blockchain".format(new_block.block_index))

    print()
    print(*blockchain, sep="\n")
