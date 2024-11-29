import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def add_block(self, data):
        sanitized_data = data.replace(",", ";")  
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.datetime.now(),
            data=sanitized_data,
            previous_hash=last_block.current_hash,
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.current_hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.current_hash:
                return False
        return True

    def save_to_file(self, filename="blockchain_data.txt"):
        with open(filename, "w") as file:
            for block in self.chain:
                file.write(f"{block.index},{block.timestamp},{block.data},{block.previous_hash},{block.current_hash}\n")

    def load_from_file(self, filename="blockchain_data.txt"):
        try:
            with open(filename, "r") as file:
                self.chain = []
                for line in file.readlines():
                    parts = line.strip().split(",")
                    if len(parts) < 5:
                        raise ValueError(f"Invalid blockchain record: {line.strip()}")

                    index = int(parts[0])
                    timestamp = parts[1]
                    data = ",".join(parts[2:-2]) 
                    previous_hash = parts[-2]
                    current_hash = parts[-1]

                    block = Block(index, timestamp, data, previous_hash)
                    block.current_hash = current_hash
                    self.chain.append(block)
        except FileNotFoundError:
            self.chain = [self.create_genesis_block()]
