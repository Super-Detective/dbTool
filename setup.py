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
            'Select = my-database-tool.Select:main',
            'Table = my-database-tool.Table:main',
            'Database = my-database-tool.Database:main',
        ],
    },
)
