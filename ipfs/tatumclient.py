import http.client
import os
from dotenv import load_dotenv
load_dotenv()

# Singleton class


class TatumClient(object):
    """
    A Singleton class to represent connection to TATUM API for IPFS Storage.

    ...

    Attributes
    ----------
    _connection : connection
        Connection object to TATUM API
    """
    _connection = None  # private global variable

    def __init__(self):
        if TatumClient._connection != None:
            raise Exception(
                "Tatum Connection is a singleton class with private constructor. Use get_connection() to get instance")
        else:
            TatumClient._connection = http.client.HTTPSConnection(
                os.getenv("tatumURL"))

    @staticmethod
    def get_connection():
        """"
        Returns the connection object to TATUM API for IPFS storage using Singleton pattern
        """
        if TatumClient._connection is None:
            TatumClient()
        return TatumClient._connection
