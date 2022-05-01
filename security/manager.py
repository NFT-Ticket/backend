from pydoc import plain
from re import S
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()


SYMMETRIC_KEY = str.encode(os.getenv("SYMMETRIC_KEY"))


def encrypt(data):
    '''Encrypts the data using symmetric key and returns a cipher text'''
    data = str.encode(data)
    return Fernet.encrypt(Fernet(SYMMETRIC_KEY), data)


def decrypt(cipher):
    '''Takes the cipher text and decrypts it using symmetric key'''
    return Fernet.decrypt(Fernet(SYMMETRIC_KEY), cipher).decode()
