from setuptools import setup


setup(
    name='ceilometer-riemann',
    version='0.2.3',
    author='Brian Cline',
    author_email='bcline@softlayer.com',
    description=('Riemann publisher driver for OpenStack Ceilometer'),
    long_description=open('README.md').read(),
    license='Apache License v2.0',
    keywords='ceilometer riemann metrics instrumentation '
             'stats log processing',
    url='https://github.com/briancline/ceilometer-riemann',
    packages=['ceilometer_riemann'],
    install_requires=['bernhard'],
    entry_points={
        'ceilometer.publisher': [
            'riemann = ceilometer_riemann:RiemannPublisher'
        ]
    },
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
