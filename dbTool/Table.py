import argparse
import pymysql
from tabulate import tabulate
from .config import DATABASE_CONFIG

def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def get_all_tables(connection):
    try:
        with connection.cursor() as cursor:
            sql_query = 'SHOW TABLES;'
            cursor.execute(sql_query)

            result = cursor.fetchall()

            return result

    except Exception as e:
        print(f"Error: {e}")
        return None

def display_tables(tables):
    if tables:
        print(tabulate(tables, headers=['Tables'], tablefmt='grid'))

# get_tables_script.py

def main():
    parser = argparse.ArgumentParser(description='Database Query Tool')

    parser.add_argument('-database', type=str, help='Database name', required=True)

    args = parser.parse_args()

    connection = connect_to_database(args.database)

    if connection:
        tables = get_all_tables(connection)

        display_tables(tables)

        connection.close()

if __name__ == "__main__":
    main()
