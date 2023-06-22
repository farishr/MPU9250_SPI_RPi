import spidev
import time
import csv
import numpy as np

# REGISTERS
REGISTER_INT_PIN_CFG            = 0x37
REGISTER_VALUE_BYPASS_EN        = 0x02

REGISTER_PWR_MGMT_1             = 0x6B
REGISTER_VALUE_RESET            = 0x80

REGISTER_ACCEL_CONFIG           = 0x1C
REGISTER_ACCEL_OUT              = 0x3B

# ACCEL_XOUT_H = 0x3B
# ACCEL_XOUT_L = 0x3C
# ACCEL_YOUT_H = 0x3D
# ACCEL_YOUT_L = 0x3E
# ACCEL_ZOUT_H = 0x3F
# ACCEL_ZOUT_L = 0x40

# GYRO_XOUT_H = 0x43
# GYRO_XOUT_L = 0x44
# GYRO_YOUT_H = 0x45
# GYRO_YOUT_L = 0x46
# GYRO_ZOUT_H = 0x47
# GYRO_ZOUT_L = 0x48
ACC_REG = [0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40]
GYRO_REG = [0x43, 0x44, 0x45, 0x46, 0x47, 0x48]

# VARIABLES

AxRaw, AyRaw, AzRaw, GxRaw, GyRaw, GzRaw = [],[],[],[],[],[]
AccRawData = []
GyrRawData = []
i = 0

accRangeFactor = 1
gyrRangeFactor = 1

lastMicros = 0
MAX_SAMPLING_FREQ = 20000		# Sampling Frequecy
MINIMUM_SAMPLING_DELAY_uSec = 1000*1000*1000/MAX_SAMPLING_FREQ

# SPI SETUP
spi = spidev.SpiDev()
spi.open(0 , 0)
spi.max_speed_hz = 1*1000000

# FUNCTIONS

def writeMPU9250Register(addr, val):
	spi.xfer([addr,val])	# [<Address to be Written to>, <Value to be written to the Address>]
	time.sleep(0.1)


def get_data(samples):
	i = 0
	while i < samples:
		# ~ rawData = spi.xfer([ACC_REG[0], ACC_REG[1], ACC_REG[2], ACC_REG[3], ACC_REG[4], ACC_REG[5], GYRO_REG[0], GYRO_REG[1], GYRO_REG[2], GYRO_REG[3], GYRO_REG[4], GYRO_REG[5]])
		AccRawData = spi.xfer([ACC_REG[0], ACC_REG[1], ACC_REG[2], ACC_REG[3], ACC_REG[4], ACC_REG[5]])
		GyrRawData = spi.xfer([GYRO_REG[0], GYRO_REG[1], GYRO_REG[2], GYRO_REG[3], GYRO_REG[4], GYRO_REG[5]])
		
		AxRaw = float(np.array((AccRawData[1] << 8) | AccRawData[0]).astype(np.int16))
		AyRaw = float(np.array((AccRawData[3] << 8) | AccRawData[2]).astype(np.int16))
		AzRaw = float(np.array((AccRawData[5] << 8) | AccRawData[4]).astype(np.int16))
		
		GxRaw = np.array((GyrRawData[1] << 8) | GyrRawData[0]).astype(np.int16)
		GyRaw = np.array((GyrRawData[3] << 8) | GyrRawData[2]).astype(np.int16)
		GzRaw = np.array((GyrRawData[5] << 8) | GyrRawData[4]).astype(np.int16)
		
		AxRaw = AxRaw / 16384.0
		AyRaw = AyRaw / 16384.0
		AzRaw = AzRaw / 16384.0
		
		# ~ GxRaw.append(int16( (GyrRawData[1] << 8) | GyrRawData[0] )) # type: ignore
		# ~ GyRaw.append(int16( (GyrRawData[3] << 8) | GyrRawData[2] )) # type: ignore
		# ~ GzRaw.append(int16( (GyrRawData[5] << 8) | GyrRawData[4] )) # type: ignore
		
		# Conversion from Raw Values to Corrected Values
		
		
		
		# ~ print("Gx: {0} ; Gy : {1} ; Gz : {2}".format(GxRaw, GyRaw, GzRaw))
		print("Ax: {0} ; Ay : {1} ; Az : {2}".format(AxRaw, AyRaw, AzRaw))
		# ~ print("Ax: {0} ; Ay : {1} ; Az : {2} ; Gx: {3} ; Gy : {4} ; Gz : {5}".format(AxRaw, AyRaw, AzRaw, GxRaw, GyRaw, GzRaw))
		time.sleep(0.1)
		i += 1
	
	i=0
	
	
# PROGRAM CODE

writeMPU9250Register(REGISTER_PWR_MGMT_1, REGISTER_VALUE_RESET) # RESET MPU
time.sleep(0.1)

writeMPU9250Register(REGISTER_INT_PIN_CFG, REGISTER_VALUE_BYPASS_EN) # Bypass Enable FOR DIRECT ACCESS TO auxiliary I2C BUS
time.sleep(0.1)

for x in range(6):
	GYRO_REG[x] |= 0x80
	ACC_REG[x] |= 0x80
	
get_data(10000)
		
# ~ print("Setting to Sleep:")
# ~ writeMPU9250Register(REGISTER_PWR_MGMT_1, 0x40)

# ~ get_data(10)

spi.close()

print("Test Complete.")


