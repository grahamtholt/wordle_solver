from setuptools import setup

setup(
    name='wordler',
    version='0.1',
    description='Greedy, maximum-entropy solver for the Wordle',
    author='Graham Holt',
    author_email='graham.t.holt@gmail.com',
    packages=['wordler'],
    install_requires=['numpy',
                      'pandas',
                      'numba',
                      'fastparquet',
                      'pyarrow'
                      ],
)
