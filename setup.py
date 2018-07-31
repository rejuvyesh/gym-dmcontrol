from setuptools import setup
from setuptools import find_packages

setup(
    name='gym_dmcontrol',
    version='0.0.3',
    author='rejuvyesh',
    description=('Simple wrapper for DeepMind control suite'),
    license="Apache License, Version 2.0",
    keywords="openai gym deepmind wrapper",
    packages=find_packages(),
    install_requires=['gym', 'dm_control'],)
