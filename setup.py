import setuptools


with open('README.md', 'r') as readme_fp:
    long_description = readme_fp.read()


setuptools.setup(
    name='py_cui',
    description='A widget and grid based framework for building command line user interfaces in python.',
    long_description=long_description,
    version='0.0.1',
    author='Jakub Wlodek',
    author_email='jwlodek.dev@gmail.com',
    license='BSD (3-clause)',
    packages=['py_cui'],
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
    ],
    keywords='cui cli commandline user-interface ui',
    python_requires='>=3.2',
)
