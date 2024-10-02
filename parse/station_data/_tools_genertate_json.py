import json


def convert_station_json(string, output_file):
    # 分割成行
    lines = data.split('\n')
    # 每行生成一个dict
    stations = {}
    for line in lines:
        items = line.split()
        if len(items) > 1:
            station = {
            "station_name": items[0],
            "station_id": items[1], 
            "latitude": items[2],
            "longitude": items[3],
            "altitude": items[4], 
            "station_type": items[5],
            "station_level": items[6]    
            }
            stations[items[1]] = station
            
    # 生成json
    with open(output_file, 'w') as fp:
        json.dump(stations, fp, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    data = """
观风海	R7223	104.0	26.98	2233	40	15
河边	R7261	103.92	26.78	2321	40	15
哈喇河	R7225	103.99	26.82	2005	40	15
雪山	R7237	104.09	27.059	2509	40	15
松山	R7252	104.13	27.03	2196	40	15
秀水	R7263	103.94	26.91	2200	40	15
上关口	R7247	103.79	26.93	2129	40	15
双龙	R7236	104.14	26.9	2246	40	15
县局	56691	104.28	26.86	2234	0	11"""
    convert_station_json(data, "data.json")