'''
Author: Zhong Xiao Wei 56347761+kura-Lee@users.noreply.github.com
Date: 2023-11-23 21:07:11
LastEditTime: 2024-10-02 22:27:22
FilePath: /Dataset_build/generate/config/microrain_radar_cfg.py
Description: 

Copyright (c) 2023 by Zhongxiaowei, All Rights Reserved. 
'''
from .BaseType import NcType


# nc维度变量名定义 元组形式:(维度变量名, 维度变量值)
Datetime = ('Datetime', None)
Dime_HGT_31 = ('Dime_HGT_31', 31)
Dime_HGT_32 = ('Dime_HGT_32', 32)
Dime_part_diam_clas = ('Dime_part_diam_clas', 64)

MicroRianRadarRawNCINFO = {
    # (input_data_name, (name nc_typ, dim, longname, units, value))
    "head":
        {   # 站点信息组
            "head_grp1": [
                ('station_name', ('Station_Name', NcType.string, (), 'Station name', '-', 'Xueshan')),
                ('station_id', ('Station_ID', NcType.string, (), 'Station identity', '-', '56691')),
                ('-', ('Country', NcType.string, (), 'Country', '-', 'China')),
                ('-', ('Province', NcType.string, (), 'Province', '-', 'Guizhou')),
                ('-', ('City', NcType.string, (), 'City', '-', 'Bijie')),
                ('-', ('County', NcType.string, (), 'County', '-', 'Weining')),
                ('latitude', ('LAT', NcType.float, (), 'Latitude', '°', 26.86)),
                ('longitude', ('LON', NcType.float, (), 'Longitude', '°', 104.28)),
                ('altitude', ('ALT', NcType.ushort, (), 'Altitude', 'm', 2234)),
                ('station_type', ('Station_type', NcType.ubyte, (), 'Station type', '-', 40)),
                ('station_level', ('Station_level', NcType.string, (), 'Station level', '-', 11)),
                ('-', ('Admi_code_CHN', NcType.string, (), 'Administrative area code of China', '-', '520526')),
            ],
            # 设备信息组
            "head_grp2": [
                ('-', ('Mete_data_code', NcType.string, (), 'Meteorological data code', '-', 'RRD (Rain radar data)')),
                ('-', ('Manufacturer_model', NcType.string, (), 'Manufacturer and model', '-', 'METE (METEK)')),
                ('-', ('RRD_sens_HGT', NcType.float, (), 'Rain radar height', 'm', 1.5)),
                ('-', ('Service_version', NcType.string, (), 'Version number of the MRR Service (service version number)', '-', 'SVS: 6.0.0.6')),
                ('+', ('Device_version', NcType.string, (), 'Device version number (firmware)', '-', 'DVS: 6.00')),
                ('+', ('Devi_seri_numb', NcType.string, (), 'Device serial number', '-', 'DSN: 0505123820')),
                ('BW', ('Bandwidth', NcType.string, (), 'Bandwidth', '-', 'BW: 40200')),
                ('+', ('Calibration_constant', NcType.string, (), 'Calibration constant', '-', 'CC: 2279042')),
                ('+', ('MMR_data_qual', NcType.string, (), 'Micro Rain Radar Data quality', '-', 'MDQ: 100')),
            ],
            # 数据信息组
            "head_grp3": [
                ('+', ('Data_level', NcType.string, (), 'Data level', '-', 'Lraw')),
                ('-', ('Timezone', NcType.string, (), 'Timezone', '-', 'UTC+8')),
                ('-', ('Time_resolution', NcType.ubyte, (), 'Time resolution', 's', 10)),
                ('-', ('Obse_begi_DT', NcType.string, (), 'Observing beginning datetime', 'yyyy-mm-dd hh:mm:ss', '')),
                ('-', ('Obse_end_DT', NcType.string, (), 'Observing ending datetime', 'yyyy-mm-dd hh:mm:ss', '')),
                ('-', ('Data_crea_DT', NcType.string, (), 'Data creating datetime', 'yyyy-mm-dd hh:mm:ss', '')),
                ('-', ('Dataset_version', NcType.string, (), 'Dataset version', '-', '1.0')),
            ]
        },
    # (input_data_name, (name, nc_typ, dim, longname, units))
    "observation": 
        [
            ('Datetime', NcType.string, (Datetime, ), 'Datetime', 'yyyy-mm-dd hh:mm:ss'),
            ('HGT', NcType.ushort, (Datetime, Dime_HGT_32), 'Height in meters', 'm'),
            ('Transfer_function', NcType.double, (Datetime, Dime_HGT_32), 'Transfer function', '-'),
            ('Spectral_reflectivities', NcType.double, (Datetime, Dime_HGT_32, Dime_part_diam_clas), 'Spectral reflectivities', 'dB'),
            ('Q_data', NcType.ubyte, (Datetime, ), 'Quality control code of data', '-'),
        ],
    "name": ["RADA", "MODI", "MOBS", "SUOB", "WNFB", "", "RRD", "METE", "Lraw", "", "FMT", True],
}


