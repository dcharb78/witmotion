import struct
import serial
import time
import json
from serial.tools import list_ports

def find_ch340_port():
    for port in list_ports.grep('1a86:7523'):
        return port.device
    raise Exception("QinHeng Electronics CH340 serial converter not found")

serial_port = find_ch340_port()

ser = serial.Serial(
    port=serial_port,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)
def read_accelerometer_calibration_values(): 
    """Read the accelerometer calibration values from the witmotion WT901BLE device over USB serial.""" 
     
    # Send command to read calibration values 
    ser.write(b'\x55\x71') 
     
    # Read response 
    response = ser.read(18) 
     
    # Parse response 
    axL = response[2] 
    axH = response[3] 
    ayL = response[4] 
    ayH = response[5] 
    azL = response[6] 
    azH = response[7] 
    wxL = response[8] 
    wxH = response[9] 
    wyL = response[10] 
    wyH = response[11] 
    wzL = response[12] 
    wzH = response[13] 
    RollL = response[14] 
    RollH = response[15] 
    PitchL = response[16] 
    PitchH = response[17] 
    YawL = response[18] 
    YawH = response[19] 
     
    # Calculate accelerometer values 
    ax = (axH << 8) | axL 
    ay = (ayH << 8) | ayL 
    az = (azH << 8) | azL 
    ax = ax/32768 * 16 g 
    ay = ay/32768 * 16 g 
    az = az/32768 * 16 g 
     
    # Calculate angular velocity values 
    wx = (wxH << 8) | wxL 
    wy = (wyH << 8) | wyL 
    wz = (wzH << 8) | wzL 
    wx = wx/32768 * 2000°/s 
    wy = wy/32768 * 2000°/s 
    wz = wz/32768 * 2000°/s 
     
    # Calculate Euler angles 
    Roll = (RollH << 8) | RollL 
    Pitch = (PitchH << 8) | PitchL 
    Yaw = (YawH << 8) | YawL 
    Roll = Roll/32768 * 180° 
    Pitch = Pitch/32768 * 180° 
    Yaw = Yaw/32768 * 180° 
     
    # Return the acceleration, angular velocity, and Euler angles 
    return (ax, ay, az, wx, wy, wz, Roll, Pitch, Yaw) 

ser.close()
file.close()
