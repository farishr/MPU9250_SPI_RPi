# mpu-spi-lib
This python package interfaces the MPU9250 (9-Axis (Gyro + Accelerometer + Compass) MEMS MotionTracking Device) with the Raspberry Pi using the SPI interface. Package includes functions for data extraction from sensors (Accelerometer, Gyroscope, Temperature), calibration, range setting for sensors and inbuilt Low Pass Filters. This repository will be updated constantly with more functions, better functionalities, test results etc. This is an experimental and learning project for me.

## In this README:

- [Features](#features)
- [Wiring](#wiring)
  - [Initial setup](#initial-setup)
  - [Creating releases](#creating-releases)
- [Projects using this template](#projects-using-this-template)
- [FAQ](#faq)
- [Contributing](#contributing)

## Features
**Version: v1**
- Extraction of raw data directly from registers, sensors values in standard units and calibrated sensor values.
- Set multiple data ranges on the sensors for each application it is used.
- Apply various inbuilt LPFs on the sensors for filtering out noise and getting cleaner data.

## Wiring
MPU9250 is interfaced to the Raspberry Pi using the SPI interface. This can be acheived by using the following wiring scheme:
| RPi | MPU9250 |
|--------|-------|
| Pin 1 | Vcc |
| Pin 6 | GND |
| Pin 23 | SCL |
| Pin 19 | SDA |
| Pin 21 | AD0 |
| Pin 24 | NCS |
| Pin 6 | FSYNC |

## Software Setup
1. Ensure that SPI has been enabled in your Raspberry Pi. Follow this [link](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/) to setup SPI in your RPi.
2. Install **spidev**
   ```bash
   sudo pip install spidev
   ```
3. Install **spidev**
   ```bash
   sudo pip install numpy
   ```
## Functions
  ### Get raw accelerometer value
  Gets the raw accelerometer data in the unsigned int16 format.
   ```bash
   getRawAccValues()
   ```
  ### Get raw gyroscope value
  Gets the raw gyroscope data in the unsigned int16 format.
  ```bash
   getRawGyrValues()
   ```
  ### Get G values
  Gets the accelerometer values in 'g'. Run the calibration function before this function to get the adjusted g values.
  ```bash
  getGValues
  ```
