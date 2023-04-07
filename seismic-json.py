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

# Send the configuration commands to the accelerometer
ser.write(b'\xAA\x52\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF2')

# Open a file to write the sensor data to
file = open("sensor_data.json", "w")

# Read and log the sensor data continuously
while True:
    data = ser.read(44)
    if len(data) == 44:
        ax, ay, az, gx, gy, gz, mx, my, mz, baro, alt, temp, q0, q1, q2, q3 = struct.unpack('>hhh hhh hhh f f h f f f f', data)

        # Create a dictionary to hold the sensor data
        sensor_data = {
            "timestamp": time.time(),
            "acceleration": {
                "x": ax,
                "y": ay,
                "z": az
            },
            "angular_velocity": {
                "x": gx,
                "y": gy,
                "z": gz
            },
            "angle": {
                "q0": q0,
                "q1": q1,
                "q2": q2,
                "q3": q3
            },
            "magnetic": {
                "x": mx,
                "y": my,
                "z": mz
            },
            "atmospheric_pressure": baro,
            "altitude": alt,
            "temperature": temp
        }

        # Write the sensor data to the JSON file
        json.dump(sensor_data, file)
        file.write("\n")

        print(sensor_data)

    time.sleep(0.001)

ser.close()
file.close()
