import tatumclient
import os
from dotenv import load_dotenv
load_dotenv()


def get_ipfs_file(ipfs_cid):
    """
    Retrieves the NFT json file of given cid from IPFS system 

            Parameters:
                    ipfs_cid (str): The IPFS file ID to retrieve

            Returns:
                    nft_json (json): json file stored in IPFS for the given nft
    """
    connection = tatumclient.TatumClient.get_connection()
    GET_headers = {'x-api-key': os.getenv("tatumKey")}
    connection.request(
        "GET", f"/v3/ipfs/%7B{ipfs_cid}%7D", headers=GET_headers)
    response = connection.getresponse()
    data = response.read()
    print(data.decode("utf-8"))


def store_ipfs_file(file):
    """
    Stores the given NFT json file to IPFS system 

            Parameters:
                    file (json): The NFT json file tp stpre tp IPFS

            Returns:
                    ipfs_cid (str): IPFS file id for the stored json
    """
    connection = tatumclient.TatumClient.get_connection()
    POST_headers = {
        'content-type': "multipart/form-data",
        'x-api-key': os.getenv("tatumKey")
    }
    connection.request("POST", "/v3/ipfs", body=file,
                       headers=POST_headers, encode_chunked=True)
    response = connection.getresponse()
    data = response.read()
    print(data.decode("utf-8"))
