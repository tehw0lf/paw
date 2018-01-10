from setuptools import setup

setup(name='paw',
      version='1.1',
      description='paw - patterns and wordlists in python',
      url='https://github.com/tehw0lf/paw',
      author='tehw0lf',
      author_email='tehwolf@protonmail.com',
      license='MIT',
      packages=['paw'],
      zip_safe=False,
      entry_points={
            'console_scripts': ['paw=paw.command_line:main'],
      }
      )
