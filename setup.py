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
            'Select = my_database_tool.Select:main',
            'Table = my_database_tool.Table:main',
            'Database = my_database_tool.Database:main',
        ],
    },
)