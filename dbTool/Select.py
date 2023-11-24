import argparse
import csv
import pymysql
from tabulate import tabulate
from .config import DATABASE_CONFIG

def connect_to_database(database_name):
    config = DATABASE_CONFIG.copy()
    config['database'] = database_name
    return pymysql.connect(**config)

def execute_query(connection, table, columns, limit, conditions):
    try:
        with connection.cursor() as cursor:
            column_list = ', '.join(columns)
            sql_query = f'SELECT {column_list} FROM {table}'
            if conditions:
                where_clause = ' AND '.join(conditions)
                sql_query += f' WHERE {where_clause}'
            if limit is not None:
                sql_query += f' LIMIT {limit}'

            sql_query += ';'

            cursor.execute(sql_query)

            result = cursor.fetchall()

            return result, cursor.description

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def display_result(result, headers):
    if result and headers:
        print(tabulate(result, headers=headers, tablefmt='grid'))

def save_to_csv(result, headers, filepath):
    try:
        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([header[0] for header in headers])
            csv_writer.writerows(result)
        print(f"Results saved to {filepath}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description='Database Query Tool')
    parser.add_argument('-database', type=str, help='Database name', required=True)
    parser.add_argument('-table', type=str, help='Table name', required=True)
    parser.add_argument('-columns', nargs='+', help='List of columns to query', default=None)
    parser.add_argument('-save', action='store_true', help='Save results to CSV')
    parser.add_argument('-filepath', type=str, help='Filepath to save CSV')
    parser.add_argument('-limit', type=int, help='Limit the number of rows to query')
    parser.add_argument('-conditions', nargs='+', help='Custom conditions for the WHERE clause')

    args = parser.parse_args()

    if not args.columns:
        args.columns = ['*']

    connection = connect_to_database(args.database)

    if connection:
        result, headers = execute_query(connection, args.table, args.columns, args.limit, args.conditions)

        display_result(result, headers)

        if args.save:
            save_to_csv(result, headers, args.filepath)

        connection.close()

if __name__ == "__main__":
    main()
