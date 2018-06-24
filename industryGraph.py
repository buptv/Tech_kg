from neo4jApi import apis
from flask import Flask, g, Response, request
import json

app = Flask(__name__, static_url_path='/static/')
@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

# 生产跨域允许response
def gen_response(response):
    res = Response(response, mimetype="application/json")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

# 根据关键词搜索子图
@app.route('/search/<name>', methods=['POST'])
@app.route('/search/<name>/<int:low_level>/<int:high_level>', methods=['POST'])
def search(name,low_level=1,high_level=3):
    response = json.dumps(apis.search_sub_tree(name,low_level,high_level))
    return gen_response(response)

# 查看图谱
@app.route('/graph', methods=['POST'])
@app.route('/graph/<limit>', methods=['POST'])
def graph(limit=10000):
    response = json.dumps(apis.search_graph(limit))
    return gen_response(response)

#添加叶子节点
@app.route("/add_node/<int:father>/<int:father_level>/<name>/<label>/<r_type>/<r_name>",methods=['GET', 'POST'])
def add_node(father,father_level,name,label,r_type,r_name):
    response = json.dumps(apis.add_node(father,father_level,name,label,r_type,r_name))
    return gen_response(response)

#删除节点
@app.route("/del_node/<id>",methods=['GET', 'POST'])
def del_node(id,):
    response = json.dumps(apis.del_node(id))
    return gen_response(response)

#修改节点属性
@app.route("/mod_node/<id>/<name>",methods=['GET', 'POST'])
def mod_node(id,name):
    response = json.dumps(apis.mod_node(id,name))
    return gen_response(response)

#添加关系
@app.route("/add_rel/<father>/<son>/<r_type>/<r_name>",methods=['GET', 'POST'])
def add_rel(father,son,r_type,r_name):
    response = json.dumps(apis.add_rel(father,son,r_type,r_name))
    return gen_response(response)

#删除关系
@app.route("/del_rel",methods={'POST','GET'})
def del_rel(father,son,r_type,r_name):
    response = json.dumps(apis.del_rel(father, son, r_type, r_name))
    return gen_response(response)

#修改关系属性
@app.route("/mod_rel",methods={'POST','GET'})
def mod_rel(father,son,r_type,r_name,new_name):
    response = json.dumps(apis.mod_rel(father,son,r_type,r_name,new_name))
    return gen_response(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5008)


