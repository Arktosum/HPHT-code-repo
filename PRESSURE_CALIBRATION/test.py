import pyautogui
import time
# Wait for user input in the console.

PRESSURE = 115
INCREMENT = 5
DELAY_TIME = 10  # seconds
# Type the text at the current cursor position
time.sleep(10)
while True:
    pyautogui.typewrite(str(PRESSURE))
    # Send the Enter key
    pyautogui.press("enter")
    PRESSURE += INCREMENT
    time.sleep(DELAY_TIME)
