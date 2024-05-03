# 导入sqlite3和pandas，pandas用于处理数据，简化代码
import pandas as pd
import sqlite3

# 先创建一个数据连接
# 如果数据库文件不存在，会自动在当前的目录创建
conn = sqlite3.connect("citycode.db")
# 获取数据，读取当前目录下的CSV文件
df = pd.read_csv('China-City-List-latest.csv', sep=',')
# 使用pandas的to_sql函数把数据导入到sqlite3中
df.to_sql('areas', conn, if_exists='append', index=False)
# 最后记得关闭连接
conn.close()

