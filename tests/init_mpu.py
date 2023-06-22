import mpu9250_spi
import spidev
import os

spi1 = spidev.SpiDev()
spi1.open(0 , 0)

address = 0x68
# ~ myMPU9250 = mpu9250(address, spi1)
