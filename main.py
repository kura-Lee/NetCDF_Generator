from generate import NcGenerator
from generate.config.microrain_radar_cfg import MicroRianRadarRawNCINFO
from dbcontroller import get_mongo_cilent


# 连接数据库,获取数据
db_client = get_mongo_cilent()
couser = db_client.get_docs('RRD_Lraw', limit=10)
# print(list(couser))

# 按配置数据nc生成器实例
gc = NcGenerator(MicroRianRadarRawNCINFO)
print(gc)

# 传入数据生成nc
gc.gerneral_nc('test.nc', list(couser))