from setuptools import setup


setup(
    name='ceilometer-riemann',
    version='0.1.1-dev',
    author='Brian Cline',
    author_email='bcline@softlayer.com',
    description=('Riemann publisher driver for OpenStack Ceilometer'),
    license='Apache License v2.0',
    keywords='ceilometer riemann metrics instrumentation '
             'stats log text processing',
    url='http://packages.python.org/ceilometer-riemann',
    packages=['ceilometer-riemann', 'tests'],
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: OpenStack',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Monitoring',
    ],
)
