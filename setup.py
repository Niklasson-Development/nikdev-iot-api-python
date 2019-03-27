# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='nikdev_iot',
      version='0.3',
      description='Python API for NikDev IoT server.',
      url='https://github.com/Niklasson-Development/nikdev_iot_python',
      author='Johan Niklasson',
      author_email='johan@nik-dev.se',
      license='MIT',
      packages=['nikdev_iot'],
      install_requires=[
          'requests>=2.19,<3',
      ],
      zip_safe=False)
