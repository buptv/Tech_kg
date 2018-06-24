import requests
import json
header={"Content-Type": "application/json"}

def createNode(d):
	url="http://localhost:7474/db/data/node"
	l=requests.post(url,data=json.dumps(d),headers=header)
	return l
def createRelation(n1,n2):
	n1=n1.json()
	n2=n2.json()
	url1=n1['create_relationship']
	url2=n2['self']
	d={'to':url2,'type':'is_connected'}
	requests.post(url1,data=json.dumps(d),headers=header)


if __name__=='__main__':
	d={'city':'gurgaon','state':'haryana'}
	d1={'city':'faridabad','state':'haryana'}
	n1=createNode(d)
	n2=createNode(d1)
	createRelation(n1,n2)