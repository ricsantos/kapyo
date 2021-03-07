from setuptools import setup

setup(
  name='kapyo',
  version='0.1',
  author='Ben Alexander',
  author_email='benphillipalexander@gmail.com',
  packages=['kapyo'],
  install_requires=[
    "requests",
    "datetime",
  ],
  description='Helper Package for Kayo Apis'
)