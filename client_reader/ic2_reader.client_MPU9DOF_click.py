#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import smbus
from socketIO_client import SocketIO
from socketIO_client import BaseNamespace

"""
    File name: reader-i2c-mpu9dof-client-django.socket.io.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 03/10/2016
    License: MIT
    Python Version: 2.7
    Code guide line: PEP8 - reST Sphinx

    About MPU-9DOF click [MikroElektronika/www.mikroe.com]:
        http://www.mikroe.com/click/mpu-9dof/
        http://download.mikroe.com/documents/add-on-boards/click/mpu-9dof/mpu-9dof-click-manual-v100.pdf
        http://learn.mikroe.com/mems-sensors-conversion-physical-world-digital-world/
        http://libstock.mikroe.com/projects/download/1149/0/1149_mpu_9dof___example_v1.0.0.0.zip

"""

# Device direction bus
DEVICE_BUS = 1
# Initial direction in I2C device
ADDRESS_IC2_START = 0x69
# IP server Django-socket.io
IP_SERVER = '192.168.1.44'
# Port server Django-socket.io
PORT_SERVER = 8000
# Instance bus
bus = smbus.SMBus(DEVICE_BUS)


def cls():

    os.system('cls' if os.name=='nt' else 'clear')


def config_i2c():
        # MPUREG_PWR_MGMT, BIT_H_RESET
        bus.write_byte_data(ADDRESS_IC2_START, 0x6b, 0x80)
        time.sleep(0.1) # 0.1
        # MPUREG_SMPLRT_DIV, 0
        bus.write_byte_data(ADDRESS_IC2_START, 0x19, 0x00)
        # MPUREG_CONFIG, BITS_DLPF_CFG_42HZ
        bus.write_byte_data(ADDRESS_IC2_START, 0x1a, 0x03)
        # MPUGREG_GYRO_CONFIG, BITS_F_1000DPS
        bus.write_byte_data(ADDRESS_IC2_START, 0x1b, 0x10)
        # MPUREG_ACCEL_CONFIG, 10
        bus.write_byte_data(ADDRESS_IC2_START, 0x1c, 0x10)
        # MPUREG_FIFO_EN, BIT_FIFO_DIS
        bus.write_byte_data(ADDRESS_IC2_START, 0x23, 0x00)
        # MPUREG_INT_PIN_CFG, 2
        bus.write_byte_data(ADDRESS_IC2_START, 0x37, 0x02)
        # MPUREG_INT_ENABLE, 0
        bus.write_byte_data(ADDRESS_IC2_START, 0x38, 0x00)
        # MPUREG_USER_CTRL, 0
        bus.write_byte_data(ADDRESS_IC2_START, 0x6a, 0x00)
        # PUREG_PWR_MGMT_1, 0
        bus.write_byte_data(ADDRESS_IC2_START, 0x6b, 0x00)
        # PUREG_PWR_MGMT_2, 0
        bus.write_byte_data(ADDRESS_IC2_START, 0x6c, 0x00)
        # MAGREG_CNTL, 1
        bus.write_byte_data(ADDRESS_IC2_START, 0x0a, 0x01)


def read_sensor():
        # Gyroscope
        x_h = bus.read_byte_data(ADDRESS_IC2_START, 0x43)  # h
        x_l = bus.read_byte_data(ADDRESS_IC2_START, 0x44)  # l
        y_h = bus.read_byte_data(ADDRESS_IC2_START, 0x45)
        y_l = bus.read_byte_data(ADDRESS_IC2_START, 0x46)
        z_h = bus.read_byte_data(ADDRESS_IC2_START, 0x47)
        z_l = bus.read_byte_data(ADDRESS_IC2_START, 0x48)
        x = int((x_h << 8) | x_l)
        y = int((y_h << 8) | y_l)
        z = int((z_h << 8) | z_l)
        print "X sin componer: " + str(x_h) + "h::" + str(x_l) + "l"
        print "Y sin componer: " + str(y_h) + "h::" + str(y_l) + "l"
        print "Z sin componer: " + str(z_h) + "h::" + str(z_l) + "l"
        print "Compose X:" + str(x)
        print "Compose Y:" + str(y)
        print "Compose Z:" + str(z)
        print "[Calibration]"
        print " +-- a X: " + str(x-65250)
        print " +-- a Y: " + str(y-65250)
        print " +-- a Z: " + str(z-150)
        print "-"

        # Temperature
        t_h = bus.read_byte_data(ADDRESS_IC2_START, 0x41) # h
        t_l = bus.read_byte_data(ADDRESS_IC2_START, 0x42) # l
        t = int((t_h << 8) | t_l)
        print "Temp sin componer: " + str(t_h) + "h::" + str(t_l) + "l  >> " \
              + str(t)
        print "Temp: " + str((t/340.0)+36.5)
        print "[Calibration]"
        print " +-- Temp: " + str(((t/340.0)+36.5)-200)
        print "-"

        # Json and calibration
        return {'X': x-65250,
                'Y': y-65250,
                'Z': z-150,
                'TEMP': ((t/340.0)+36.5)-200 }

if __name__ == "__main__":
    try:
        print ("Connecting...")
        socketIO = SocketIO(IP_SERVER, PORT_SERVER)
        api_namespace = socketIO.define(BaseNamespace, '/streaming')

        print ("[+]Configuration device. MPU9DOF click MikroElektronika")
        config_i2c()

        print ("[+]Reading sensor")
        while True:
                json_data_sensor = read_sensor()
                api_namespace.emit('push_data_api', json_data_sensor)
                time.sleep(0.1)
                cls()
    except Exception as e:
        print ("Connection refused: " + e.message)