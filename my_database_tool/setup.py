from setuptools import setup, find_packages

setup(
    name='my_database_tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'query_script = my_database_tool.Select:main',
            'get_tables_script = my_database_tool.Table:main',
            'get_databases_script = my_database_tool.Database:main',
        ],
    },
)
