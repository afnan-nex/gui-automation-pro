---
name: gui-automation-pro
description: Windows PC GUI automation with precise visual element detection. Use this skill whenever you need to automate Windows applications, click on UI elements, type text, navigate windows, extract screen information, interact with web browsers, or control desktop applications. This includes filling forms, navigating windows, taking screenshots, detecting text/buttons/images, clicking coordinates, typing input, and automating repetitive GUI tasks. Always use this skill for any Windows desktop automation task that requires screen scanning, element detection, or user interface interaction.
compatibility: Windows 10/11, Python 3.8+, pyautogui, pytesseract, opencv-python, pygetwindow, Tesseract OCR
---

# Windows GUI Automation Pro

A comprehensive skill for automating Windows PC applications with precise visual element detection and intelligent interaction methods.

## CORE CAPABILITIES

### 1. **Screen Scanning & OCR**
Capture the entire screen and extract all visible text with exact pixel coordinates using Tesseract OCR.

```python
import pyautogui, pytesseract
from PIL import Image

img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print('=== VISIBLE TEXT ON SCREEN ===')
for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        conf = int(data['conf'][i])
        print(f'  [{text}] -> ({x}, {y}) [confidence: {conf}%]')
```

**Use this before every action** to locate elements precisely.

### 2. **Smart Element Clicking - Priority Order**

#### ✅ **METHOD 1: Click by Text (MOST RELIABLE)**
Find and click any button, link, or text element by its visible text content.

```python
import pyautogui, pytesseract

img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
target = 'Submit'  # Replace with target text
found = False

for i, text in enumerate(data['text']):
    if target.lower() in text.lower() and int(data['conf'][i]) > 50:
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'Clicking [{text}] at ({x}, {y})')
        pyautogui.click(x, y)
        found = True
        break

if not found:
    print(f'NOT FOUND: {target}')
```

**When to use:** Buttons, links, menu items, labels, any clickable text element.

#### ✅ **METHOD 2: Click by Image Template (Icons & Complex Elements)**
Match a reference image to find and click visual elements like icons.

```python
import pyautogui, cv2, numpy as np

img = pyautogui.screenshot()
img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

# Load your reference icon/template image
template = cv2.imread(r'C:\path\to\icon.png', 0)
res = cv2.matchTemplate(img_np, template, cv2.TM_CCOEFF_NORMED)
_, confidence, _, loc = cv2.minMaxLoc(res)

if confidence > 0.75:
    h, w = template.shape
    cx, cy = loc[0] + w//2, loc[1] + h//2
    print(f'Found icon at ({cx},{cy}) confidence={confidence:.2f}')
    pyautogui.click(cx, cy)
else:
    print(f'Icon not found. Best match: {confidence:.2f}')
```

**When to use:** Icons, toolbar buttons, images without text.

#### ✅ **METHOD 3: Window Focus & Interaction**
Activate and manage application windows by name.

```python
import pygetwindow as gw
import time

# Get window by title
wins = gw.getWindowsWithTitle('Notepad')
if wins:
    win = wins[0]
    win.activate()
    win.maximize()  # or win.resizeTo(1366, 768) and win.moveTo(0, 0)
    time.sleep(0.5)
    print(f'Activated: {win.title}')
else:
    print('Window not found. Available:', [w.title for w in gw.getAllWindows()])
```

**When to use:** Switching between windows, maximizing/minimizing, managing window position.

#### ✅ **METHOD 4: Raw Coordinates (Last Resort)**
Click a known coordinate directly (use only if other methods fail).

```python
import pyautogui
pyautogui.click(683, 384)  # Center of 1366x768 screen
```

---

## KEYBOARD INPUT & SHORTCUTS

### Type Text (Slow, Character-by-Character)
```python
import pyautogui
pyautogui.typewrite('hello world', interval=0.05)
```

### Type Text (Fast, Using Clipboard)
```python
import pyautogui, subprocess
text = "Your text here with special chars!"
subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')  # Paste
```

### Common Keyboard Shortcuts
```python
import pyautogui

pyautogui.hotkey('ctrl', 'a')      # Select All
pyautogui.hotkey('ctrl', 'c')      # Copy
pyautogui.hotkey('ctrl', 'v')      # Paste
pyautogui.hotkey('ctrl', 's')      # Save
pyautogui.hotkey('ctrl', 'z')      # Undo
pyautogui.hotkey('alt', 'tab')     # Switch window
pyautogui.hotkey('win', 'd')       # Show desktop
pyautogui.hotkey('win', 'r')       # Run dialog
pyautogui.press('enter')           # Press Enter
pyautogui.press('delete')          # Press Delete
pyautogui.press('backspace')       # Press Backspace
```

### Scroll & Mouse Movement
```python
import pyautogui
import time

# Scroll down 5 units
pyautogui.scroll(-5)

# Scroll up 5 units
pyautogui.scroll(5)

# Move mouse to coordinate
pyautogui.moveTo(683, 384)
time.sleep(0.3)

# Double-click
pyautogui.click(683, 384)
pyautogui.click(683, 384)

# Right-click
pyautogui.click(683, 384, button='right')
```

---

## CRITICAL EXECUTION RULES

