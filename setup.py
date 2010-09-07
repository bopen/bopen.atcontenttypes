# -*- coding: utf-8 -*-
"""
This module contains the tool of bopen.atcontenttypes
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('bopen', 'atcontenttypes', 'README.txt')
)

tests_require = ['zope.testing']

setup(
    name='bopen.atcontenttypes',
    version=version,
    description="B-Open AT Content Types for Plone",
    long_description=long_description,
    classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
    keywords='',
    author='B-Open Solutions srl',
    author_email='',
    url='http://www.bopen.eu/open-source/bopen.atcontenttypes',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['bopen', 'bopen.atcontenttypes'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.i18nmessageid',
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite='bopen.atcontenttypes.tests.test_docs.test_suite',
    entry_points="""
    # -*- entry_points -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
    setup_requires=["PasteScript"],
    paster_plugins=["ZopeSkel"],
)
