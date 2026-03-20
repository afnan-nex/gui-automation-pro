# 🚀 GUI Automation Pro - Getting Started (5-Minute Quick Start)

## The 3-Step Workflow (Always!)

```
┌──────────────────────────────────────────────┐
│  1. SCAN SCREEN                              │
│  (Read all visible text with coordinates)    │
├──────────────────────────────────────────────┤
│  2. LOCATE TARGET                            │
│  (Find your element in the scan output)      │
├──────────────────────────────────────────────┤
│  3. CLICK/INTERACT                           │
│  (Use Method 1-4 based on element type)      │
└──────────────────────────────────────────────┘
```

---

## Step 1️⃣ — SCAN THE SCREEN

**Goal:** Find all visible text and their exact coordinates

```python
import pyautogui, pytesseract

img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        conf = int(data['conf'][i])
        print(f'[{text}] @ ({x}, {y}) [{conf}%]')
```

**Output Example:**
```
[Google] @ (683, 150) [95%]
[Search] @ (683, 400) [88%]
[Gmail] @ (100, 50) [92%]
[Sign in] @ (1200, 30) [90%]
```

✅ You now know exactly where every element is!

---

## Step 2️⃣ — LOCATE YOUR TARGET

Look at the scan output and find your target element.

**Example:** Want to click "Sign in"?
- From scan: `[Sign in] @ (1200, 30) [90%]`
- **Coordinates:** (1200, 30)
- **Confidence:** 90% (good!)

---

## Step 3️⃣ — CLICK/INTERACT

Choose the best method:

### 🥇 METHOD 1: Click by Text (BEST - Try This First!)
```python
import pyautogui, pytesseract

img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

for i, text in enumerate(data['text']):
    if 'Sign in' in text and int(data['conf'][i]) > 50:  # ← Your target
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        pyautogui.click(x, y)
        break
```

✅ **When:** Buttons, links, labels (anything readable)  
✅ **Why:** Works even if layout changes  
✅ **Reliability:** 95%+ when confidence > 60%

---

### 🥈 METHOD 2: Click by Image (Icons)
```python
import pyautogui, cv2, numpy as np

img = pyautogui.screenshot()
img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

template = cv2.imread('icon.png', 0)  # ← Your icon reference
res = cv2.matchTemplate(img_np, template, cv2.TM_CCOEFF_NORMED)
_, conf, _, loc = cv2.minMaxLoc(res)

if conf > 0.75:
    h, w = template.shape
    cx, cy = loc[0] + w//2, loc[1] + h//2
    pyautogui.click(cx, cy)
```

✅ **When:** Toolbar icons, images without text  
✅ **Why:** Precise visual matching  
✅ **Reliability:** 90%+ when confidence > 0.75

---

### 🥉 METHOD 3: Activate Window (Window Management)
```python
import pygetwindow as gw
import time

wins = gw.getWindowsWithTitle('Notepad')  # ← Your app name
if wins:
    wins[0].activate()  # Bring it to focus
    time.sleep(0.5)
```

✅ **When:** Managing windows, ensuring focus  
✅ **Why:** App needs to be active before clicking  
✅ **Reliability:** 100%

---

### ⚠️ METHOD 4: Raw Coordinates (Last Resort)
```python
import pyautogui

pyautogui.click(683, 384)  # ← Known coordinates
```

✅ **When:** Fixed, unchanging positions  
✅ **Why:** Simple and direct  
✅ **Reliability:** 100% (if coords stay same)

---

## ⌨️ QUICK TASK: Type Text

```python
import subprocess, pyautogui

# Method A: Clipboard (works with special chars!)
subprocess.run(['clip'], input='Your text'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')

# Method B: Direct typing (slow)
pyautogui.typewrite('hello', interval=0.05)
```

---

## ⏱️ CRITICAL: Add Delays

After every interaction, wait for the screen to respond:

