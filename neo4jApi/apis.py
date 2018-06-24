from neo4jApi.utils import transaction_commit

# 获取单挑语句执行结果
def get_response(cypher):
    response = transaction_commit(cypher)
    data = response.json()['results'][0]['data']
    return data

# 获取子图，返回节点和边
def get_sub_graph(cypher):
    data = get_response(cypher)
    nodes = []
    edges = []
    for path in data:
        row = path['row'][0]
        meta = path['meta'][0]
        for i in range(len(row)):
            obj = row[i]
            if meta[i]['type'] == 'node':
                if obj not in nodes:
                    nodes.append(obj)
        for i in range(len(row)):
            obj = row[i]
            if meta[i]['type'] == 'relationship':
                obj['resource'] = nodes.index(row[i-1])
                obj['target'] = nodes.index(row[i + 1])
                if obj not in edges:
                    edges.append(obj)
    return nodes,edges


# 返回整个图
def search_graph(limit):
    statement = "MATCH p=()-[]-() RETURN p limit %d" % (limit)
    statement = "{\"statement\" : \"%s\" }" % statement
    cypher = "{\"statements\" : [%s]}" % statement
    return get_sub_graph(cypher)

# 搜索子树，name是搜索节点名称，low_level是展示的最低层级数，high_level是最高层数
def search_sub_tree(name,low_level,high_level):
    statement = "MATCH p=(n{name:'%s'})-[r*%d..%d]->(m) return p" % (name,low_level,high_level)
    statement = "{\"statement\" : \"%s\" }" % statement
    cypher = "{\"statements\" : [%s]}" % statement
    return get_sub_graph(cypher)



if __name__ == '__main__':
    # cypher = "{\"statements\" : [{\"statement\" : \"MATCH p=(n{name:'人工智能'})-[r*1..3]->(m) return p\" } ]}"
    # nodes, edges = get_sub_tree(cypher)
    # print(nodes)
    # print(edges)
    # cypher = "{\"statements\" : [{\"statement\" : \"match p=()-[]-() return p\" } ]}"
    # print(get_response(cypher))
    print(search_sub_tree("人工智能",1,3))