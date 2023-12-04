import csv
import argparse
import pymysql
from .config import DATABASE_CONFIG
from configparser import ConfigParser



def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def record_exists(cursor, table, unique_column, value):
    # 构建 SQL 查询语句
    sql_query = f'SELECT * FROM {table} WHERE `{unique_column}` = "{value}";'

    # 执行查询
    cursor.execute(sql_query)

    # 返回是否存在记录
    return cursor.fetchone() is not None

def insert_data(connection, table, filepath, unique_column):
    try:
        with connection.cursor() as cursor:
            # 打开 CSV 文件并读取数据
            with open(filepath, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # 获取表头

                # 判断是否指定了唯一性约束的列
                if unique_column not in header:
                    print(f"Error: The specified unique column '{unique_column}' does not exist in the CSV file.")
                    return

                # 执行插入操作
                for row in csv_reader:
                    # 获取唯一性约束列的值
                    unique_value = row[header.index(unique_column)]

                    # 判断记录是否已存在
                    if not record_exists(cursor, table, unique_column, unique_value):
                        # 构建列和值的字符串
                        columns = [f'`{col}`' for col in header]
                        values = [f'"{value}"' for value in row]

                        # 执行插入操作
                        sql_query = f'INSERT INTO {table} ({", ".join(columns)}) VALUES ({", ".join(values)});'
                        print(sql_query)
                        cursor.execute(sql_query)
                    # else:
                    #     print(f"Record with '{unique_column}' value '{unique_value}' already exists. Skipping insertion.")

            # 提交事务
            connection.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")

def main():

    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Database Insert Tool')

    # 添加命令行参数
    parser.add_argument('-database', type=str, help='Database name')
    parser.add_argument('-table', type=str, help='Table name')
    parser.add_argument('-filepath', type=str, help='Filepath with data to insert', required=True)
    parser.add_argument('-unique_column', type=str, help='Column used for uniqueness constraint', required=True)

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
    if not args.table:
        # 加载配置文件 config.ini
        config = ConfigParser()
        config.read('config.ini')
        # 从配置文件设置默认值
        DEFAULT_TABLE = config.get('DEFAULT', 'TABLE')
        args.table = DEFAULT_TABLE

    # 建立数据库连接
    connection = connect_to_database(args.database)

    if connection:
        # 插入数据
        insert_data(connection, args.table, args.filepath, args.unique_column)

        # 关闭数据库连接
        connection.close()

if __name__ == "__main__":
    main()
