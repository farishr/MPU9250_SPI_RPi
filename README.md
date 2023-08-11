# mpu-spi-lib
This python package interfaces the MPU9250 (9-Axis (Gyro + Accelerometer + Compass) MEMS MotionTracking Device) with the Raspberry Pi using the SPI interface. Package includes functions for data extraction from sensors (Accelerometer, Gyroscope, Temperature), calibration, range setting for sensors and inbuilt Low Pass Filters. This repository will be updated constantly with moer functions, better functionalities, test results etc. This is an experimental and learning project for me.

## In this README:

- [Features](#features)
- [Usage](#usage)
  - [Initial setup](#initial-setup)
  - [Creating releases](#creating-releases)
- [Projects using this template](#projects-using-this-template)
- [FAQ](#faq)
- [Contributing](#contributing)

## Features
1. Extraction of raw data directly from registers, sensors values in standard units and calibrated sensor values.
2. Set multiple data ranges on the sensors for each application it is used.
3. Apply various inbuilt LPFs on the sensors for filtering out noise and getting cleaner data. 
