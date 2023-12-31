import argparse
import pymysql
from tabulate import tabulate
from .config import DATABASE_CONFIG
from configparser import ConfigParser




def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def get_all_tables(connection):
    try:
        with connection.cursor() as cursor:
            # 获取所有表的查询
            sql_query = 'SHOW TABLES;'
            cursor.execute(sql_query)

            # 获取查询结果
            result = cursor.fetchall()

            return result

    except Exception as e:
        # 处理异常
        print(f"Error: {e}")
        return None

def display_tables(tables):
    if tables:
        print(tabulate(tables, headers=['Tables'], tablefmt='grid'))

# get_tables_script.py

def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Database Query Tool')

    # 添加命令行参数
    parser.add_argument('-database', type=str, help='Database name')

    # 解析命令行参数
    args = parser.parse_args()

    # 如果未提供数据库和表，使用默认值
    if not args.database:
        # 加载配置文件 config.ini
        config = ConfigParser()
        config.read('config.ini')
        
        # 从配置文件设置默认值
        DEFAULT_DATABASE = config.get('DEFAULT', 'DATABASE')
        args.database = DEFAULT_DATABASE

    # 建立数据库连接
    connection = connect_to_database(args.database)

    if connection:
        # 获取所有表
        tables = get_all_tables(connection)

        # 显示结果
        display_tables(tables)

        # 关闭数据库连接
        connection.close()

if __name__ == "__main__":
    main()
