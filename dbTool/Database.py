import argparse
import pymysql
from tabulate import tabulate
from .config import DATABASE_CONFIG

def connect_to_database(database_name=None):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def get_all_databases(connection):
    try:
        with connection.cursor() as cursor:
            # 获取所有数据库的查询
            sql_query = 'SHOW DATABASES;'
            cursor.execute(sql_query)

            # 获取查询结果
            result = cursor.fetchall()

            return result

    except Exception as e:
        # 处理异常
        print(f"Error: {e}")
        return None

def display_databases(databases):
    if databases:
        print(tabulate(databases, headers=['Databases'], tablefmt='grid'))

def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Database Query Tool')

    # 解析命令行参数
    args = parser.parse_args()

    # 建立数据库连接
    connection = connect_to_database()

    if connection:
        # 获取所有数据库
        databases = get_all_databases(connection)

        # 显示结果
        display_databases(databases)

        # 关闭数据库连接
        connection.close()

if __name__ == "__main__":
    main()
