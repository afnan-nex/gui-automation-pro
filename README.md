# 🖥️ GUI Automation Pro - Windows PC Automation Skill

A comprehensive skill for automating Windows GUI applications with **precise visual element detection** and **intelligent interaction methods**.

## ✨ Features

✅ **Screen Scanning & OCR** — Extract all visible text with exact pixel coordinates  
✅ **Smart Element Clicking** — Find and click by text (most reliable), images, or coordinates  
✅ **Window Management** — Activate, focus, maximize/minimize any application  
✅ **Text Input** — Safe typing with clipboard support for special characters  
✅ **Keyboard Shortcuts** — All common shortcuts (Ctrl+A, Ctrl+V, Alt+Tab, etc.)  
✅ **Mouse Actions** — Click, scroll, double-click, right-click, move  
✅ **Form Automation** — Fill multiple fields sequentially  
✅ **Error Handling** — Graceful fallbacks and retry logic  

---

## 🚀 Quick Start

### 1. Scan the Screen (Always First!)
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

### 2. Click by Text (Most Reliable Method)
```python
import pyautogui, pytesseract

img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

target = 'Submit'
for i, text in enumerate(data['text']):
    if target.lower() in text.lower() and int(data['conf'][i]) > 50:
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        pyautogui.click(x, y)
        break
```

### 3. Type Text Safely
```python
import subprocess, pyautogui

subprocess.run(['clip'], input='Hello World'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
```

---

## 📁 Skill Contents

```
gui-automation-pro/
├── SKILL.md                          # Main documentation (comprehensive guide)
├── references/
│   └── quick-reference.md            # Quick lookup for common tasks
└── scripts/
    └── helpers.py                    # Reusable helper functions
```

---

## 📚 Documentation Files

### **SKILL.md** — Complete Guide
- Detailed explanations of all 4 clicking methods
- Screen configuration and coordinate system
- Keyboard input techniques
- Multi-step automation workflows
- Troubleshooting guide
- Dependencies & setup instructions

**When to use:** Learning the skill, understanding all capabilities

### **quick-reference.md** — Fast Lookup
- Quick code snippets for common tasks
- Copy-paste ready examples
- Timing guidelines
- Debugging tips
- Complete workflow examples

**When to use:** Writing automation scripts, need quick syntax

### **helpers.py** — Reusable Functions
Pre-built functions for:
- `scan_screen_and_find_text()` — Find text on screen
- `click_by_text()` — Click any button/link
- `click_by_image()` — Match and click icons
- `activate_window()` — Focus applications
- `type_text_safe()` — Type with special characters
- `fill_form()` — Auto-fill multiple fields
- And 20+ more helper functions

**When to use:** Building complex automation scripts

---

## 🎯 The 4 Clicking Methods (Priority Order)

### ✅ **METHOD 1: Click by Text** (MOST RELIABLE)
Best for: Buttons, links, labels, any readable text
```python
# Find "Submit" button and click it
# Works even if button moves or window resizes
```
→ Try this first for 90% of tasks

### ✅ **METHOD 2: Click by Image** (Icon Matching)
Best for: Toolbar icons, images without text
```python
# Match reference image (template) and click the icon
# High precision for visual elements
```
→ Use for icons, thumbnails, screenshots

### ✅ **METHOD 3: Window Focus** (Application Management)
Best for: Managing application windows
```python
# Activate "Notepad" window
# Ensures correct application has focus
```
→ Always use before clicking in specific app

### ✅ **METHOD 4: Raw Coordinates** (Last Resort)
Best for: Known, fixed positions
```python
# Click at exact pixel (683, 384)
# Use only if other methods fail
```
→ Only when coordinates never change

---

## 💡 Key Concepts

### **Screen Scanning**
Every automation starts by reading the screen visually. The OCR engine (`pytesseract`) extracts:
- All visible text
- Exact pixel coordinates (x, y) of each word
- Confidence scores (0-100%)

This is your "visual sense" — always use it.

### **Coordinate System**
```
(0, 0) ──────────── (1366, 0)
  │                      │
  │    1366 × 768       │
  │                      │
(0, 768) ──────── (1366, 768)

Screen Center: (683, 384)
```

### **Element Center Calculation**
When OCR finds text, it returns:
- `left`, `top` — top-left corner
- `width`, `height` — element size
- **Center point** = `(left + width/2, top + height/2)` ← Click here!

### **Timing Guidelines**
```
0.3s  → Quick UI response (text appears)
0.5s  → After typing in form fields
1.0s  → Window opens/closes, dialog appears
2.0s  → Page loads, heavy operations
3.0s  → Very slow operations (downloads, large uploads)
```