# @app.route('/test')
# def test():
#     db = get_db()
#     results = db.run("MATCH (industry:产业) RETURN industry")
#     print(type(results))
#     for result in results:
#         print(result)
#     return "ok"
#
# def serialize_node(node):
#     return {
#         'id': node.id,
#         'type': list(node.labels)[0],
#         'father': node['father'],
#          'level': node['level'],
# 	'name': node['name']
#     }
#
# def serialize_rel(nodeFlag,rel):
#     return {
#         'id': rel.id,
#         'source': nodeFlag[rel.start],
#         'target': nodeFlag[rel.end],
#         'rel': rel.type,
#         'name': rel['name']
#     }
#
# def serialize_rel_manmade(nodeFlag,rel):
#     return {
#         'source': nodeFlag[rel['start']],
#         'target': nodeFlag[rel['end']]
#     }
#
# def serialize_enterprise(enterprise):
#     return {
#         'uni_code': enterprise[0],
#         'com_name': enterprise[1],
#     }
#
# # 返回结果
# def gen_response(results):
#     nodes = []
#     rels = []
#     i = 0
#     for record in results:
#         node = record["n"]
#         rel = record["r"]
#         # print(node)
#         # print(rel)
#         nodes.append(node)
#         rels.append(rel)
#     # print(len(nodes))
#     # print(len(rels))
#     nodes = list(set(nodes))
#     rels = list(set(rels))
#     nodeFlag = {}
#     for i in range(0, len(nodes)):
#         nodeFlag[nodes[i].id] = i
#     print(nodeFlag)
#     # print(len(nodes))
#     # print(len(rels))
#     res = Response(dumps(
#         {"nodes": [serialize_node(node) for node in nodes], "links": [serialize_rel(nodeFlag, rel) for rel in rels]}),
#                    mimetype="application/json")
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     return res
#
# def gen_response_path(results):
#     nodes = []
#     rels = []
#     i = 0
#     for record in results:
#         print(record)
#         path = record['p']
#         # print(path)
#         start = path.start
#         end = path.end
#         rel = {'start': start.id, 'end': end.id}
#         if start not in nodes:
#             nodes.append(start)
#         if end not in nodes:
#             nodes.append(end)
#         rels.append(rel)
#     nodeFlag = {}
#     for i in range(0, len(nodes)):
#         nodeFlag[nodes[i].id] = i
#     res = Response(dumps(
#         {"nodes": [serialize_node(node) for node in nodes], "links": [serialize_rel_manmade(nodeFlag, rel) for rel in rels]}),
#         mimetype="application/json")
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     return res
#
#
# @app.route("/find_enterprise",methods=['GET', 'POST'])
# def find_enterprise():
#     print("进入find_enterprise()方法——————")
#     if request.method == 'POST':
#         enterprises = mysql.select_enterprise()
#         print(enterprises)
#         res = Response(dumps({"enterprises": [serialize_enterprise(enterprise) for enterprise in enterprises]}), mimetype="application/json")
#         res.headers['Access-Control-Allow-Origin'] = '*'
#         return res
#     else:
#         return "请使用POST请求"
#
# #
# @app.route("/add_enterprise",methods=['GET', 'POST'])
# def add_enterprise():
#     print("进入add_enterprise()方法——————")
#     if request.method == 'POST':
#         print(request.values)
#         father = request.form['father'].strip()
#         print(father)
#         r_name = request.form['r_type'].strip()
#         print(r_name)
#         r_type = request.form['r_type'].strip()
#         enterprises = request.form["enterprises"]
#         enterprises = json.loads(enterprises)
#         print(enterprises)
#         print(type(enterprises))
#         try:
#             db = get_db()
#             print("1111111")
#             for enterprise in enterprises:
#                 print("2222222")
#                 print(type(enterprise))
#                 print(enterprise)
#                 print(enterprise["com_name"])
#                 print(enterprise["uni_code"])
#                 cypher = "match (father) where ID(father)=%s create (son:%s{father:%s,name:'%s',uni_code:'%s',level:%s}) create (father)-[:%s{name:'%s'}]->(son)" % (
#                 father, "企业", father, enterprise["com_name"], enterprise["uni_code"], 12, r_type, r_name)
#                 print("44444")
#                 print(cypher)
#                 results = db.run(cypher)
#                 print(results)
#             print("33333333")
#             mysql.updata_enterprise_import_flag(enterprises)
#             return get_graph(100000)
#         except:
#             print("add_enterprise方法失败---")
#             return "添加失败---"
#     else:
#         print("请使用POST请求")
#         return "请使用POST请求"
#
# #查看图谱
# @app.route("/graph/<limit>",methods=['GET', 'POST'])
# def get_graph(limit):
#     db = get_db()
#     results = db.run("MATCH (n)-[r]-() RETURN n,r "
#              "LIMIT {limit}", {"limit": int(limit)})
#     res = gen_response(results)
#     return res
#
# #添加叶子节点
# @app.route("/add_node",methods=['GET', 'POST'])
# def add_node():
#     if request.method == 'POST':
#         father = request.form['father'].strip()
#         name = request.form['name'].strip()
#         label = request.form['label'].strip()
#         r_type = request.form['r_type'].strip()
#         r_name = request.form['r_name'].strip()
#         db = get_db()
#         cypher = "match (father) where ID(father)=%s return father.level" % (father)
#         for record in db.run(cypher):
#             father_level =record[0]
#         cypher = "match (father) where ID(father)=%s create (son:%s{father:%s,name:'%s',level:%s}) create (father)-[:%s{name:'%s'}]->(son)" % (father,label,father,name,father_level+1,r_type,r_name)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#     else:
#         return "请使用POST请求"
#
# #删除节点
# @app.route("/del_node",methods=['GET', 'POST'])
# def del_node():
#     if request.method == 'POST':
#         id = request.form['id'].strip()
#         db = get_db()
#         cypher = "MATCH (n)-[r]-() where ID(n)=%s delete n,r" % id
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#     else:
#         return "请使用POST请求"
#
# #修改节点属性
# @app.route("/mod_node",methods=['GET', 'POST'])
# def mod_node():
#     print(request.values)
#     print(request.form)
#     if request.method == 'GET':
#         id = request.values.get('id').strip()
#         name = request.values.get('name').strip()
#         db = get_db()
#         cypher = "match (from) where ID(from)=%s set from.name='%s'" % (id,name)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#     else:
#         # return "请使用POST请求"
#         id = request.form['id'].strip()
#         name = request.form['name'].strip()
#         db = get_db()
#         cypher = "match (from) where ID(from)=%s set from.name='%s'" % (id, name)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#
# #添加关系
# @app.route("/add_rel",methods=['GET', 'POST'])
# def add_rel():
#     if request.method == 'POST':
#         father = request.form['father'].strip()
#         son = request.form['son'].strip()
#         r_type = request.form['r_type'].strip()
#         r_name = request.form['r_name'].strip()
#         db = get_db()
#         #cypher = "match (from),(to) where ID(from)=%s and ID(to)=%s create (from)-[:%s{name:'%s'}]->(to)" % (father,son,r_type,r_name)
#         cypher = "match (from),(to) where ID(from)=%s and ID(to)=%s create (from)-[:%s{name:'%s'}]->(to)" % (father,son,r_type,r_name)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#     else:
#         return "请使用POST请求"
#
# #删除关系
# @app.route("/del_rel",methods={'POST','GET'})
# def del_rel():
#     if request.method == 'POST':
#         father = request.values.get('father').strip()
#         son = request.values.get('son').strip()
#         r_type = request.values.get('r_type').strip()
#         r_name = request.values.get('r_name').strip()
#         db = get_db()
#         cypher = "match (from)-[r:%s{name:'%s'}]->(to) where ID(from)=%s and ID(to)=%s delete r" % (r_type,r_name,father,son)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#     else:
#         return "请使用POST请求"
#
# #修改关系属性
# @app.route("/mod_rel",methods={'POST','GET'})
# def mod_rel():
#     if request.method == 'POST':
#         father = request.values.get('father').strip()
#         son = request.values.get('son').strip()
#         r_type = request.values.get('r_type').strip()
#         r_name = request.values.get('r_name').strip()
#         new_name = request.values.get('new_name').strip()
#         db = get_db()
#         cypher = "match (from)-[r:%s{name:'%s'}]->(to) where ID(from)=%s and ID(to)=%s set r.name='%s'" % (r_type,r_name,father,son,new_name)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         return get_graph(100000)
#     else:
#         return "请使用POST请求"
#
# # 搜索特定2级3级节点下的子图
# # MATCH p=(n{name:'人工智能'})-[r*1..3]->(m) return p
# @app.route("/search_subtree",methods={'POST','GET'})
# def search_subtree():
#     if request.method == 'POST':
#         name = request.values.get('name').strip()
#         deep = int(request.values.get('deep').strip())
#         db = get_db()
#         cypher = "MATCH p=(n{name:'%s'})-[r*1..%d]->(m) return p" % (name,deep if deep else 3)
#         print(cypher)
#         results = db.run(cypher)
#         print(results)
#         res = gen_response_path(results)
#         return res
#     else:
#         return "请使用POST请求"

