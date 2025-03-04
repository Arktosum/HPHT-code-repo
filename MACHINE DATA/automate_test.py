import pyautogui
import time
print("Move your mouse to the desired position and click. Press Ctrl + C to exit.")

value = 100
INCREMENT = 0.5
RAMP_TIME = 5

while True:
    pyautogui.write(str(value), interval=0.1)  # Type text
    pyautogui.press("ENTER")  # Press Enter
    value += INCREMENT
    time.sleep(RAMP_TIME)
    