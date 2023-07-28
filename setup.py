from setuptools import setup, find_packages

setup(name='sbc-classification',
      version='0.0.3',
      description='Demand Patterns SBC (Syntetos, Boylan, Croston) method of Categorizations',
      author='Thu Nguyen',
      author_email='tqn1472@gmail.com',
      license='MIT License',
      long_description_content_type='text/markdown',
      long_description=open('README.md').read(),
      packages=find_packages(),
      install_requires=[
          'pandas >= 1.5.3',
          'numpy >= 1.24.4',
          'matplotlib >= 3.7.2'
      ],
      test_suite='tests',
      tests_require=['pytest'],

      package_data={'sbc-classification': [
          'tests/data_files/sales_train_clean.csv']},
      keywords=['python', 'demand patterns', 'sbc classification', 'croston', 'idclass', 'tsintermittent'],
      include_package_data=True,
      zip_safe=False)