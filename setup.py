from setuptools import _install_setup_requires, setup, find_packages

with open('requirements.txt') as file:
    content = file.readlines()
    requirements = [x.strip() for x in content]

setup(
    name='api_final_prod_pkg',
    version='0.0.1',
    packages=find_packages(
        where='api_final_prod',
        include=['*pkg*'],
    ),
    scripts=['scripts/'],
    requirements=requirements
)