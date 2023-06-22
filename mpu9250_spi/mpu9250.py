import spidev
import numpy as np
import config
import time

class mpu9250:
	
	# Class Variables

	
	ACC_REG = []
	# ~ for x in range(6):
		# ~ GYRO_REG[x] |= 0x80
		# ~ ACC_REG[x] |= 0x80
	
	def __init__(self, address, bus, spi_clk=125000000):
		self.cfg = config.getConfigVals()
		self.cfg.Address = address
		self.spiBus = bus
		self.spiBus.max_speed_hz = spi_clk
		
		mpu9250.ACC_REG = [self.cfg.AccelOut, self.cfg.AccelOut+1, self.cfg.AccelOut+2, self.cfg.AccelOut+3, self.cfg.AccelOut+4, self.cfg.AccelOut+5]
		print(mpu9250.ACC_REG)
	
	def begin(self):
		self.writetoRegister(self.cfg.PowerManagement1, self.cfg.PowerReset)	# Reset MPU
		time.sleep(0.1)
		self.writetoRegister(self.cfg.InitPinConfig, self.cfg.BypassEN)	# Bypass Enable
		time.sleep(0.1)
		
		ACC_REG = [self.cfg.AccelOut, self.cfg.AccelOut+1, self.cfg.AccelOut+2, self.cfg.AccelOut+3, self.cfg.AccelOut+4, self.cfg.AccelOut+5]
		for x in range(6):
			# ~ GYRO_REG[x] |= 0x80
			ACC_REG[x] |= 0x80
		
		accOffsetVal = 0.0
		accOffsetVal = 0.0
		accOffsetVal = 0.0
		accRangeFactor = 1
		gyrOffsetVal = 0.0
		gyrOffsetVal = 0.0
		gyrOffsetVal = 0.0
		gyrRangeFactor = 1
		
	def getRawGValues(self):
			
		self.AccRegVals = self.spiBus.xfer(mpu9250.ACC_REG)
		self.AccRawData = [float(np.array((self.AccRegVals[1] << 8) | self.AccRegVals[0]).astype(np.int16)),
						   float(np.array((self.AccRegVals[3] << 8) | self.AccRegVals[2]).astype(np.int16)),
						   float(np.array((self.AccRegVals[5] << 8) | self.AccRegVals[4]).astype(np.int16))]
		print(mpu9250.ACC_REG)
	
	def enableGyrDLPF(self):
		regVal = self.readfromRegister(self.cfg.GyroConfig)
		time.sleep(0.1)
		regVal &= 0xFC
		self.writetoRegister(self.cfg.GyroConfig, regVal)

	
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
myMPU9250 = mpu9250(address, spi1)

myMPU9250.begin()
myMPU9250.enableGyrDLPF()

# ~ while True:
myMPU9250.getRawGValues()
	# ~ print("Ax: {0} ; Ay : {1} ; Az : {2}".format(myMPU9250.AccRawData[0], myMPU9250.AccRawData[1], myMPU9250.AccRawData[2]))
	# ~ time.sleep(0.2)



