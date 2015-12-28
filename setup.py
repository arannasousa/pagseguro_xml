#!/usr/bin/env python
#  coding=utf-8
# ---------------------------------------------------------------
# Desenvolvedor:    Arannã Sousa Santos
# Mês:              12
# Ano:              2015
# Projeto:          pagseguro_xml
# e-mail:           asousas@live.com
# ---------------------------------------------------------------

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
requirements = ['requests', 'pytz', 'lxml']

setup(
    name='pagseguro_xml',
    version='0.0.1.dev0',
    description='Pagseguro API v2 e v3',
    author='Aranna Sousa Santos',
    author_email='asousas@live.com',
    url='https://github.com/arannasousa/pagseguro_xml',
    packages=[
        'pagseguro_xml',
    ],
    package_dir={'pagseguro_xml': 'pagseguro_xml'},
    install_requires=requirements,
    license='GNU GENERAL PUBLIC LICENSE',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: Portuguese BR',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    keywords='pagseguro, payment, payments, credit-card, pagseguro_xml, xml, transacao, assinatura')