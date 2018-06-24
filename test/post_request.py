import requests

if __name__=='__main__':
    url = "http://10.108.211.136:7474/db/data/transaction/commit"

    payload = "{\"statements\" : [{\"statement\" : \"MATCH p=(n{name:'人工智能'})-[r*1..3]->(m) return p\" } ]}".encode('utf-8')
    headers = {
        'accept': "application/json",
        'content-type': "application/json; charset=UTF-8",
        'authorization': "Basic bmVvNGo6dm5pcXVl",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)