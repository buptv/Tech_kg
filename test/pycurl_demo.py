import os
if __name__=='__main__':
    tmpres = os.popen('curl -u neo4j:vnique  http://localhost:7474/db/data').readlines()
    print(tmpres)
    print("ok..")