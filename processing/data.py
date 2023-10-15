import serial
import numpy as np
from inference import detect_chewing

selected_port = 'COM3'
ser = serial.Serial(selected_port, 115200)
data_list = []

try:
    while True:
        data = ser.readline().decode().strip()
        if data:
            x, y, z = map(float, data.split())
            data_list.append((x, y, z))
            if len(data_list) == 20:
                print(f"Length of data list: {len(data_list)}")
                data_array = np.array(data_list)
                answer = detect_chewing(data_array.reshape(1, -1))
                print(answer)
                data_list.clear()

except KeyboardInterrupt:
    print("Data collection stopped.")

ser.close()
