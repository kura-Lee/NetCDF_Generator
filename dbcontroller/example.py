
from dbcontroller import MyMongodb, get_mongo_cilent
from log import Tee

def print_line():
    print('='*20)

# 日志记录器,将stdout和stderr同时输出到文件中
Tee(name="log")
    
# ip 用户名 密码 数据库(不存在会在存储数据时自动创建)
db_client = get_mongo_cilent()


print_line()
# 切换mongoDB操作对象到guizhou_test数据库
db_client.change_db("guizhou_test")


print_line()
# 列出guizhou_test数据库中的集合(表)
db_client.list_colls()


print_line()
# 获取微波辐射计表的数据, 返回一个可遍历的游标对象,其每个元素即为表的每一行数据字典
datas = db_client.get_docs(coll_name="MRD")
print(type(datas))
# 一般采用循环遍历输出
for data in datas:
    print(data)
# # 数据量较少可以将其直接转换为列表(不推荐)
# print(list(datas))


print_line()
# 存储List[Dict]/Dict数据到test表(不存在会自动创建)中 返回存入的数据条数
datas = [{"test_field": 123, "field1": "你好"}]
db_client.save_docs(datas, coll_name="test")


print_line()
#查看我们刚才写入test集合的数据
print(list(db_client.get_docs(coll_name="test")))


print_line()
# 更新test表中field1字段的名称为field111
db_client.update_key_many(coll_name="test", update_map={"field1":"field111"})
print(list(db_client.get_docs(coll_name="test")))


print_line()
# 更新test表中field111字段的值为"她好"
db_client.update_many(coll_name="test", fit={}, update={"field111": "她好"})
print(list(db_client.get_docs(coll_name="test")))


print_line()
# 删除test表中field111字段为"她好"的文档(行)
db_client.remove_docs(coll_name="test", filter_map={"field111": "她好"})
print(list(db_client.get_docs(coll_name="test")))


# 关闭数据库
db_client.close_mongodb_client()