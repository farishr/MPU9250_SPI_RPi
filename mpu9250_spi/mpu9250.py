import spidev
import numpy as np
import config
import time, csv

class mpu9250:
	
	# Class Variables

	ACC_REG = []
	GYRO_REG = []
	TEMP_REG = []
	
	def __init__(self, address, bus, spi_clk=125000000):
		self.cfg = config.getConfigVals()
		self.cfg.Address = address
		self.spiBus = bus
		self.spiBus.max_speed_hz = spi_clk
		self.accel_bias = [0.0, 0.0, 0.0]
		self.gyro_bias = [0.0, 0.0, 0.0]
		
		mpu9250.ACC_REG = [self.cfg.AccelOut, self.cfg.AccelOut+1, self.cfg.AccelOut+2, self.cfg.AccelOut+3, self.cfg.AccelOut+4, self.cfg.AccelOut+5]
		mpu9250.GYRO_REG = [self.cfg.GyroOut, self.cfg.GyroOut+1, self.cfg.GyroOut+2, self.cfg.GyroOut+3, self.cfg.GyroOut+4, self.cfg.GyroOut+5]
		mpu9250.TEMP_REG = [self.cfg.TempOut, self.cfg.TempOut+1]
		
	# MEMBER FUNCTIONS
	
	def begin(self):
		self.writetoRegister(self.cfg.PowerManagement1, self.cfg.PowerReset)	# Reset MPU
		time.sleep(0.1)
		self.writetoRegister(self.cfg.InitPinConfig, self.cfg.BypassEN)	# Bypass Enable
		time.sleep(0.1)
		# ~ print(mpu9250.ACC_REG)
		self.AccelScale = 1/16384.0
		self.GyroScale = 1/16384.0
		
		for x in range(6):
			mpu9250.ACC_REG[x] |= 0x80
			mpu9250.GYRO_REG[x] |= 0x80
			
		mpu9250.TEMP_REG[1] |= 0x80
		mpu9250.TEMP_REG[0] |= 0x80

		
	def getRawAccValues(self):
		self.AccRegVals = self.spiBus.xfer([mpu9250.ACC_REG[0], mpu9250.ACC_REG[1], mpu9250.ACC_REG[2], mpu9250.ACC_REG[3], mpu9250.ACC_REG[4], mpu9250.ACC_REG[5]])
		raw_vals = [np.array((self.AccRegVals[1] << 8) | self.AccRegVals[0]).astype(np.int16),
					np.array((self.AccRegVals[3] << 8) | self.AccRegVals[2]).astype(np.int16),
					np.array((self.AccRegVals[5] << 8) | self.AccRegVals[4]).astype(np.int16)]
		return raw_vals
						   
	def getRawGyrValues(self):
		self.GyrRegVals = self.spiBus.xfer([mpu9250.GYRO_REG[0], mpu9250.GYRO_REG[1], mpu9250.GYRO_REG[2], mpu9250.GYRO_REG[3], mpu9250.GYRO_REG[4], mpu9250.GYRO_REG[5]])
		raw_vals = [np.array((self.GyrRegVals[1] << 8) | self.GyrRegVals[0]).astype(np.int16),
					np.array((self.GyrRegVals[3] << 8) | self.GyrRegVals[2]).astype(np.int16),
					np.array((self.GyrRegVals[5] << 8) | self.GyrRegVals[4]).astype(np.int16)]
		return raw_vals
	
	def getGValues(self):
		acc_vals = self.getRawAccValues()
		acc_vals = [(acc_vals[i] - self.accel_bias[i]) * self.AccelScale for i in range(3)]
		return acc_vals
		
	def getGyrValues(self):
		gyr_vals = self.getRawGyrValues()
		gyr_vals = [(gyr_vals[i] - self.gyro_bias[i]) * self.GyroScale for i in range(3)]
		return gyr_vals

	def getTemperature(self):
		self.TempVals = self.spiBus.xfer([mpu9250.TEMP_REG[0], mpu9250.TEMP_REG[1]])
		self.Temp = (float(np.array((self.TempVals[1] << 8) | self.TempVals[0]).astype(np.int16))/self.cfg.TempScale) + self.cfg.TempOffset
		return self.Temp
		
	def setAccRange(self, accelRange):
		"""Sets the range of accelerometer

		Parameters
		----------
		accelRange : str
			The supported ranges are as following ->
			2g  -> AccelRangeSelect2G
			4g  -> AccelRangeSelect4G
			8g  -> AccelRangeSelect8G
			16g -> AccelRangeSelect16G

		"""
		
		try:
			self.writetoRegister(self.cfg.AccelConfig, self.cfg[accelRange])
			self.AccelRange = accelRange
		except:
			print ("{0} is not a proper value for accelerometer range".format(accelRange))
			return -1
		accelVal = float(accelRange.split('t')[1].split('G')[0])
		self.AccelScale = accelVal/32767.5
		return 1
		
	def setGyroRange(self, gyroRange):
		"""Sets the range of gyroscope

		Parameters
		----------
		gyroRange : str
			The supported ranges are as following ->
			250DPS  -> GyroRangeSelect250DPS
			500DPS  -> GyroRangeSelect500DPS
			1000DPS -> GyroRangeSelect1000DPS
			2000DPS -> GyroRangeSelect2000DPS

			DPS means degrees per freedom

		"""

		try:
			self.writetoRegister(self.cfg.GyroConfig, self.cfg[gyroRange])
			self.GyroRange = gyroRange
		except:
			print ("{0} is not a proper value for gyroscope range".format(gyroscope))
			return -1
		gyroVal = float(gyroRange.split('t')[1].split('D')[0])
		self.GyroScale = gyroVal/32767.5
		return 1
		
	# Digital Low Pass Filters
	
	def enableGyrDLPF(self):
		regVal = self.readfromRegister(self.cfg.GyroConfig)
		time.sleep(0.1)
		regVal &= 0xFC
		self.writetoRegister(self.cfg.GyroConfig, regVal)
	
	def enableAccDLPF(self):
		regVal = self.readfromRegister(self.cfg.AccelConfig2)
		time.sleep(0.1)
		regVal &= ~8
		self.writetoRegister(self.cfg.AccelConfig2, regVal)
		
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
	
	def setAccDLPF(self, accfrequency):
		try:
			self.writetoRegister(self.cfg.AccelConfig2, self.cfg[accfrequency])
			self.Frequency = accfrequency
			time.sleep(0.1)
		except:
			print ("{0} is not a proper value for low pass filter".format(accfrequency))
			return -1
		return 1
		
	def setGyrDLPF(self, gyrfrequency):
		try:
			self.writetoRegister(self.cfg.GyroConfig2, self.cfg[gyrfrequency])
			self.Frequency = gyrfrequency
			time.sleep(0.1)
		except:
			print ("{0} is not a proper value for low pass filter".format(gyrfrequency))
			return -1
		return 1
	
	# Calibration
		
	def calibrate(self, calib_samples):
		self.setAccRange("AccelRangeSelect2G")
		self.setGyroRange("GyroRangeSelect250DPS")
		# ~ self.enableAccDLPF()
		# ~ self.enableGyrDLPF()
		print("Starting Calibration...")
		
		for i in range(calib_samples):
			a_vals = myMPU9250.getRawAccValues()
			g_vals = myMPU9250.getRawGyrValues()
			self.accel_bias[0] += a_vals[0]
			self.accel_bias[1] += a_vals[1]
			self.accel_bias[2] += a_vals[2]
			self.gyro_bias[0] += g_vals[0]
			self.gyro_bias[1] += g_vals[1]
			self.gyro_bias[2] += g_vals[2]
			time.sleep(0.05)
		
		for j in range(3):
			self.accel_bias[j] = self.accel_bias[j]/calib_samples
			self.gyro_bias[j] = self.gyro_bias[j]/calib_samples
		
		self.accel_bias[2] = self.accel_bias[2] - 1 	# Adjusting for Z Axis gravity

	def clear_offsets(self):
		self.accel_bias = [0.0 for x in range(3)]
		self.gyro_bias = [0.0 for x in range(3)]
	
	def writetoRegister(self, addr, val):
		self.spiBus.xfer([addr,val])		# [<Address to be Written to>, <Value to be written to the Address>]
		time.sleep(0.1)
	
	def readfromRegister(self, reg):
		reg |= 0x80
		val = self.spiBus.xfer([reg])
		return val[0]


	@property
	def spiBus(self):
		return self._spiBus

	@spiBus.setter
	def spiBus(self, spiBus):
		if isinstance(spiBus, spidev.SpiDev):
			self._spiBus = spiBus
		else:
			raise Exception("Please provide the object created by spidev")
			

# ######################Testing Section######################

AxRaw, AyRaw, AzRaw, GxRaw, GyRaw, GzRaw = [],[],[],[],[],[]

spi1 = spidev.SpiDev()
spi1.open(0 , 0)

address = 0x68
myMPU9250 = mpu9250(address, spi1,2000000)

myMPU9250.begin()

myMPU9250.calibrate(100)

for y in range(50):
	accel = myMPU9250.getGValues()
	print(accel)
	time.sleep(0.2)

print("Setting Offsets")
myMPU9250.clear_offsets()
time.sleep(10)

for y in range(50):
	accel = myMPU9250.getGValues()
	print(accel)
	time.sleep(0.2)
