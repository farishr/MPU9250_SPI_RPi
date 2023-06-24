import spidev
import numpy as np
import config
import time

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
		
		for x in range(6):
			mpu9250.ACC_REG[x] |= 0x80
			mpu9250.GYRO_REG[x] |= 0x80
			
		mpu9250.TEMP_REG[1] |= 0x80
		mpu9250.TEMP_REG[0] |= 0x80
		
		# ~ print(mpu9250.ACC_REG)
		
		AxOffsetVal = 0.0
		AyOffsetVal = 0.0
		AzOffsetVal = 0.0
		accRangeFactor = 1
		GxOffsetVal = 0.0
		GyOffsetVal = 0.0
		GzOffsetVal = 0.0
		gyrRangeFactor = 1
		
	def getRawAccValues(self):
		self.AccRegVals = self.spiBus.xfer([mpu9250.ACC_REG[0], mpu9250.ACC_REG[1], mpu9250.ACC_REG[2], mpu9250.ACC_REG[3], mpu9250.ACC_REG[4], mpu9250.ACC_REG[5]])
		self.AccRawData = [np.array((self.AccRegVals[1] << 8) | self.AccRegVals[0]).astype(np.int16),
						   np.array((self.AccRegVals[3] << 8) | self.AccRegVals[2]).astype(np.int16),
						   np.array((self.AccRegVals[5] << 8) | self.AccRegVals[4]).astype(np.int16)]
		return self.AccRawData
						   
	def getRawGyrValues(self):
		self.GyrRegVals = self.spiBus.xfer([mpu9250.GYRO_REG[0], mpu9250.GYRO_REG[1], mpu9250.GYRO_REG[2], mpu9250.GYRO_REG[3], mpu9250.GYRO_REG[4], mpu9250.GYRO_REG[5]])
		self.GyrRawData = [np.array((self.GyrRegVals[1] << 8) | self.GyrRegVals[0]).astype(np.int16),
						   np.array((self.GyrRegVals[3] << 8) | self.GyrRegVals[2]).astype(np.int16),
						   np.array((self.GyrRegVals[5] << 8) | self.GyrRegVals[4]).astype(np.int16)]
		return self.GyrRawData

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
		self.AccelScale = self.cfg.Gravity*accelVal/32767.5
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
		self.GyroScale = self.cfg.Degree2Radian*(gyroVal/32767.5)
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
	
	def setAccDLPF(self, accfrequency):
		try:
			self.writetoRegister(self.cfg.AccelConfig2, self.cfg[accfrequency])
			self.Frequency = accfrequency
		except:
			print ("{0} is not a proper value forlow pass filter".format(accfrequency))
			return -1
		return 1
		
	def setGyrDLPF(self, gyrfrequency):
		try:
			self.writetoRegister(self.cfg.GyroConfig2, self.cfg[gyrfrequency])
			self.Frequency = gyrfrequency
		except:
			print ("{0} is not a proper value forlow pass filter".format(gyrfrequency))
			return -1
		return 1
	
	# Calibration
		
	def autoOffsets(self):
		self.setAccRange("AccelRangeSelect2G")
		self.setGyroRange("GyroRangeSelect250DPS")

	
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

spi1 = spidev.SpiDev()
spi1.open(0 , 0)

address = 0x68
myMPU9250 = mpu9250(address, spi1,1000000)

myMPU9250.begin()
myMPU9250.enableGyrDLPF()

i=0
j=0

while i<50:
	gyro_sensor = myMPU9250.getRawGyrValues()
	print("Gx: {0} ; Gy : {1} ; Gz : {2}".format(gyro_sensor[0], gyro_sensor[1], gyro_sensor[2]))
	# ~ print("Gx: {0} ; Gy : {1} ; Gz : {2}".format(myMPU9250.GyrRawData[0], myMPU9250.GyrRawData[1], myMPU9250.GyrRawData[2]))
	
	# ~ acc_sensor = myMPU9250.getRawAccValues()
	# ~ print("Ax: {0} ; Ay : {1} ; az : {2}".format(acc_sensor[0], acc_sensor[1], acc_sensor[2]))
	
	# ~ temp = myMPU9250.getTemperature()
	# ~ print("Temp: {0}".format(temp))
	i+=1
	time.sleep(0.2)

myMPU9250.enableAccDLPF()
myMPU9250.setGyrDLPF("AccelLowPassFilter184")
print("DLPF SET")

while j<50:
	gyro_sensor = myMPU9250.getRawGyrValues()
	print("Gx: {0} ; Gy : {1} ; Gz : {2}".format(gyro_sensor[0], gyro_sensor[1], gyro_sensor[2]))
	# ~ print("Gx: {0} ; Gy : {1} ; Gz : {2}".format(myMPU9250.GyrRawData[0], myMPU9250.GyrRawData[1], myMPU9250.GyrRawData[2]))
	
	# ~ acc_sensor = myMPU9250.getRawAccValues()
	# ~ print("Ax: {0} ; Ay : {1} ; az : {2}".format(acc_sensor[0], acc_sensor[1], acc_sensor[2]))
	
	# ~ temp = myMPU9250.getTemperature()
	# ~ print("Temp: {0}".format(temp))
	j+=1
	time.sleep(0.2)

