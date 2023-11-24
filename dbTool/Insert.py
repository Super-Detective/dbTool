import csv
import argparse
import pymysql
from config import DATABASE_CONFIG

def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def record_exists(cursor, table, unique_column, value):
    sql_query = f'SELECT * FROM {table} WHERE `{unique_column}` = "{value}";'
    cursor.execute(sql_query)
    return cursor.fetchone() is not None

def insert_data(connection, table, filepath, unique_column):
    try:
        with connection.cursor() as cursor:
            with open(filepath, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  
                if unique_column not in header:
                    print(f"Error: The specified unique column '{unique_column}' does not exist in the CSV file.")
                    return

                for row in csv_reader:
                    unique_value = row[header.index(unique_column)]
                    if not record_exists(cursor, table, unique_column, unique_value):
                        columns = [f'`{col}`' for col in header]
                        values = [f'"{value}"' for value in row]
                        sql_query = f'INSERT INTO {table} ({", ".join(columns)}) VALUES ({", ".join(values)});'
                        cursor.execute(sql_query)
                    # else:
                    #     print(f"Record with '{unique_column}' value '{unique_value}' already exists. Skipping insertion.")
            connection.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")

def main():
    parser = argparse.ArgumentParser(description='Database Insert Tool')
    parser.add_argument('-database', type=str, help='Database name', required=True)
    parser.add_argument('-table', type=str, help='Table name', required=True)
    parser.add_argument('-filepath', type=str, help='Filepath with data to insert', required=True)
    parser.add_argument('-unique_column', type=str, help='Column used for uniqueness constraint', required=True)
    args = parser.parse_args()
    connection = connect_to_database(args.database)
    if connection:
        insert_data(connection, args.table, args.filepath, args.unique_column)
        connection.close()
if __name__ == "__main__":
    main()
