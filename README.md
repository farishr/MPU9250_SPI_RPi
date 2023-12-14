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
  getGValues()
  ```
  ### Get gyroscope values
  Gets the gyroscope values in angular velocity. Run the calibration function before this function to get the adjusted gyroscope values.
  ```bash
  getGyrValues()
  ```
  ### Get Temperature
  Gets the temperature readings from the sensor in degree celsius.
  ```bash
getTemperature()
```
### Set accelerometer range
Sets the following ranges in the accelerometer.
```bash
setAccRange(accelRange)
```
```bash
"""
accelRange : str
	The supported ranges are as following:
	2g: AccelRangeSelect2G
	4g: AccelRangeSelect4G
	8g: AccelRangeSelect8G
	16g: AccelRangeSelect16G
"""
```
### Set gyroscope range
```bash
setGyroRange(accelRange)
```
```bash
"""
gyroRange : str
	The supported ranges are as following ->
	250DPS: GyroRangeSelect250DPS
	500DPS: GyroRangeSelect500DPS
	1000DPS: GyroRangeSelect1000DPS
	2000DPS: GyroRangeSelect2000DPS
"""
```
### Enable Digital Low Pass Filter
```bash
# Accelerometer DLPF
enableAccDLPF()
setAccDLPF(level)

# Gyroscope DLPF
enableGyrDLPF()	
setGyrDLPF(level)
```
```bash
"""
Select from the 8 levels of Low Pass Filters
	1 > MPU9250_DLPF_0
	2 > MPU9250_DLPF_1
	3 > MPU9250_DLPF_2
	4 > MPU9250_DLPF_3
	5 > MPU9250_DLPF_4
	6 > MPU9250_DLPF_5
	7 > MPU9250_DLPF_6
	8 > MPU9250_DLPF_7
	
Check the Register map for more details. 
"""
```
