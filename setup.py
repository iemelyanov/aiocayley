import os
import re
import sys
from setuptools import setup, find_packages


install_requires = ['aiohttp>=0.9.1']

PY_VER = sys.version_info

if PY_VER >= (3, 4):
    pass
elif PY_VER >= (3, 3):
    install_requires.append('asyncio')
else:
    raise RuntimeError("aiocayley doesn't suppport Python earllier than 3.3")


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'aiocayley', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in aiocayley/__init__.py')

classifiers = [
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Environment :: Web Environment',
    'Development Status :: 4 - Alpha',
    'Topic :: Database',
    'Topic :: Database :: Front-Ends',
]


setup(name='aiocayley',
      version=read_version(),
      description=('Cayley integration with asyncio.'),
      long_description='',
      classifiers=classifiers,
      platforms=['POSIX'],
      author='Igor Emelyanov',
      author_email='iiemelyanov@gmail.com',
      url='',
      download_url='',
      license='BSD',
      packages=find_packages(),
      install_requires=install_requires,
      include_package_data=True)