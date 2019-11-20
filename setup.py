import setuptools
from setuptools import setup

setup(
    name='cozypy',
    version='1.1.1',
    packages=setuptools.find_packages(),
    url='https://github.com/biker91620/cozypy/tree/master',
    license='https://github.com/biker91620/cozypy/blob/master/LICENSE',
    author='Snake',
    author_email='biker91620@gmail.com',
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
