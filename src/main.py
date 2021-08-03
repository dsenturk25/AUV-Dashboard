import cv2
import tkinter as tk
import tkinter.font as font
from PIL import Image
from PIL import ImageTk
import numpy as np

root = tk.Tk()
root.resizable(0, 0)

canvas = tk.Canvas(root, width=1000, height=700)
canvas.pack()

header = tk.Label(canvas, text="Tigers Robotics ROV Dashboard", font=("Arial", 20))
header.place(relwidth=0.35, relheight=0.1, rely=0.02, relx=0.02)

lower_hue_label = tk.Label(canvas, text="Lower Hue", font=("Arial", 10))
lower_hue_label.place(relwidth=0.1, relheight=0.1, rely=0.15, relx=0.04)

lower_hue = tk.Scale(canvas, from_=0, to=255, orient="horizontal")
lower_hue.place(relwidth=0.35, relheight=0.1, rely=0.16, relx=0.13)

lower_saturation_label = tk.Label(canvas, text="Lower Saturation", font=("Arial", 10))
lower_saturation_label.place(relwidth=0.1, relheight=0.1, rely=0.24, relx=0.04)

lower_saturation = tk.Scale(canvas, from_=0, to=255, orient="horizontal")
lower_saturation.place(relwidth=0.35, relheight=0.1, rely=0.25, relx=0.13)

lower_value_label = tk.Label(canvas, text="Lower Value", font=("Arial", 10))
lower_value_label.place(relwidth=0.1, relheight=0.1, rely=0.32, relx=0.04)

lower_value = tk.Scale(canvas, from_=0, to=255, orient="horizontal")
lower_value.place(relwidth=0.35, relheight=0.1, rely=0.33, relx=0.13)

upper_hue_label = tk.Label(canvas, text="Upper Hue", font=("Arial", 10))
upper_hue_label.place(relwidth=0.1, relheight=0.1, rely=0.44, relx=0.04)

upper_hue = tk.Scale(canvas, from_=0, to=255, orient="horizontal")
upper_hue.place(relwidth=0.35, relheight=0.1, rely=0.45, relx=0.13)

upper_saturation_label = tk.Label(canvas, text="Upper Saturation", font=("Arial", 10))
upper_saturation_label.place(relwidth=0.1, relheight=0.1, rely=0.54, relx=0.04)

upper_saturation = tk.Scale(canvas, from_=0, to=255, orient="horizontal")
upper_saturation.place(relwidth=0.35, relheight=0.1, rely=0.55, relx=0.13)

upper_value_label = tk.Label(canvas, text="Upper Value", font=("Arial", 10))
upper_value_label.place(relwidth=0.1, relheight=0.1, rely=0.64, relx=0.04)

upper_value = tk.Scale(canvas, from_=0, to=255, orient="horizontal")
upper_value.place(relwidth=0.35, relheight=0.1, rely=0.65, relx=0.13)

# connect to server UI widgets

server_label = tk.Label(canvas, text="Server (localhost:3000, RPI 4)", font=("Arial", 16))
server_label.place(relwidth=0.22, relheight=0.1, rely=0.80, relx=0.1)

connect_button = tk.Button(canvas, text="Connect")
connect_button.place(relwidth=0.1, relheight=0.05, rely=0.825, relx=0.34)

# imageViews for original and filtered

cap = cv2.VideoCapture('http:/localhost:3000/video')

original_feed = tk.Label(canvas)
original_feed.place(relwidth=0.4, relheight=0.4, rely=0.1, relx=0.5)

filtered_feed = tk.Label(canvas)
filtered_feed.place(relwidth=0.4, relheight=0.4, rely=0.5, relx=0.5)

while True:
    ret, frame = cap.read()

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_b = np.array([lower_hue.get(), lower_saturation.get(), lower_value.get()])
    u_b = np.array([upper_hue.get(), upper_saturation.get(), upper_value.get()])

    mask = cv2.inRange(hsv_image, l_b, u_b)
    final = cv2.bitwise_and(frame, frame, mask=mask)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)

    frame = Image.fromarray(frame)
    final = Image.fromarray(final)

    frame = ImageTk.PhotoImage(frame)
    final = ImageTk.PhotoImage(final)

    original_feed.image = frame
    original_feed.configure(image=frame)
    filtered_feed.image = final
    filtered_feed.configure(image=final)

    root.update()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break


root.mainloop()

cap.release()
cv2.destroyAllWindows()
