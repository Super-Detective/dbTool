import argparse
import csv
import pymysql
from tabulate import tabulate
from config import DATABASE_CONFIG

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

def display_result(result, headers):
    if result and headers:
        print(tabulate(result, headers=headers, tablefmt='grid'))

def save_to_csv(result, headers, filepath):
    try:
        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # 写入表头
            csv_writer.writerow([header[0] for header in headers])
            
            # 写入数据
            csv_writer.writerows(result)

        print(f"Results saved to {filepath}")

    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Database Query Tool')

    # 添加命令行参数
    parser.add_argument('-database', type=str, help='Database name', required=True)
    parser.add_argument('-table', type=str, help='Table name', required=True)
    parser.add_argument('-columns', nargs='+', help='List of columns to query', default=None)
    parser.add_argument('-save', action='store_true', help='Save results to CSV')
    parser.add_argument('-filepath', type=str, help='Filepath to save CSV')
    parser.add_argument('-limit', type=int, help='Limit the number of rows to query')
    parser.add_argument('-conditions', nargs='+', help='Custom conditions for the WHERE clause')

    # 解析命令行参数
    args = parser.parse_args()

    # 如果未提供列名，默认为所有列（SELECT *）
    if not args.columns:
        args.columns = ['*']

    # 建立数据库连接
    connection = connect_to_database(args.database)

    if connection:
        # 执行查询
        result, headers = execute_query(connection, args.table, args.columns, args.limit, args.conditions)

        # 显示结果
        display_result(result, headers)

        # 如果指定保存到 CSV 文件
        if args.save:
            save_to_csv(result, headers, args.filepath)

        # 关闭数据库连接
        connection.close()

if __name__ == "__main__":
    main()
