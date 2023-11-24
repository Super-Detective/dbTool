from setuptools import setup, find_packages

setup(
    name='dbTool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'Select = dbTool.Select:main',
            'Table = dbTool.Table:main',
            'Database = dbTool.Database:main',
        ],
    },
)
