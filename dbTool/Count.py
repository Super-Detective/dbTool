import argparse
import csv
import pymysql
from tabulate import tabulate
from .config import DATABASE_CONFIG
from configparser import ConfigParser

# 加载配置文件 config.ini
config = ConfigParser()
config.read('config.ini')

# 从配置文件设置默认值
DEFAULT_DATABASE = config.get('DEFAULT', 'DATABASE')
DEFAULT_TABLE = config.get('DEFAULT', 'TABLE')

def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def execute_query(connection, table, columns, limit, conditions):
    try:
        with connection.cursor() as cursor:
            # 构建查询语句
            column_list = ', '.join(columns)
            sql_query = f'SELECT {column_list} FROM {table}'
            
            # 添加 WHERE 子句
            if conditions:
                where_clause = ' AND '.join(conditions)
                sql_query += f' WHERE {where_clause}'
            
            # 添加 LIMIT 子句
            if limit is not None:
                sql_query += f' LIMIT {limit}'

            sql_query += ';'

            # 执行查询
            cursor.execute(sql_query)

            # 获取查询结果
            result = cursor.fetchall()

            return result, cursor.description

    except Exception as e:
        # 处理异常
        print(f"Error: {e}")
        return None, None

def count_records(connection, table, conditions):
    try:
        with connection.cursor() as cursor:
            # 构建查询语句
            sql_query = f'SELECT COUNT(*) FROM {table}'
            
            # 添加 WHERE 子句
            if conditions:
                where_clause = ' AND '.join(conditions)
                sql_query += f' WHERE {where_clause}'

            sql_query += ';'

            # 执行查询
            cursor.execute(sql_query)

            # 获取查询结果
            result = cursor.fetchone()

            return result[0]  # 返回记录数量

    except Exception as e:
        # 处理异常
        print(f"Error: {e}")
        return None

def display_result(result, headers):
    if result and headers:
        print(tabulate(result, headers=headers, tablefmt='grid'))



def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Database Query Tool')

    # 添加命令行参数
    parser.add_argument('-database', type=str, help='Database name')
    parser.add_argument('-table', type=str, help='Table name')
    parser.add_argument('-columns', nargs='+', help='List of columns to query', default=None)
    parser.add_argument('-limit', type=int, help='Limit the number of rows to query')
    parser.add_argument('-conditions', nargs='+', help='Custom conditions for the WHERE clause')
    parser.add_argument('-show', action='store_true', help='Count records matching the conditions')

    # 解析命令行参数
    args = parser.parse_args()

        # 如果未提供数据库和表，使用默认值
    if not args.database:
        args.database = DEFAULT_DATABASE
    if not args.table:
        args.table = DEFAULT_TABLE

    # 如果未提供列名，默认为所有列（SELECT *）
    if not args.columns:
        args.columns = ['*']

    # 建立数据库连接
    connection = connect_to_database(args.database)

    if connection:
        # 如果指定统计记录数量
        if args.show:
            # 执行查询
            result, headers = execute_query(connection, args.table, args.columns, args.limit, args.conditions)

            # 显示结果
            display_result(result, headers)
        else:
            record_count = count_records(connection, args.table, args.conditions)
            print(f"Number of records matching the conditions: {record_count}")

        # 关闭数据库连接
        connection.close()

if __name__ == "__main__":
    main()
