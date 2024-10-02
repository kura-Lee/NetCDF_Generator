from copy import deepcopy
from datetime import datetime
import logging
import os
import time
from typing import Dict, List, Tuple, Union
from pprint import pformat
import netCDF4 as nc
import numpy as np

from .config.BaseType import NcDim, NcName, NcType, BaseHeadData, BaseObsData
from log import get_default_logger


logger = get_default_logger(os.path.basename(__file__), log_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "log/log.txt"))
logger.setLevel(logging.INFO)


class NcGenerator(object):
    def __init__(self,
                 nc_config: dict,
                 head_data_cls = BaseHeadData,
                 observation_data_cls = BaseObsData
                 ) -> None:
        """nc文件信息类
        Args:
            nc_config (Dict): 生成配置字典,包含三个键值对,分别是描述信息desc, 要素信息obs, 文件名name,注意只有'name'是指定键名,用于生成文件名,其余两个键可自定义名称
                desc (Dict[List[Tuple]] / List[Tuple]): 描述信息元组字典或列表：{"grop_name": [(db_key, (name, nc_typ, dim, longname, units, value)), ...], ...}
                obs (Dict[List[Tuple]] / List[Tuple]): 要素信息元组字典或列表： {"group_name": [(name, nc_typ, dim, longname, units), ...] 或 [(db_key, (name, nc_typ, dim, longname, units)), ...], ...}
                name (List): nc文件名配置参数
        """    
        self.unique_dims = set()                    # 维度信息
        self.nc2data = {}                           # nc变量到实际数据名的映射表
        name = nc_config.get('name', None)
        if name is None:
            self.name = None
        else:
            self.name = NcName(*nc_config.pop('name'))  # 生成的nc文件名
        keys = list(nc_config.keys())
        if len(keys) == 0:
            raise ValueError(f"There are no valid data items in the configuration:\n{nc_config}")
        assert len(keys) == 2, f"Two items must be configured in:\n{nc_config}"
        self.head = self._parse_dict({keys[0]: nc_config.pop(keys[0])}, DataClass=head_data_cls)                          # 头部描述信息
        self.observation = self._parse_dict(nc_config, DataClass=observation_data_cls)     # 要素信息
        self.unique_dims = list(self.unique_dims)
          
    def _parse_datas(self, datas: Union[Tuple | List[Tuple]], DataClass):
        if not isinstance(datas, list):
            datas = [datas]
        grpl = []
        for row in datas:
            if len(row) == 2 and isinstance(row[1], tuple):
                if row[0] == '+':           # 实际变量名与生成nc文件名相同
                    grpl.append(DataClass(row[1][0], *row[1]))
                    self.nc2data[row[1][0]] = row[1][0]
                elif row[0] == '-':         # 无实际变量名，仅使用默认值生成
                    if issubclass(DataClass, BaseHeadData):
                        grpl.append(DataClass(None, *row[1]))
                    elif issubclass(DataClass, BaseObsData):
                        raise ValueError(f"{DataClass} no support use '-' to omit data.")
                    else:
                        raise ValueError(f"unknown DataClass:{DataClass}")
                else:
                    grpl.append(DataClass(row[0], *row[1]))
                    self.nc2data[row[1][0]] = row[0]
            elif isinstance(row, tuple):    # 实际变量名与生成nc文件名相同
                grpl.append(DataClass(row[0], *row))
                self.nc2data[row[0]] = row[0]
            else:
                raise ValueError(f"not support formate at {row}")
            var_dims = []                   # 记录每个变量的实际的维度变量名,方便生成直接使用
            for _dim in grpl[-1].dim:       # 记录唯一维度信息
                self.unique_dims.add(NcDim(*_dim))
                var_dims.append(_dim[0])
            grpl[-1].dim = tuple(var_dims)
                
        return grpl

    def _parse_dict(self, data: dict, DataClass):
        res = {}
        def _recursion(data, DataClass, res):
            for grpName, grpData in data.items():
                if isinstance(grpData, dict):
                    res[grpName] = _recursion(grpData, DataClass, deepcopy(res))
                elif isinstance(grpData, (list, tuple)):
                    res[grpName] = self._parse_datas(grpData, DataClass)
                else:
                    raise ValueError(f"values of {grpName} must be {DataClass}.")
            return res
        _recursion(data, DataClass, res)
        return res

    def generate_fileanme(self, start_time):
        """生成nc文件名

        Args:
            start_time (_type_): _description_

        Returns:
            _type_: _description_
        """
        if self.name is None:
            return ''
        try:
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d_%H%M%S")
        except ValueError:
            # 带毫秒数据的处理
            dt_str, ms_str = start_time.split('.')
            ms_str = "_" + ms_str
            start_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d_%H%M%S") + ms_str
        # 依次对各项数据进行连接
        if self.name.station_code:
            filename = "_".join((self.name.class01,
                                 self.name.class02,
                                 self.name.class03,
                                 self.name.class04,
                                 self.name.base,
                                 self.name.station_code,
                                 self.name.data_code,
                                 self.name.manufacturer_code,
                                 self.name.data_level,
                                 start_time))
        else:
            filename = "_".join((self.name.class01,
                                 self.name.class02,
                                 self.name.class03,
                                 self.name.class04,
                                 self.name.base,
                                 self.name.data_code,
                                 self.name.manufacturer_code,
                                 self.name.data_level,
                                 start_time))
        if self.name.format_code is not None:
            filename = f"{filename}_{self.name.format_code}"
        # 质控选项, 默认为TRUE
        if self.name.is_quality_control:
            filename += '_QC'
        filename += '.nc'
        
        return filename

    def _generate_dimension(self, nc_obj: nc._netCDF4):
        for dim_info in self.unique_dims:
            dim_var = nc_obj.createDimension(dim_info.name, dim_info.value)
            logger.debug(f"create dim_var:{dim_var.name} size:{dim_var.size}")
            
    def _update_head(self, data, current_dict, time_st="", time_end=""):
        for head_grp_name in current_dict.keys():
            head_datas = current_dict[head_grp_name]
            if isinstance(head_datas, dict):
                self._update_head(data, head_datas, time_st, time_end)
            else:
                for i in range(len(head_datas)):
                    head_var = current_dict[head_grp_name][i]
                    if head_var.key is not None:
                        current_dict[head_grp_name][i].value = data[head_var.key]
                    elif time_st and head_var.name == "Obse_begi_DT":
                        current_dict[head_grp_name][i].value = time_st
                    elif time_end and head_var.name == "Obse_end_DT":
                        current_dict[head_grp_name][i].value = time_end
                    elif head_var.name == "Data_crea_DT":
                        current_dict[head_grp_name][i].value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def _create_var(self, nc_obj: nc._netCDF4, data_info, datas, accumulate_desc=False):
        for grp_name, grp_data in data_info.items():
            if len(grp_data) == 0:                                      # 跳过空的组
                continue
            grp_obj = nc_obj.createGroup(grp_name)
            if isinstance(grp_data, dict):
                self._create_var(grp_obj, grp_data, datas, accumulate_desc)
            else:
                for info in grp_data:
                    if info.nc_typ != NcType.string:                    # 非字符类型nc变量压缩
                        var = grp_obj.createVariable(info.name, info.nc_typ, info.dim, compression="zlib")
                    else:
                        var = grp_obj.createVariable(info.name, info.nc_typ, info.dim)
                    if not accumulate_desc:                             # 不进行数据叠加
                        val = np.array(info.value, dtype=info.nc_typ)
                    else:                                               # 默认固定值(未设置对应数据的key) 或数据叠加
                        val = np.array([info.value for _ in datas], dtype=info.nc_typ) if info.key is None else \
                            np.array([d[info.key] for d in datas], dtype=info.nc_typ)
                    var[:] = val                                        # 数据存储
                    var.long_name = info.longname
                    var.units = info.units
                    
    def gerneral_nc(self, nc_path, datas: List):
        if datas[0].get('Datetime', None) is not None:
            logger.info(f"generate nc file: {datas[0]['Datetime']} ~ {datas[-1]['Datetime']}")
        time_st = datas[0].get('Datetime', '')
        time_ed = datas[-1].get('Datetime', '')
        self._update_head(datas[0], self.head, time_st, time_ed)    # 更新描述信息值
        output_dir, _ = os.path.split(nc_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        nc_obj = nc.Dataset(nc_path, "w", "NETCDF4")
        self._generate_dimension(nc_obj)                            # 生成维度信息
        self._create_var(nc_obj, self.head, datas, accumulate_desc=False)
        self._create_var(nc_obj, self.observation, datas, accumulate_desc=True)
        nc_obj.close()                                          # 关闭文件
        logger.info(f"has generated nc file {nc_path}")

    def __repr__(self) -> str:
        return pformat({"head": self.head, 
                        "observation": self.observation, 
                        "nc2data": self.nc2data,
                        "unique_dims": self.unique_dims,
                        "name": self.name})