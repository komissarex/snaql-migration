# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='snaql-migration',
    version='0.1.2',
    author='Egor Komissarov',
    author_email='komissarex@gmail.com',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/komissarex/snaql-migration',
    description='Lightweight SQL schema migration tool, based on Snaql query builder',
    install_requires=[
        'click==6.6',
        'snaql==0.4',
        'PyYAML==5.1'
    ],
    entry_points={
        'console_scripts': [
            'snaql-migration=snaql_migration.snaql_migration:snaql_migration'  # ¯\_(ツ)_/¯
        ]
    }
)