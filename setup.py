from setuptools import setup, find_packages


setup(
    name='mindreader',
    version='1.0.1',
    author='Yahav Ben Yaakov',
    description='A brain computer interface.',
    packages=find_packages(),
    install_requires=['click', 'flask'],
    tests_require=['pytest', 'pytest-cov'],
)
