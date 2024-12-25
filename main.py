import yaml
import pyautogui
import time
import random
import math
from PIL import ImageGrab
import logging
import keyboard
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)

def load_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            return {
                'target_color': config['target_color'],
                'target_pos': tuple(config['target_position']),
                'scan_area': tuple(config['scan_area']),
                'color_tolerance': config.get('color_tolerance', 20),
                'sample_size': config.get('sample_size', 5),
                'scan_step': config.get('scan_step', 15)  # Reduced step size
            }
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        sys.exit(1)

def check_pixel_color(config):
    try:
        x, y = config['target_pos']
        sample_size = config['sample_size']
        area = (x - sample_size, y - sample_size, 
               x + sample_size, y + sample_size)
        screen = ImageGrab.grab(bbox=area)
        center = screen.getpixel((sample_size, sample_size))
        
        return all(abs(c - t) <= config['color_tolerance'] 
                  for c, t in zip(center, config['target_color']))
    except Exception as e:
        logging.error(f"Screenshot failed: {e}")
        return False

def move_character(key, duration=0.5):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def press_8():
    pyautogui.keyDown('8')
    time.sleep(0.1)
    pyautogui.keyUp('8')

def efficient_scan(config):
    x1, y1, x2, y2 = config['scan_area']
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    radius = min((x2 - x1), (y2 - y1)) // 3
    angle = 0
    step = 35  # Increased angle step
    expansion_rate = 0.5  # Faster spiral expansion
    
    while is_running and angle < 560:
        r = radius * (angle / 560.0) * expansion_rate
        x = center_x + int(r * math.cos(math.radians(angle)))
        y = center_y + int(r * math.sin(math.radians(angle)))
        
        x = max(x1, min(x2, x))
        y = max(y1, min(y2, y))
        
        pyautogui.moveTo(x, y, duration=0.005)  # Faster movement
        
        if check_pixel_color(config):
            return True
            
        angle += step
        
    return False

def hunt(config):
    global kills
    logging.info("Starting farmbot...")
    time.sleep(2)
    last_key_press = 0
    movement_sequence = ['w', 's', 'a', 'd']
    current_move = 0
    
    try:
        while True:
            if not is_running:
                time.sleep(0.1)
                continue
                
            current_time = time.time()
            
            # Skill management
            if current_time - last_key_press >= 21:
                press_8()
                last_key_press = current_time
            
            # Character movement
            move_character(movement_sequence[current_move], 0.5)
            current_move = (current_move + 1) % 4
            
            # Monster scanning
            if efficient_scan(config):
                pyautogui.doubleClick()
                kills += 1
                logging.info(f"Kills: {kills}")
                time.sleep(2)  # Reduced wait time
            
            time.sleep(0.01)
            
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def toggle_bot():
    global is_running
    is_running = not is_running
    state = "started" if is_running else "stopped"
    logging.info(f"Bot {state}")
    print(f"Bot {state}")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    is_running = False
    kills = 0
    
    keyboard.on_press_key('z', lambda _: toggle_bot())
    
    config = load_config()
    print("Bot ready! Press Z to start/stop, move mouse to corner to exit.")
    hunt(config)