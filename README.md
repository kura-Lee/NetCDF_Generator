# netCDF文件生成器

根据指定的配置文件格式, 生成相应格式的nc文件, 理论上支持无限嵌套的结构.


**主要模块**

* dbcontroller: mongodb数据库驱动
* generate: 主要的nc文件生成核心
    * config: 基础数据类定义,建议将配置定义到此
* log: 日志记录
* parse: 基础解析器,需要针对具体文件实现parse方法