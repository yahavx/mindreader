from setuptools import setup, find_packages


setup(
    name='YahavFooBar',
    version='1.0.1',
    author='Yahav Ben Yaakov',
    description='A brain computer interace.',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov'],
)
