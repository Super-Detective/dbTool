import csv
import argparse
import pymysql
from .config import DATABASE_CONFIG

def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def update_data(connection, table, filepath, unique_column):
    try:
        with connection.cursor() as cursor:
            # 打开 CSV 文件并读取数据
            with open(filepath, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                # 执行更新操作
                for row in csv_reader:
                    # 获取记录的 ID
                    record_id = row[unique_column]
                    
                    # 构建 SET 子句
                    set_clause = ', '.join([f"`{column}` = '{value}'" for column, value in row.items() if column != unique_column])
                    
                    # 构建 UPDATE 语句
                    sql_query = f"UPDATE `{table}` SET {set_clause} WHERE `{unique_column}` = '{record_id}';"
                    cursor.execute(sql_query)

            # 提交事务
            connection.commit()

        print(f"Data updated in `{table}` from {filepath} using `{unique_column}` as the identifier")

    except Exception as e:
        print(f"Error updating data: {e}")

def main():

    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Database Update Tool')

    # 添加命令行参数
    parser.add_argument('-database', type=str, help='Database name', required=True)
    parser.add_argument('-table', type=str, help='Table name', required=True)
    parser.add_argument('-filepath', type=str, help='Filepath with data to update', required=True)
    parser.add_argument('-unique_column', type=str, help='Column name for the identifier', required=True)

    # 解析命令行参数
    args = parser.parse_args()

    # 建立数据库连接
    connection = connect_to_database(args.database)

    if connection:
        # 更新数据
        update_data(connection, args.table, args.filepath, args.unique_column)

        # 关闭数据库连接
        connection.close()

if __name__ == "__main__":
    main()
