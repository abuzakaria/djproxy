from codecs import open
from setuptools import setup, find_packages

from djproxy import __author__, __doc__, __version__

install_requires = ['requests>=1.0.0', 'six>=1.9.0', 'tld']
tests_require = [
    'mock==1.3.0', 'nose==1.3.7', 'unittest2==1.1.0', 'spec==1.3.1',
    'requests>=1.0.0']


with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name="djproxy",
    version=__version__,
    url='https://github.com/thomasw/djproxy',
    author=__author__,
    author_email='thomas.welfley+djproxy@gmail.com',
    description=__doc__.strip().split('\n')[0],
    long_description=readme,
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite='nose.collector'
)
