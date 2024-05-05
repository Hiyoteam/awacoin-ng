from secrets import token_bytes, token_hex
from base64 import b64encode

class Wallet:
    public_key: str
    private_key: str
    balance: int
    def __init__(self):
        self.public_key=token_hex(32)
        self.private_key=b64encode(token_bytes(64)).decode()
        self.balance=0