### ✅ ALWAYS DO THIS
1. **SCAN FIRST** — Run OCR to read the screen before every action
2. **LOCATE TARGET** — Find your element in the OCR output
3. **CHOOSE METHOD** — Pick the best clicking method (text → image → window → coordinates)
4. **ADD DELAY** — Use `time.sleep(1)` after UI changes, window opens, or page loads
5. **EXECUTE** — Use `python -c "..."` inline only (never save .py files)
6. **REPEAT** — Scan again before the next action

### ✅ EXECUTION TEMPLATE
Every automation follows this structure:

```python
import pyautogui, pytesseract, time
from PIL import Image

# STEP 1: SCAN
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print('=== SCREEN SCAN ===')
for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'  [{text}] -> ({x}, {y})')

# STEP 2: FIND TARGET (from scan output)
# [Use scan output to identify exact coordinates]

# STEP 3: CLICK/INTERACT
# [Choose Method 1-4 and execute]
pyautogui.click(target_x, target_y)
time.sleep(1)  # Wait for UI response

# STEP 4: NEXT ACTION (return to Step 1)
```

### ❌ NEVER DO THIS
- ❌ Create or save .py files to disk
- ❌ Skip the initial screen scan
- ❌ Assume coordinates without scanning
- ❌ Click without verifying element exists first
- ❌ Forget `time.sleep()` after UI transitions

---

## MULTI-STEP AUTOMATION EXAMPLE

**Task:** Open Notepad, type "Hello World", save as test.txt

```python
import pyautogui, pytesseract, time, subprocess
from PIL import Image

# Step 1: Open Notepad via Run Dialog
pyautogui.hotkey('win', 'r')
time.sleep(1)

# Scan to verify Run dialog opened
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print('Run dialog opened')

# Type 'notepad' and press Enter
subprocess.run(['clip'], input=b'notepad', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

# Step 2: Type text using clipboard
subprocess.run(['clip'], input='Hello World'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

# Step 3: Save file
pyautogui.hotkey('ctrl', 's')
time.sleep(1)

# Scan to find "Save As" dialog
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

# Type filename
subprocess.run(['clip'], input='test.txt'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(1)

print('✓ File saved successfully')
```

---

## SCREEN CONFIGURATION

- **Resolution:** 1366 × 768 pixels
- **Valid X Range:** 0–1366
- **Valid Y Range:** 0–768
- **Screen Center:** (683, 384)
- **Coordinates:** (X, Y) where X increases right, Y increases down

---

## TROUBLESHOOTING

### Issue: OCR returns empty or gibberish
- **Solution:** Application text might be too small or using non-standard fonts
- Try Method 3 (window focus) or Method 2 (image templates)
- Increase screen resolution if possible

### Issue: Can't find target text in OCR output
- **Solution:** Text might be partially visible, off-screen, or low confidence
- Check OCR confidence values (aim for >60%)
- Scroll window and scan again
- Use partial text matching: `if 'Sub' in text` instead of exact match

### Issue: Click registers but nothing happens
- **Solution:** Window might not have focus
- Use Method 3 first: `win.activate()`
- Add longer `time.sleep()` delays between actions (try 2 seconds)
- Verify window is fully loaded before clicking

### Issue: Image template matching fails
- **Ensure reference image is:**
  - Clear and high contrast
  - Similar size to on-screen element
  - Not rotated or scaled differently
  - Saved as .png with transparency if needed

---

## DEPENDENCIES & SETUP

Install required packages:
```bash
pip install pyautogui pytesseract opencv-python pygetwindow pillow
```

Download Tesseract OCR (required for text detection):
- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Installation path:** Usually `C:\Program Files\Tesseract-OCR`
- **Add to PATH** or specify in code:
```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## BEST PRACTICES

1. **Always scan first** — OCR is your visual sense. Use it before every action.
2. **Use meaningful waits** — 0.5s for immediate responses, 1-2s for window opens, 2-3s for page loads
3. **Confidence matters** — Prioritize high-confidence OCR matches (>70%)
4. **Chain operations logically** — Group related clicks before adding long delays
5. **Test in isolation** — Run one step at a time during development
6. **Handle errors gracefully** — Always check if elements exist before interacting

---

## ADVANCED TECHNIQUES

### Multi-Monitor Support
```python
import pyautogui
# Get screen size
width, height = pyautogui.size()
print(f'Screen: {width}x{height}')

# Detect primary/secondary monitors
# Use absolute coordinates for clicks on secondary monitors
```

### Region-Based Scanning
```python
import pyautogui, pytesseract
from PIL import Image

# Crop to a specific region before OCR
left, top, right, bottom = 0, 0, 683, 384  # Left half
region = img.crop((left, top, right, bottom))
data = pytesseract.image_to_data(region, output_type=pytesseract.Output.DICT)
```

### Coordinate Offset Calculations
```python
# When clicking inside windows with known positions
window_x, window_y = 100, 100
element_rel_x, element_rel_y = 50, 30
absolute_x = window_x + element_rel_x
absolute_y = window_y + element_rel_y
```

---

## WHEN TO USE THIS SKILL

✅ **Use this skill for:**
- Opening applications and navigating menus
- Filling web forms and input fields
- Extracting information from applications
- Automating repetitive click-and-type tasks
- Screenshot analysis and element detection
- Window management and focus control
- Testing UI elements and workflows
- Data entry and form submission

❌ **Don't use this skill for:**
- System-level operations (use shell/terminal)
- File I/O beyond clicking file dialogs
- Code that doesn't require visual feedback
- Tasks that could be done via APIs instead

