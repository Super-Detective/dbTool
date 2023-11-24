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
            with open(filepath, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    record_id = row[unique_column]
                    set_clause = ', '.join([f"`{column}` = '{value}'" for column, value in row.items() if column != unique_column])
                    sql_query = f"UPDATE `{table}` SET {set_clause} WHERE `{unique_column}` = '{record_id}';"
                    cursor.execute(sql_query)
            connection.commit()

        print(f"Data updated in `{table}` from {filepath} using `{unique_column}` as the identifier")

    except Exception as e:
        print(f"Error updating data: {e}")

def main():
    parser = argparse.ArgumentParser(description='Database Update Tool')
    parser.add_argument('-database', type=str, help='Database name', required=True)
    parser.add_argument('-table', type=str, help='Table name', required=True)
    parser.add_argument('-filepath', type=str, help='Filepath with data to update', required=True)
    parser.add_argument('-unique_column', type=str, help='Column name for the identifier', required=True)

    args = parser.parse_args()

    connection = connect_to_database(args.database)

    if connection:
        update_data(connection, args.table, args.filepath, args.unique_column)

        connection.close()

if __name__ == "__main__":
    main()
