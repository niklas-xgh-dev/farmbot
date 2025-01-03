# Farmbot

Automated bot that finds and clicks monsters by detecting their health bar color. Can be repurposed for different MMORPGs.

## Setup & Usage

1. **Install dependencies:**
```bash
pip install pyautogui pillow pyyaml
```

2. **Find coordinates with coordinate_finder.py:**
```python
import pyautogui
import keyboard
from PIL import ImageGrab

def get_pixel_color(x, y):
    screen = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    return screen.getpixel((0, 0))

print("Press 'p' for coordinates/RGB, 'q' to quit")

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
```

3. **Configure config.yaml:**
```yaml
target_color: [227, 114, 112]  # Health bar RGB from coordinate_finder
target_position: [1837, 102]   # Health bar position
scan_area: [250, 280, 3642, 1829]  # [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
color_tolerance: 100
sample_size: 5
scan_step: 150
```

4. **Run main.py to start bot:**
```bash
python main.py
```

## Features

- Detects health bar by RGB color
- Random mouse movement in defined scan area
- Random WASD movements
- Auto-presses '8' every 21 seconds
- Failsafe: Move cursor to screen corner to stop
- Activity logging to monster_hunter.log

## Files

- `coordinate_finder.py`: Tool to get screen coordinates and RGB values
- `config.yaml`: Bot configuration
- `main.py`: Main bot script
- `requirements.txt`: Python dependencies