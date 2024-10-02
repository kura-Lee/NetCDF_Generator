import json
import pandas as pd
from typing import IO

import chardet  


class BaseParser(object):
    def __init__(self) -> None:
        self.datas = []
        
    def parse(self):
        raise NotImplementedError
    
    
    def save2csv(self, file_name):
        pd.DataFrame(self.datas).to_csv(file_name, index=False)
    
    def save2json(self, file_name):
        with open(file_name, 'w') as fp:
            json.dump(self.datas, fp, indent=4, ensure_ascii=False)



class BaseTxtParser(BaseParser):
    def __init__(self, file: str, mode: str='r', encoding: str='utf8') -> None:
        """文本文件类解析器

        Args:
            file (str): 文件名
            mode (str, optional): 打开文件的模式. Defaults to 'r'.
            encoding (str, optional): 文件的编码，若传入空字符串，会使用chardet自动检测文件编码. Defaults to 'utf8'.
        """
        super().__init__()
        self.fp = BaseTxtParser.openfile(file, mode, encoding)
    
    @staticmethod
    def encoding_detect(file: str, detect_size: int=4096) -> str:
        with open(file, 'rb') as f:
            raw_data = f.read(detect_size)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            return encoding

    @staticmethod
    def openfile(file: str, mode: str, encoding: str) -> IO:
        if encoding == "":
            encoding = BaseTxtParser.encoding_detect(file)
        return open(file, mode, encoding=encoding)
  
    def parse(self):
        """操作打开的文件指针self.fp,解析数据到self.datas中,并返回self.datas

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError
    
    def __del__(self):
        if self.fp:  
            self.fp.close()  
        return False


class BaseCsvParser(BaseParser):
    def __init__(self, file: str) -> None:
        """CSV类文件解析器

        Args:
            file (str): 要解析的文件
        """
        super().__init__()
        self.file = file

    def parse(self):
        """操作文件self.file,解析数据到self.datas中,并返回self.datas

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError