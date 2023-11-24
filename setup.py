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
            'db select = dbTool.Select:main',
            'db table = dbTool.Table:main',
            'db database = dbTool.Database:main',
            'db insert = dbTool.Insert:main',
            'db update = dbTool.Update:main',
        ],
    },
)
