from setuptools import setup

setup(
    name='pchyme',
    version='0.1',
    packages=['pchyme'],
    package_data={'pchyme': ['english.txt', 'sounds/*.wav']},
    install_requires=['pydub >=0.14.1'],
    entry_points={'console_scripts': ['pchyme = pchyme.__main__:main']},
)
