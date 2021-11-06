from setuptools import setup

setup(
  name='kapyo',
  version='0.2',
  author='Ben Alexander',
  author_email='benphillipalexander@gmail.com',
  packages=['kapyo'],
  install_requires=[
    "requests",
  ],
  extras_requires={
    "dev": [
      "pytest",
      "pytest-cov",
      "pytest-mock"
    ]
  },
  description='Helper Package for Kayo Apis'
)