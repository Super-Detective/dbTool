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
            'Insert = dbTool.Insert:main',
            'Update = dbTool.Update:main',
            'Count = dbTool.Count:main',
        ],
    },
    author='Ming',
    author_email='email@example.com',
    description='A set of tools for interacting with databases',
    long_description='This package provides command-line tools for various database operations.',
    url='https://github.com/chengxuyuanlm/dbTool',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='database tool sql pymysql',
)
