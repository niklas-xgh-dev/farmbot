import pyautogui
import keyboard
import time
from PIL import ImageGrab

print("Press 'p' to print coordinates and RGB. Press 'q' to quit.")

def get_pixel_color(x, y):
   screen = ImageGrab.grab(bbox=(x, y, x+1, y+1))
   return screen.getpixel((0, 0))

try:
   while True:
       if keyboard.is_pressed('p'):
           x, y = pyautogui.position()
           color = get_pixel_color(x, y)
           print(f"Coordinates: x={x}, y={y}")
           print(f"RGB color: {color}")
           time.sleep(0.2)
       elif keyboard.is_pressed('q'):
           break
except KeyboardInterrupt:
   pass