from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("FERNET_KEY")

if not key:
    raise ValueError("FERNET_KEY not set in environment")

cipher = Fernet(key.encode())

def encrypt_message(msg: str) -> bytes:
    return cipher.encrypt(msg.encode())

def decrypt_message(msg: bytes) -> str:
    return cipher.decrypt(msg).decode()