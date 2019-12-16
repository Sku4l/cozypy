import setuptools
from setuptools import setup

setup(
    name='cozytouchpy',
    version='1.3.0',
    packages=setuptools.find_packages(),
    url='https://github.com/cyr-ius/cozypy/tree/master',
    license='https://github.com/cyr-ius/cozypy/blob/master/LICENSE',
    author='Cyr-ius',
    author_email='cyr-ius@ipocus.net',
    description='Cozytouch python client',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    keywords=[
        'rest',
        'overkiz',
        'cozytouch',
        'atlantic',
        'thermor',
        'sauter',
        'io',
        'smart-things',
        'iot'
    ],
    install_requires=["requests"]
)
