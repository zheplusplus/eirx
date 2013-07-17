import os.path
from setuptools import setup, find_packages

def descr():
    with open('README.md') as f:
        return f.read()

setup(
        name='eirx',
        version='0.1',
        author='Neuron Teckid',
        author_email='lene13@gmail.com',
        license='MIT',
        keywords='image manipulate resize',
        url='https://github.com/neuront/eirx',
        description='Simple image manipulate based on PIL.',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        long_description=descr(),
        install_requires = [
                'PIL',
            ],
        zip_safe=False,
        entry_points=dict(
                console_scripts=[ 'eirx=eirx.main:main' ],
            ),
    )
