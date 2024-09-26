import network
import urequests
import time
import json
import dht
from machine import I2C, Pin
import utime

MPU6050_ADDR = 0x68

temp_register = 0x41
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
PWR_MGMT_1 = 0x6B


i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400000)

i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b'\x00')

def read_raw_data(addr):

    high = i2c.readfrom_mem(MPU6050_ADDR, addr, 1)[0]
    low = i2c.readfrom_mem(MPU6050_ADDR, addr + 1, 1)[0]
    
    value = (high << 8) | low

    if value > 32767:
        value -= 65536
        
    return value

def Get_Acc_Data():
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)
    
    accel_x = accel_x / 16384.0
    accel_y = accel_y / 16384.0
    accel_z = accel_z / 16384.0
    
    return accel_x, accel_y, accel_z

firebase_url = 'https://omniverse-cloud-data-default-rtdb.firebaseio.com/accel.json'

ssid = 'wifi name'
password = 'passowrd'

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

def send_to_firebase(x, y, z):
    data = {'x': x, 'y': y, 'z': z}
    try:
        response = urequests.post(firebase_url, json=data)
        print('Data sent to Firebase:', response.text)
        response.close()
    except Exception:
        print('Error sending data')

connect_to_wifi()

while True:
    accel_x, accel_y, accel_z = Get_Acc_Data()
    print(f'X: {accel_x}, Y: {accel_y}, Z: {accel_z}')
    send_to_firebase(accel_x, accel_y, accel_z)
    time.sleep(1)
