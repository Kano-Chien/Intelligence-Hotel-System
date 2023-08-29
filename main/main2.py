import keyboard
import tkinter as tk
from contact_to_server import *

while True:
    time.sleep(0.01)
    if keyboard.is_pressed('f3'):
        def submit():
            value1 = entry1.get()
            value2 = entry2.get()
            window.destroy()
            print(get_cleaning_session())
            update_cleaning_session([int(value1), int(value2)])
            print(get_cleaning_session())


        window = tk.Tk()
        label1 = tk.Label(window, text="請輸入開始打掃時間(24小時制):")
        label1.pack()
        entry1 = tk.Entry(window)
        entry1.pack()
        label2 = tk.Label(window, text="請輸入結束打掃時間(24小時制):")
        label2.pack()
        entry2 = tk.Entry(window)
        entry2.pack()
        button = tk.Button(window, text="提交", command=submit)
        button.pack()
        window.mainloop()
