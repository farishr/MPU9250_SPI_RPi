from setuptools import find_packages, setup
setup(
    name='mpu9250_spi',
    packages=find_packages(include=['mpu9250_spi']),
    version='0.1.0',
    description='Interfacing MPU9250 IMU Sensor with RPi using SPI',
    author='Farish Reheman',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
