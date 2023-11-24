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
            sql_query = 'SHOW DATABASES;'
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error: {e}")
        return None

def display_databases(databases):
    if databases:
        print(tabulate(databases, headers=['Databases'], tablefmt='grid'))

def main():
    parser = argparse.ArgumentParser(description='Database Query Tool')
    args = parser.parse_args()
    connection = connect_to_database()
    if connection:
        databases = get_all_databases(connection)
        display_databases(databases)
        connection.close()

if __name__ == "__main__":
    main()
