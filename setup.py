import setuptools
from sys import platform


# Use README for long description
with open('README.md', 'r') as readme_fp:
    long_description = readme_fp.read()

with open('requirements.txt', 'r') as req_fp:
    required_libs = req_fp.readlines()


# py_cui setup
setuptools.setup(
    name='py_cui',
    description='A widget and grid based framework for building command line user interfaces in python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.2',
    author='Jakub Wlodek',
    author_email='jwlodek.dev@gmail.com',
    license='BSD (3-clause)',
    packages=setuptools.find_packages(exclude=['docs','tests', 'examples', 'venv']),
    install_requires=required_libs,
    url='https://github.com/jwlodek/py_cui',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='cui cli commandline user-interface ui',
    python_requires='>=3.2',
)
