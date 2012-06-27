import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


requires = [
    'paramiko'
    ]

setup(name='SuperParamiko',
      version='0.1.0',
      description='Wrapper around paramiko adding pbs style functionality',
      long_description=README,
      license="AGPLv3+",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ],
      author='Ross Delinger',
      author_email='rossdylan@csh.rit.edu',
      url='http://github.com/rossdylan/SuperParamiko',
      keywords='ssh paramiko',
      packages=['SuperParamiko',],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )

