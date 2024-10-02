'''
Author: Zhong Xiao Wei 56347761+kura-Lee@users.noreply.github.com
Date: 2023-11-26 22:00:31
LastEditTime: 2024-09-27 15:07:56
FilePath: /Dataset_build/parse/station_data/__init__.py
Description: 

Copyright (c) 2023 by Zhongxiaowei, All Rights Reserved. 
'''
import json
import os

from log import get_default_logger

EQUIPMENT_JSON_FILE_MAP = {
    "RRD":"microrain_station.json",
}
logger = get_default_logger(os.path.basename(__file__))
current_dir = os.path.dirname(__file__)



def _get_station_info(station_id, json_file, return_default=False):
    """根据配置json获取站点信息

    Args:
        station_id (str): 站点ID
        json_file (str): json文件路径
        return_default (bool): 不存在此键时返回默认站点,默认关闭 
    Raises:
        ValueError: json文件最好配置键"_default"作为没有station_id不存在时返回的数据
                    若未开启return_default,则在站点不存在时报错
    Returns:
        _type_: _description_
    """
    with open(json_file, "r", encoding='utf8') as fp:
        stations = json.load(fp)
    if station_id in stations:
        return stations[station_id]
    elif return_default:
        logger.info(f"unknow station:{station_id}, use default.")
        if "_default" not in stations:      # 自动生成'_default'
            stations['_default'] = {k: "0" for k in stations[stations.keys()[0]].keys()}
        default_dict = stations['_default']
        return default_dict
    else:
        raise ValueError(f"unknow station:{station_id}.")


def get_station_info(equipment, station_id) -> dict:
    """根据设备类型和站点代号获取信息的字典

    Args:
        equipment (str): 设备名
        station_id (str): 站点代号

    Returns:
        _type_: 站点信息字典
    """
    json_file_name = EQUIPMENT_JSON_FILE_MAP.get(equipment, None)
    if json_file_name is None:
        raise KeyError(f"not support equipment: {equipment}, please chiose in {EQUIPMENT_JSON_FILE_MAP.keys()}")
    json_file = os.path.join(current_dir, json_file_name)
    return _get_station_info(station_id, json_file)


if __name__ == '__main__':
    pass
    # station = get_microrain_station_info("1")
    # print(station)