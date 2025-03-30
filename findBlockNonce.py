#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, transactions):
    """
        k - Number of trailing zeros in the binary representation (integer)
        prev_hash - the hash of the previous block (bytes)
        transactions - a set of "transactions," i.e., data to be included in this block (list of strings)

        Finds a nonce such that 
        sha256( prev_hash + transactions + nonce )
        has k trailing zeros in its *binary* representation
    """
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'

    # Combine prev_hash and transactions into a single byte string
    block_data = prev_hash + ''.join(transactions).encode('utf-8')

    nonce = 0
    while True:
        # Convert nonce to bytes
        nonce_bytes = str(nonce).encode('utf-8')

        # Compute the hash of the block data + nonce
        hash_result = hashlib.sha256(block_data + nonce_bytes).digest()

        # Convert the hash to binary and check the number of trailing zeros
        binary_hash = bin(int.from_bytes(hash_result, byteorder='big'))
        if binary_hash[-k:] == '0' * k:
            assert isinstance(nonce_bytes, bytes), 'nonce should be of type bytes'
            return nonce_bytes

        # Increment nonce for the next attempt
        nonce += 1


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 20

    transactions = get_random_lines(filename, num_lines)
    nonce = mine_block(diff, transactions)
    print(nonce)
