from pyb import I2C, delay
from ustruct import unpack

#some MPU6050 Registers and their Address
PWR_MGMT_1   = const(0x6B)
SMPLRT_DIV   = const(0x19)
CONFIG       = const(0x1A)
GYRO_CONFIG  = const(0x1B)
INT_ENABLE   = const(0x38)
ACCEL_XOUT_H = const(0x3B)
ACCEL_YOUT_H = const(0x3D)
ACCEL_ZOUT_H = const(0x3F)
GYRO_XOUT_H  = const(0x43)
GYRO_YOUT_H  = const(0x45)
GYRO_ZOUT_H  = const(0x47)

device_addr = 104
i2c = I2C(2,I2C.MASTER)

def MPU_Init():
    #write to sample rate register
    i2c.mem_write(7, device_addr, SMPLRT_DIV)

    #Write to power management register
    i2c.mem_write(1, device_addr, PWR_MGMT_1)

    #Write to Configuration register
    i2c.mem_write(0, device_addr, CONFIG)

    #Write to Gyro configuration register
    i2c.mem_write(24, device_addr, GYRO_CONFIG)

    #Write to interrupt enable register
    i2c.mem_write(1, device_addr, INT_ENABLE)

def get_raw_values():
    data = i2c.mem_read(14, device_addr, 0x3B)
    return data

def get_values():
    raw_data = get_raw_values()
    values = unpack('>7h', raw_data)
    vals = {}
    vals['AcX'] = values[0]
    vals['AcY'] = values[1]
    vals['AcZ'] = values[2]
    vals['Tmp'] = values[3] / 340.00 + 36.53
    vals['GyX'] = values[4]
    vals['GyY'] = values[5]
    vals['GyZ'] = values[6]
    return vals

MPU_Init()

while True:
    print(get_values())
    delay(500)

