import setuptools
from setuptools import setup

setup(
    name='cozypy',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/biker91620/cozypy/tree/master',
    license='https://github.com/biker91620/cozypy/blob/master/LICENSE',
    author='Snake',
    author_email='biker91620@gmail.com',
    description='Cozytouch python client',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=["requests"]
)
