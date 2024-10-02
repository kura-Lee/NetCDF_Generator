'''
Author: Zhong Xiao Wei 56347761+kura-Lee@users.noreply.github.com
Date: 2023-11-26 09:55:02
LastEditTime: 2024-10-02 22:30:58
FilePath: /Dataset_build/parse/__init__.py
Description: 

Copyright (c) 2023 by Zhongxiaowei, All Rights Reserved. 
'''
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Callable
from tqdm import tqdm
from logging import getLogger

from . import BaseParser
from . import station_data


logger = getLogger(os.path.basename(__file__))
__all__ = ['station_data', 'BaseParser']



class FileProcessor:  
    def __init__(self, parser_class: BaseParser, num_workers=4):  
        self.num_workers = num_workers
        self.parser_class = parser_class
        self.result = []

    def filter_files(self, file_paths, filter_func: Callable=lambda x: x):
        """根据文件名过滤文件， 默认不过滤文件"""
        return filter(filter_func, file_paths)
    
    def process_files(self, file_paths):  
        """使用进程池处理文件""" 
        self.result.clear()
        filtered_files = self.filter_files(file_paths)   
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:  
            futures = [executor.submit(self.process_file, file) for file in filtered_files]  
            for future in tqdm(futures):
                try:
                    result = future.result()
                except Exception as exc:
                    print(f"Error processing {future.file_path}: {exc}")
        return self.result

    def process_file(self, file_path, *args, **kwargs):  
        """处理单个文件"""
        parser = self.parser_class(file_path, *args, **kwargs)  
        result = parser.parse(file_path)
        self.result.extend(result)
        return result
  
    def process_directory(self, directory):  
        """处理整个目录"""
        self.result.clear()
        file_paths = [str(p) for p in Path(directory).rglob('*') if p.is_file()]  
        return self.process_files(file_paths)

    @staticmethod
    def find_files_in_folder(folder_path, prefix, identifier, suffix):
        """
        在指定文件夹下查找所有以指定前缀、包含指定标识符、以指定后缀命名的文件

        Args:
            folder_path (str): 文件夹路径
            prefix (str): 文件名前缀
            identifier (str): 唯一标识符
            suffix (str): 文件名后缀

        Returns:
            List[str]: 匹配的文件路径列表
        """
        matching_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.startswith(prefix) and identifier in file and file.endswith(suffix):
                    matching_files.append(os.path.join(root, file))
        return matching_files
  
  
  
# 使用示例  
if __name__ == "__main__":  
    processor = FileProcessor(BaseParser, num_workers=2)  
    processor.process_directory("/path/to/your/directory")