from setuptools import setup, find_packages

setup(
    name='dbTool',
    version='0.2',
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
    package_data={
        '': ['config.ini'],
    },
    include_package_data=True,
    author='Ming L',
    author_email='email@example.com',
    description='A set of tools for interacting with databases',
    long_description='This package provides command-line tools for various database operations.',
    url='https:https://github.com/Super-Detective/dbTool',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11.4',
    ],
    keywords='database tool sql pymysql',
)
