import serial
import numpy as np
import tkinter as tk
from Model.inference import detect_chewing
from threading import Thread


selected_port = 'COM4'
ser = serial.Serial(selected_port, 115200)
data_list = []
chewing_count = 0
not_chewing_count = 0
window = tk.Tk()
window.title("Chewing Detection")
window.geometry("1920x1080")
#background_image = tk.PhotoImage(file="./Assets/img/Background.png")
#background_label = tk.Label(window, image=background_image)
#background_label.place(relwidth=1, relheight=1)
logo = tk.PhotoImage(file="./Assets/img/healthy_eating_logo.png")
logo_label = tk.Label(window, image=logo)
logo_label.pack()
result_label = tk.Label(window, text="Result: ", font=("Helvetica", 16))
result_label.pack()
count_label = tk.Label(window, text="Chewing Count: 0", font=("Helvetica", 12))
count_label.pack()
count_label_not = tk.Label(window, text="Interval Status: 0", font=("Helvetica", 12))
count_label_not.pack()
suggestion_label = tk.Label(window, text="", font=("Helvetica", 16))
suggestion_label.pack()

def calculate_chewing_rate():
    total_count = chewing_count + not_chewing_count
    if total_count > 0:
        rate = (chewing_count / total_count) * 100
        return rate
    return 0

def update_suggestion():
    rate = calculate_chewing_rate()
    if rate < 50:
        suggestion_label.config(text="Chew more!")
    else:
        suggestion_label.config(text="Healthy Chewing!")
        play_healthy_chewing_music()

def process_data():
    global chewing_count, not_chewing_count

    try:
        while True:
            data = ser.readline().decode().strip()
            if data:
                x, y, z = map(float, data.split())
                data_list.append((x, y, z))
                if len(data_list) == 30:
                    data_array = np.array(data_list)
                    answer = detect_chewing(data_array.reshape(1, -1))
                    if answer == 1:
                        result_label.config(text="Result: Chewing")
                        chewing_count += 1
                        count_label.config(text=f"Chewing Count: {chewing_count}")
                    else:
                        result_label.config(text="Result: Not Chewing")
                        not_chewing_count += 1
                        count_label_not.config(text=f"Interval Status Count: {not_chewing_count}")
                    data_list.clear()
                    update_suggestion()
    except KeyboardInterrupt:
        print("Data collection stopped.")
        ser.close()

def play_healthy_chewing_music():
    import pygame
    pygame.init()
    pygame.mixer.music.load('./Assets/L.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

import threading
data_thread = threading.Thread(target=process_data)
data_thread.start()

window.mainloop()
