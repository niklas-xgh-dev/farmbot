import yaml
import pyautogui
import time
import random
from PIL import ImageGrab
import logging
from pathlib import Path
import sys

logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s',
   handlers=[logging.FileHandler('monster_hunter.log'), logging.StreamHandler()]
)

class MonsterHunter:
   def __init__(self, config_path='config.yaml'):
       self.load_config(config_path)
       pyautogui.FAILSAFE = True
       self.movement_keys = ['w', 'a', 's', 'd']
       
   def load_config(self, config_path):
       try:
           with open(config_path, 'r') as f:
               config = yaml.safe_load(f)
               self.target_color = config['target_color']
               self.target_pos = tuple(config['target_position'])
               self.scan_area = tuple(config['scan_area'])
               self.color_tolerance = config.get('color_tolerance', 20)
               self.sample_size = config.get('sample_size', 5)
               self.scan_step = config.get('scan_step', 50)
       except Exception as e:
           logging.error(f"Failed to load config: {e}")
           sys.exit(1)

   def random_movement(self, duration=0.5):
       key = random.choice(self.movement_keys)
       pyautogui.keyDown(key)
       time.sleep(random.uniform(0.1, duration))
       pyautogui.keyUp(key)

   def check_pixel_color(self):
       try:
           x, y = self.target_pos
           area = (x - self.sample_size, y - self.sample_size, 
                  x + self.sample_size, y + self.sample_size)
           screen = ImageGrab.grab(bbox=area)
           center = screen.getpixel((self.sample_size, self.sample_size))
           logging.info(f"Current pixel color: {center}")
           
           return all(abs(c - t) <= self.color_tolerance 
                     for c, t in zip(center, self.target_color))
       except Exception as e:
           logging.error(f"Screenshot failed: {e}")
           return False

   def scan_pattern(self):
        x1, y1, x2, y2 = self.scan_area
        try:
            while True:
                # Divide area into quadrants for better coverage
                quadrant = random.randint(1, 4)
                if quadrant == 1:
                    x = random.randint(x1, (x1 + x2)//2)
                    y = random.randint(y1, (y1 + y2)//2)
                elif quadrant == 2:
                    x = random.randint((x1 + x2)//2, x2)
                    y = random.randint(y1, (y1 + y2)//2)
                elif quadrant == 3:
                    x = random.randint(x1, (x1 + x2)//2)
                    y = random.randint((y1 + y2)//2, y2)
                else:
                    x = random.randint((x1 + x2)//2, x2)
                    y = random.randint((y1 + y2)//2, y2)

                pyautogui.moveTo(x, y, duration=0.05)  # Faster movement
                
                if self.check_pixel_color():
                    return True
                
                self.random_movement(1)  # Shorter movement duration
                time.sleep(0.02)  # Shorter sleep
                
        except Exception as e:
            logging.error(f"Scan error: {e}")
            return False

   def hunt(self):
        logging.info("Starting monster hunter...")
        time.sleep(3)
        last_key_press = 0
        
        try:
            self.press_8()
            last_key_press = time.time()
            
            while True:
                current_time = time.time()
                if current_time - last_key_press >= 21:
                    self.press_8()
                    last_key_press = current_time
                    
                if self.scan_pattern():
                    current_pos = pyautogui.position()
                    pyautogui.doubleClick()
                    time.sleep(3)
                    self.random_movement(1)
                time.sleep(0.05)
        except KeyboardInterrupt:
            logging.info("Stopped by user")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

   def press_8(self):
        pyautogui.keyDown('8')
        time.sleep(0.1)
        pyautogui.keyUp('8')
        logging.info("Pressed 8")

if __name__ == "__main__":
   hunter = MonsterHunter()
   hunter.hunt()