```python
import time

pyautogui.click(683, 384)   # Click button
time.sleep(0.5)             # Wait for response

pyautogui.typewrite('text')  # Type
time.sleep(0.3)             # Wait

pyautogui.press('enter')    # Submit
time.sleep(2)               # Wait for page load
```

**Timing Guide:**
| Action | Delay |
|--------|-------|
| Text appears | 0.3s |
| Type in field | 0.5s |
| Button click | 0.5-1s |
| Window opens | 1-2s |
| Page loads | 2-3s |
| Heavy operation | 3-5s |

---

## 🎯 COMPLETE EXAMPLE: Open & Search

```python
import pyautogui, pytesseract, subprocess, time

# 1. SCAN
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print('=== ELEMENTS ON SCREEN ===')
for i, text in enumerate(data['text']):
    if text.strip():
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'[{text}] @ ({x}, {y})')

# 2. OPEN FIREFOX
pyautogui.hotkey('win', 'r')
time.sleep(1)
subprocess.run(['clip'], input=b'firefox', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(4)

# 3. NAVIGATE & SEARCH
pyautogui.hotkey('ctrl', 'l')  # Focus address bar
time.sleep(0.5)
subprocess.run(['clip'], input=b'google.com', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

# 4. SCAN FOR SEARCH BOX
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
for i, text in enumerate(data['text']):
    if 'search' in text.lower() and int(data['conf'][i]) > 50:
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        pyautogui.click(x, y)
        break

time.sleep(0.5)

# 5. TYPE SEARCH QUERY
subprocess.run(['clip'], input=b'python automation', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

print('✓ Search completed!')
```

---

## 🛑 STOP! Before You Code...

### ❌ DON'T
- ❌ Skip the initial screen scan
- ❌ Click without checking coordinates
- ❌ Forget delays between actions
- ❌ Save .py files (use `python -c` only)

### ✅ DO
- ✅ Scan first, always
- ✅ Find exact coordinates from OCR
- ✅ Add 1-2 second delays
- ✅ Test one step at a time

---

## 📦 Setup (One-Time Only)

### 1. Install Python Packages
```bash
pip install pyautogui pytesseract opencv-python pygetwindow pillow
```

### 2. Install Tesseract OCR
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Windows: Run `tesseract-ocr-w64-setup-v5.x.x.exe`
- Choose default location: `C:\Program Files\Tesseract-OCR`

### 3. Verify
```bash
tesseract --version
python -c "import pyautogui, pytesseract; print('Ready!')"
```

---

## 🔑 KEY INSIGHT

**Your screen has coordinates.**

Every pixel on your 1366×768 screen has an (X, Y) coordinate:

```
(0, 0) ────────────── (1366, 0)
  │                      │
  │                      │
  │                      │
(0, 768) ────────── (1366, 768)
```

**OCR finds text → tells you coordinates → you click there.**

That's it! 🎯

---

## 📚 Next Steps

1. **Read:** `quick-reference.md` (for snippets)
2. **Try:** Run Example 1 (Notepad)
3. **Learn:** Read `SKILL.md` (full documentation)
4. **Build:** Use `helpers.py` (reusable functions)
5. **Create:** Write your automation task

---

## 🆘 Help!

| Problem | Solution |
|---------|----------|
| "Element not found" | Print scan output, check confidence |
| "Click didn't work" | Add longer delay, activate window first |
| "Text is blurry" | Increase screen resolution or font size |
| "Special characters fail" | Use clipboard method, not typewrite |
| "Window not detected" | Print `gw.getAllWindows()` to list them |

---

## ⚡ TL;DR

1. **Scan** → `pyautogui.screenshot()` + OCR
2. **Locate** → Read OCR output for coordinates
3. **Click** → `pyautogui.click(x, y)`
4. **Wait** → `time.sleep(1)`
5. **Repeat** → Go back to step 1

**That's GUI automation!** 🚀

