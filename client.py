import requests
import json

from flask import jsonify


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getQty",
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()

    # assert response["result"] == "echome!"
    # assert response["jsonrpc"]
    # assert response["id"] == 0

    buffer = ''
    buffer += str(response)  ## adding the response to the buffer

    print(response)


#
#

if __name__ == "__main__":
    main()
