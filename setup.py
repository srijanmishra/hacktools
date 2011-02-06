'''
Buzzackup, Google Buzz feed backup utility and static feed webpage generator.
Written by Rohit Yadav.
'''

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

name = 'buzzackup'
version = '1.0'

setup(
    name=name,
    version=version,
    description='Buzzackup, Google Buzz feed backup utility and static feed webpage generator',
    long_description=__doc__,
    keywords='google buzz feed backup',
    license='BSD',
    author='Rohit Yadav',
    author_email='rohityadav89@gmail.com',
    url='http://code.google.com/p/vmcontroller',
    packages=find_packages(exclude=['ez_setup', 'distribute_setup', 'tests', 'tests.*']),
    package_data={'buzzackup': ['*.cfg*', 'tests/resources/*']},
    namespace_packages=['buzzackup'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'distribute',
        'setuptools',
        'urllib2',
        'xml',
        'ConfigParser',
        'optparse',
        'django.utils',
        'calendar',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points="""
    [console_scripts]
    buzzackup = buzzackup
    """,
)
