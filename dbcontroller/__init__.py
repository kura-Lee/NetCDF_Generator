# -*- coding:utf-8 -*-

# @Time : 21/11/03 PM 08:49
# @Author : LINZIJIE (linzijie1998@126.com)
# @Filename : __init__.py.py
# @Version: v0.1
# @License: GNU GENERAL PUBLIC LICENSE Version 3
# @Description: 连接MongoDB数据库，并且读取数据

import os
from typing import List, Union
import logging
from logging import getLogger
import pymongo
import gridfs
from pymongo import CursorType
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId
from dotenv import load_dotenv


load_dotenv()
logger = getLogger(os.path.basename(__file__))


class MyMongodb:
    def __init__(self, host: str, username: str, pwd: str, database: str, port=27017, maxPoolSize=2):
        """
        初始化设置

        :param host:        MongoDB数据库服务器IP地址
        :param username:    用户名
        :param pwd:         密码
        :param database:    要操作的数据库名
        :param port:        MongoDB数据库服务器端口，默认为27017
        :param maxPoolSize: MongoDB数据库服务器并发设置, 默认为2
        """
        self.link = rf"mongodb://{username}:{pwd}@{host}:{port}/" 
        self.client = pymongo.MongoClient(self.link, maxPoolSize=maxPoolSize)
        self.db = self.client[database]
        if self.client.list_database_names():
            logger.info(f"connect to mongo {host}:{self.db.name} database.")
        
    def change_db(self, db_name: str):
        """将操作切换到指定数据库

        Args:
            db_name (str): 要切换到的数据库名
        """
        self.db = self.client[db_name]
        logger.info(f"change to {self.db.name} database.")
        return self
    
    def list_colls(self) -> List:
        """列出此数据库中的集合

        Returns:
            List: 集合列表
        """
        colls = self.db.list_collection_names()
        logger.debug(f"collections in {self.db.name}: {colls}")
        return colls
    
    def get_docs(self, coll_name: str, sortby: Union[str, list]=None, sql: dict=None, limit: int=None) -> CursorType:
        """
        根据sql进行数据的处理
        """
        if sql == None:
            table_data = self.db[coll_name].find()                 # 查询集合（表）中所有数据
        else:
            table_data = self.db[coll_name].find(sql)        # 根据条件查询集合（表）中的数据
        if sortby:
            table_data = table_data.sort(sortby)
        if limit:
            table_data = table_data.limit(limit)
        return table_data
    
    def get_field_distinct(self, coll_name: str, field: str):
        """获取集合中field字段的唯一值集合

        Args:
            field (str): 文档中的字段名
        """
        data = self.db[coll_name].distinct(field)
        return data
        
    def save_docs(self, data: Union[list, dict], coll_name: str, extend_dict: dict={}) -> int:
        """
        保存文档(行数据)到指定集合
        """
        if isinstance(data, dict):
            data = [data]
        colle = self.db[coll_name]
        if extend_dict:
            for e in data:
                e.update(extend_dict)
        cnt = 0
        chunk = 1000                # 一次最多存储的条数
        data_len = len(data)
        for st in range(0, data_len, chunk):
            res = colle.insert_many(data[st: st+chunk])
            cnt += len(res.inserted_ids)
        logger.info(f"{cnt} document are inserted into {coll_name} collection in {self.db.name} database.")
        return cnt
    
    def update_one(self, coll_name: str, fit: dict, update: dict) -> bool:
        """更新集合中的单个文档

        Args:
            coll_name (_type_): _description_
            fit (_type_): _description_
            update (_type_): _description_
        """
        if coll_name in self.db.list_collection_names():
            colle = self.db[coll_name]
            up_res = colle.update_one(fit, {"$set":update})
            return up_res.modified_count
        else:
            logger.debug(f"collection {coll_name} not exist!")
            return 0
    
    def update_many(self, coll_name: str, fit: dict, update: dict) -> int:
        """更新集合中的多个文档

        Args:
            coll_name (_type_): _description_
            fit (_type_): _description_
            update (_type_): _description_
        """
        if coll_name in self.db.list_collection_names():
            colle = self.db[coll_name]
            up_res = colle.update_many(fit, {"$set":update})
            logger.debug(f"update count:{up_res.modified_count}")
            return up_res.modified_count
        else:
            logger.debug(f"collection {coll_name} not exist!")
            return 0
    
    def update_key_many(self, coll_name: str, update_map: dict):
        """更新集合中的一个或多个键的名称

        Args:
            coll_name (_type_): _description_
            update_map (_type_): 更新字典 {旧键名: 新键名}
        """
        colle = self.db[coll_name]
        res = colle.update_many({}, {"$rename": update_map})
        logger.debug(f"modify {res.modified_count} doc.")
        return res.modified_count
    
    def create_single_index(self, coll_name, field_name):
        """
        创建升序索引（若存在会删除原有的）
        """
        collection = self.db[coll_name]
        try:
            collection.drop_index(field_name)
            index_name = collection.create_index([(field_name, pymongo.ASCENDING)])
            logger.debug(f"create index in {self.db.name}.{coll_name}['{field_name}'] named {index_name}.")
            return True
        except OperationFailure:
            return False
        
    def rename_collection(self, coll_name: str, new_name: str) -> bool:
        """
        重新命名集合
        """
        try:
            colle = self.db[coll_name]
            colle.rename(new_name)
            return True
        except OperationFailure:
            return False
    
    def remove_coll(self, coll_name: str) -> bool:
        """删除数据"""
        try:
            self.db[coll_name].drop()
            return True
        except OperationFailure:
            return False
  

    def remove_docs(self, coll_name: str, filter_map: dict):
        """删除数据"""
        colle = self.db[coll_name]
        doc = colle.delete_many(filter_map)
        return doc
        
    def save_lfs(self, file, coll='fs') -> ObjectId:
        """分布式存储大文件到当前数据库的存储桶，默认名为"fs", 返回存储文件的ObjectId对象

        Args:
            file: 数据,需要是二进制数据
            coll (str, optional): _description_. Defaults to 'fs'.
        """
        fs = gridfs.GridFS(self.db, collection=coll)
        return fs.put(file)
    
    def get_lfs(self, id: ObjectId, coll='fs'):
        """按给定ObjectId从存储桶中获取数据, 返回读取后的文件数据
        Args:
            id (ObjectId): 文件_id对象
            coll (str, optional): 存储桶表名. Defaults to 'fs'.
        """
        fs = gridfs.GridFS(self.db, collection=coll)
        return fs.get(id).read()
        
    def close_mongodb_client(self):
        """
        关闭MongoDB数据库连接
        """
        self.client.close()


def get_mongo_cilent():
    return MyMongodb(os.getenv('MONGO_IP'), 
                     os.getenv('MONGO_USER'),
                     os.getenv('MONGO_PASSWD'),
                     os.getenv('MONGO_DB'),
                     maxPoolSize=10)


if __name__ == "__main__":
    # 通用mongo数据库对象 注意可调整数据库
    mongo = get_mongo_cilent()
    mongo.list_colls()
    # print(mongo.link)