import sys
from setuptools import setup, find_packages

install_requires=[]

try:
    with open('requirements.txt') as f:
        deps = [dep for dep in f.read().split('\n') if dep.strip() != ''
                and not dep.startswith('-e')]
        install_requires = deps
except Exception as e:
    print(e)

setup(name='auth',
      version="0.1",
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires)
