from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='nubank.authorizer',
      version='0.1',
      description='transcation-authorizer processor',
      long_description='',
      author='Asutosh Parida',
      author_email='ast.jva@gmail.com',
      entry_points = {
              'console_scripts': [
                  'authorizer = authorizer.authorize:main',
              ],
          },
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux'
      ],
      packages=find_packages(),
      install_requires=[
          'importlib',
          'datetime',
          'json5',
          'logging',
          'yaml-1.3'
      ],
      dependency_links=[],
      package_data = {'':['*.yaml']},
      setup_requires=['pytest-runner'],
      tests_require=['mock', 'pytest'],
      zip_safe=False)
