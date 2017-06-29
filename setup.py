from setuptools import setup

setup(name='tradier',
      version='0.1',
      description='Unofficial Tradier SDK',
      url='http://github.com/finnpy/tradier',
      author='Tom Paoletti',
      author_email='zommaso@gmail.com',
      license='MIT',
      packages=['tradier'],
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
