# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='cron-rest',
    version='1.0.0',
    description='A simple Cron REST API',
    url='https://github.com/eug/cron-rest',
    author='Eugenio Cabral',
    author_email='eugfcl@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='cron schedule rest',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['Flask', 'python-crontab','pretty-cron'])