---

## 🔧 Setup & Dependencies

### Windows 10/11 Requirements

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Required Python Packages**
   ```bash
   pip install pyautogui pytesseract opencv-python pygetwindow pillow
   ```

3. **Tesseract OCR** (Critical for text detection)
   - Download: https://github.com/UB-Mannheim/tesseract/wiki
   - Windows installer (recommended): `tesseract-ocr-w64-setup-v5.x.x.exe`
   - Install to: `C:\Program Files\Tesseract-OCR`
   - Already in PATH ✓

4. **Verify Installation**
   ```bash
   tesseract --version
   ```

---

## 📋 Common Tasks & Examples

### Open Application & Type
```python
import pyautogui, time, subprocess

pyautogui.hotkey('win', 'r')  # Run dialog
time.sleep(1)
subprocess.run(['clip'], input=b'notepad', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

# Type text
subprocess.run(['clip'], input='Hello!'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
```

### Find Button & Click
```python
import pyautogui, pytesseract

img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

for i, text in enumerate(data['text']):
    if 'search' in text.lower() and int(data['conf'][i]) > 60:
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        pyautogui.click(x, y)
        break
```

### Fill Web Form
```python
# 1. Click field 1
click_by_text('Email')  # From helper functions
type_text_safe('user@example.com')

# 2. Click field 2
click_by_text('Password')
type_text_safe('SecurePass123')

# 3. Click Submit
click_by_text('Submit')
```

### Switch Between Windows
```python
import pygetwindow as gw
import time

# List all open windows
for win in gw.getAllWindows():
    print(win.title)

# Activate specific window
wins = gw.getWindowsWithTitle('Chrome')
if wins:
    wins[0].activate()
    time.sleep(0.5)
```

---

## ⚠️ Critical Rules

### ✅ ALWAYS DO
1. **Scan the screen first** — `pyautogui.screenshot()` + OCR
2. **Locate your target** — Find exact coordinates from OCR
3. **Choose best method** — Text click > Image > Window > Coordinates
4. **Add delays** — `time.sleep()` after every UI change
5. **Execute inline** — Use `python -c "..."` (no .py file saving)

### ❌ NEVER DO
- ❌ Skip screen scanning (you'll miss elements)
- ❌ Assume coordinates without verification
- ❌ Click without checking element exists
- ❌ Forget delays (things load asynchronously)
- ❌ Save .py files to disk (breaks automation)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Element not found" | Scan screen, verify OCR output, check confidence % |
| "Click registered but nothing happens" | Window might not have focus — activate with `win.activate()` |
| "OCR returns empty" | Text might be too small, off-screen, or uses unusual font |
| "Special characters fail" | Use clipboard method instead of typewrite |
| "Tesseract not found" | Install from https://github.com/UB-Mannheim/tesseract/wiki |
| "Image match fails" | Reference image must be clear, same size, not rotated |

---

## 📊 When to Use This Skill

### ✅ Use GUI Automation Pro For
- Automating web forms (login, search, submit)
- Repetitive data entry (copy-paste jobs)
- Testing UI workflows
- Screenshot analysis and detection
- Window management and task switching
- Desktop application control
- Any task requiring visual clicking/typing

### ❌ Don't Use For
- System commands (use terminal/PowerShell)
- File I/O beyond file dialogs
- API-based tasks
- Code that doesn't need visual feedback

---

## 🎓 Learning Path

1. **Start Here** → Read `quick-reference.md` (5 minutes)
2. **Try Examples** → Run the code snippets (10 minutes)
3. **Read Full Guide** → Study `SKILL.md` (20 minutes)
4. **Use Helpers** → Integrate `helpers.py` in your scripts (5 minutes)
5. **Build Automation** → Combine all pieces for your task (varies)

---

## 📞 Support

- **Questions about screen scanning?** → See "Screen Scanning & OCR" in SKILL.md
- **How to click an element?** → See "Smart Element Clicking" in SKILL.md
- **Need code snippet?** → Check `quick-reference.md` first
- **Want helper functions?** → Use `scripts/helpers.py`
- **Setup issues?** → See "Dependencies & Setup" in SKILL.md

---

## 📄 License

This skill is provided as-is for Windows GUI automation.

---

## 🌟 Key Takeaways

- **Always scan first** — OCR is your eyes
- **Text clicking is most reliable** — Use it for 90% of tasks
- **Timing is critical** — Add delays after UI changes
- **Execute inline only** — No .py file saving
- **Test incrementally** — One step at a time

---

**Ready to automate? Start with scanning the screen, then click by text! 🚀**

