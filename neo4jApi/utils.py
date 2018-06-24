import requests

# 执行cypher语句
def transaction_commit(cypher):
    url = "http://10.108.211.136:7474/db/data/transaction/commit"
    payload = cypher.encode('utf-8')
    headers = {
        'accept': "application/json",
        'content-type': "application/json; charset=UTF-8",
        'authorization': "Basic bmVvNGo6dm5pcXVl",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response