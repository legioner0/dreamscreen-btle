import sys
sys.path.insert(0, 'src')
from dsbtle import __version__

from setuptools import setup
setup(
    name='dsbtle',
    version=__version__,
    description='DreamScreen interface via BLE',
    url='https://github.com/legioner0/dreamscreen-btle',
    author='Pavel Motyrev',
    author_email='legioner.r@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'Topic :: Internet',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
    ],
    keywords=['DreamScreen', 'BLE', 'Bluetooth Low Energy'],
    package_dir={'': 'src'},
    packages=['dsbtle'],
    install_requires=['bluepy', 'parse'],
)
