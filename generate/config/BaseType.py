from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class NcType:
    """nc变量类型别名定义, 方便统一定义使用类型
    """
    byte: str   = 'i1'
    ubyte: str  = 'u1'
    short: str  = 'i2'
    ushort: str = 'u2'
    int: str    = 'i4'
    uint: str   = 'u4'
    int64: str  = 'i8'
    uint64: str = 'u8'
    float: str  = 'f4'
    double: str = 'f8'
    string: str = 'str'


@dataclass
class NcDim:
    name: str
    value: int
    
    def __hash__(self) -> int:
        return hash((self.name, self.value))


@dataclass
class NcName:
    """设备生成nc文件时,部分文件名配置"""        
    class01: str                # 一级分类名
    class02: str                # 二级分类名
    class03: str                # 三级分类名
    class04: str                # 四级分类名
    base: str                   # 基地代码
    station_code: str           # 站点代码 需要生成时确定，可配置为空字符串即不使用
    data_code: str              # 设备资料代码
    manufacturer: str           # 厂商代码
    data_level: str             # 数据级别
    start_time: str             # 数据起始时间 需要生成时确定，可配置为空字符串即不使用
    format_code: str            # 格式标识带代码
    quality_control: bool = False   # 质控标识


@dataclass
class BaseObsData:
    """观测要素信息的数据类
    """
    key: str        # 传入数据中对应的键值 若传入数据中不存在此字段 设置为None
    name: str       # nc变量名
    nc_typ: str     # nc变量类型
    dim: Tuple[NcDim]      # nc变量维度
    longname: str   # nc变量longname属性
    units: str      # nc变量units属性


@dataclass
class BaseHeadData:
    """头文件描述信息的数据类 带有默认参数值
    """
    key: str        # 传入数据中对应的键值 若传入数据中不存在此字段 设置为None
    name: str       # nc变量名
    nc_typ: str     # nc变量类型
    dim: Tuple[NcDim]      # nc变量维度
    longname: str   # nc变量longname属性
    units: str      # nc变量units属性
    value: Any      # 头文件描述字段nc变量的默认初始值