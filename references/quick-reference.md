# GUI Automation Quick Reference

## 🚀 QUICK START

### Always Start With: SCAN THE SCREEN
```python
import pyautogui, pytesseract
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'[{text}] -> ({x}, {y})')
```

---

## 📍 FIND & CLICK BY TEXT (Most Reliable)

```python
# Quick version
import pyautogui, pytesseract
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
target = 'Submit Button'
for i, text in enumerate(data['text']):
    if target.lower() in text.lower() and int(data['conf'][i]) > 50:
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        pyautogui.click(x, y)
        break
```

---

## ⌨️ TYPE TEXT SAFELY

```python
import subprocess, pyautogui
# Method 1: Clipboard (works with special characters)
subprocess.run(['clip'], input='Your text'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')

# Method 2: Keyboard (slow but simple)
pyautogui.typewrite('hello', interval=0.05)
```

---

## 🪟 WINDOW MANAGEMENT

```python
import pygetwindow as gw
import time

# Activate window
wins = gw.getWindowsWithTitle('Notepad')
if wins:
    wins[0].activate()
    time.sleep(0.5)

# Maximize
wins[0].maximize()

# List all windows
print([w.title for w in gw.getAllWindows()])
```

---

## 🖱️ MOUSE ACTIONS

```python
import pyautogui, time

# Click
pyautogui.click(683, 384)

# Double-click
pyautogui.click(683, 384)
pyautogui.click(683, 384)

# Right-click
pyautogui.click(683, 384, button='right')

# Move mouse
pyautogui.moveTo(683, 384)

# Scroll
pyautogui.scroll(5)      # Scroll up
pyautogui.scroll(-5)     # Scroll down
```

---

## ⌨️ KEYBOARD SHORTCUTS

```python
import pyautogui

pyautogui.hotkey('ctrl', 'a')      # Select all
pyautogui.hotkey('ctrl', 'c')      # Copy
pyautogui.hotkey('ctrl', 'v')      # Paste
pyautogui.hotkey('ctrl', 's')      # Save
pyautogui.hotkey('ctrl', 'z')      # Undo
pyautogui.hotkey('ctrl', 'y')      # Redo
pyautogui.hotkey('ctrl', 'x')      # Cut
pyautogui.hotkey('ctrl', 'f')      # Find
pyautogui.hotkey('alt', 'tab')     # Switch window
pyautogui.hotkey('win', 'd')       # Show desktop
pyautogui.hotkey('win', 'r')       # Run dialog

pyautogui.press('enter')           # Press Enter
pyautogui.press('backspace')       # Backspace
pyautogui.press('delete')          # Delete
pyautogui.press('tab')             # Tab
pyautogui.press('escape')          # Escape
```

---

## 🖼️ IMAGE MATCHING (For Icons)

```python
import pyautogui, cv2, numpy as np

img = pyautogui.screenshot()
img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

template = cv2.imread('C:\\path\\to\\icon.png', 0)
res = cv2.matchTemplate(img_np, template, cv2.TM_CCOEFF_NORMED)
_, confidence, _, loc = cv2.minMaxLoc(res)

if confidence > 0.75:
    h, w = template.shape
    cx, cy = loc[0] + w//2, loc[1] + h//2
    pyautogui.click(cx, cy)
```

---

## 🔍 ADVANCED: REGION SCANNING

```python
import pyautogui, pytesseract
from PIL import Image

# Scan only left half of screen
img = pyautogui.screenshot()
region = img.crop((0, 0, 683, 768))

data = pytesseract.image_to_data(region, output_type=pytesseract.Output.DICT)
for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'[{text}] -> ({x}, {y})')
```

---

## 📋 FORM FILLING TEMPLATE

```python
import pyautogui, pytesseract, subprocess, time

def fill_form_field(label, value):
    """Click on a field by label and fill it"""
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    # Find the label
    for i, text in enumerate(data['text']):
        if label.lower() in text.lower():
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            pyautogui.click(x, y)
            time.sleep(0.5)
            
            # Type the value
            subprocess.run(['clip'], input=value.encode('utf-8'), check=True)
            pyautogui.hotkey('ctrl', 'v')
            return True
    
    return False

# Use it
fill_form_field('First Name', 'John')
fill_form_field('Email', 'john@example.com')
fill_form_field('Password', 'SecurePass123')
```

---

## ⏱️ TIMING & DELAYS

```python
import time

# After clicking button, wait for dialog
time.sleep(1)

# After typing, wait for validation
time.sleep(0.5)

# After page load
time.sleep(2)

# General guideline:
# - 0.3s: Quick UI response
# - 0.5s: Form input
# - 1.0s: Window opens/closes
# - 2.0s: Page loads
# - 3.0s: Heavy operations
```

---

## 🔴 ERROR HANDLING

```python
import pyautogui, pytesseract, time

def safe_click(target_text, max_attempts=3, wait=1):
    """Try to click with retries"""
    for attempt in range(max_attempts):
        img = pyautogui.screenshot()
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        for i, text in enumerate(data['text']):
            if target_text.lower() in text.lower() and int(data['conf'][i]) > 50:
                x = data['left'][i] + data['width'][i] // 2
                y = data['top'][i] + data['height'][i] // 2
                pyautogui.click(x, y)
                time.sleep(wait)
                return True
        
        print(f'Attempt {attempt+1} failed, retrying...')
        time.sleep(0.5)
    
    print(f'Failed to find: {target_text}')
    return False

# Use it
safe_click('Save', max_attempts=3, wait=2)
```

---

## 🎯 COMPLETE WORKFLOW EXAMPLE

**Task: Open Firefox, go to Google, search for "automation"**

```python
import pyautogui, pytesseract, subprocess, time

# 1. Open Firefox
pyautogui.hotkey('win', 'r')
time.sleep(1)
subprocess.run(['clip'], input=b'firefox', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(3)  # Wait for browser to load

# 2. Scan to find address bar
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print('=== SCREEN ===')
for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'[{text}] -> ({x}, {y})')

# 3. Click address bar and type URL
pyautogui.click(683, 70)  # Address bar (approximate)
time.sleep(0.5)
subprocess.run(['clip'], input=b'google.com', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

# 4. Search for "automation"
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

# Find search box
for i, text in enumerate(data['text']):
    if 'search' in text.lower():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        pyautogui.click(x, y)
        time.sleep(0.5)
        break

# Type search query
subprocess.run(['clip'], input=b'automation', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

print('✓ Complete!')
```

---

## 🛠️ DEBUGGING TIPS

1. **Print every element**: Always scan and print all visible text
2. **Check confidence**: Look for OCR confidence scores > 60%
3. **Take screenshots**: Use `img.save()` to compare before/after
4. **Add delays**: When in doubt, add more `time.sleep()`
5. **Window focus**: Always activate window first with `win.activate()`
6. **Verify actions**: After each action, scan the screen again

---

## 📦 INSTALLATION

```bash
# Install dependencies
pip install pyautogui pytesseract opencv-python pygetwindow pillow

# Install Tesseract (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Then add to PATH or configure in code:

import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## ⚠️ CRITICAL RULES

✅ DO:
- Scan before every action
- Use text clicking (most reliable)
- Add delays after UI changes
- Handle missing elements gracefully

❌ DON'T:
- Save .py files (use `python -c` only)
- Skip screen scanning
- Assume coordinates without verification
- Forget delays between actions

