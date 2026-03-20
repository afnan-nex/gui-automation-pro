# GUI Automation Examples & Workbook

Complete working examples for real-world automation tasks.

---

## 📝 Example 1: Open Notepad, Type, and Save

```python
import pyautogui, pytesseract, subprocess, time

# Step 1: Open Run dialog
pyautogui.hotkey('win', 'r')
time.sleep(1)

# Step 2: Type 'notepad' using clipboard
subprocess.run(['clip'], input=b'notepad', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

# Step 3: Type content
subprocess.run(['clip'], input='Hello World!\nThis is automated.'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.5)

# Step 4: Save file (Ctrl+S)
pyautogui.hotkey('ctrl', 's')
time.sleep(1)

# Step 5: Type filename in Save dialog
subprocess.run(['clip'], input='automation_test.txt'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(1)

print('✓ File saved successfully!')
```

---

## 🌐 Example 2: Open Browser and Search

```python
import pyautogui, pytesseract, subprocess, time
from PIL import Image

# Step 1: Open Firefox
pyautogui.hotkey('win', 'r')
time.sleep(1)
subprocess.run(['clip'], input=b'firefox', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(4)  # Wait for browser to load

# Step 2: Navigate to Google
pyautogui.hotkey('ctrl', 'l')  # Focus address bar
time.sleep(0.5)
subprocess.run(['clip'], input=b'google.com', check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(3)

# Step 3: Scan screen to find search box
img = pyautogui.screenshot()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

search_box_found = False
for i, text in enumerate(data['text']):
    if 'search' in text.lower() and int(data['conf'][i]) > 60:
        x = data['left'][i] + data['width'][i] // 2
        y = data['top'][i] + data['height'][i] // 2
        print(f'Found search box at ({x}, {y})')
        pyautogui.click(x, y)
        search_box_found = True
        break

if not search_box_found:
    # Fallback: click center of page
    pyautogui.click(683, 400)

time.sleep(0.5)

# Step 4: Type search query
subprocess.run(['clip'], input='python automation'.encode('utf-8'), check=True)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

print('✓ Search completed!')
```

---

## 📋 Example 3: Fill a Web Form

```python
import pyautogui, pytesseract, subprocess, time

def find_and_click(target_text):
    """Helper: Find text on screen and click it"""
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    for i, text in enumerate(data['text']):
        if target_text.lower() in text.lower() and int(data['conf'][i]) > 50:
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            pyautogui.click(x, y)
            return True
    return False

def type_in_field(value):
    """Helper: Type using clipboard"""
    subprocess.run(['clip'], input=value.encode('utf-8'), check=True)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

# Form data
form_data = {
    'First Name': 'John',
    'Last Name': 'Doe',
    'Email': 'john.doe@example.com',
    'Phone': '555-1234',
    'Country': 'United States'
}

# Fill each field
for label, value in form_data.items():
    print(f'Filling: {label}')
    if find_and_click(label):
        type_in_field(value)
        time.sleep(0.5)
    else:
        print(f'✗ Could not find field: {label}')

# Submit form
time.sleep(1)
if find_and_click('Submit'):
    print('✓ Form submitted!')
else:
    print('✗ Could not find Submit button')
```

---

## 🔍 Example 4: Screenshot & Analyze Screen

```python
import pyautogui, pytesseract
from PIL import Image

def print_screen_analysis():
    """Detailed analysis of current screen"""
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    print('\n' + '='*80)
    print('SCREEN ANALYSIS')
    print('='*80)
    
    # Count elements by confidence
    high_conf = 0
    med_conf = 0
    low_conf = 0
    
    print(f'\n{"TEXT":<40} {"POSITION":<15} {"CONFIDENCE":<12} {"SIZE":<10}')
    print('-'*80)
    
    for i, text in enumerate(data['text']):
        if text.strip():
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            conf = int(data['conf'][i])
            width = data['width'][i]
            height = data['height'][i]
            
            if conf >= 70:
                high_conf += 1
            elif conf >= 50:
                med_conf += 1
            else:
                low_conf += 1
            
            print(f'{text:<40} ({x:4d},{y:4d})  {conf:3d}%      {width}x{height}')
    
    print('-'*80)
    print(f'High Confidence (70+): {high_conf}')
    print(f'Medium Confidence (50-69): {med_conf}')
    print(f'Low Confidence (<50): {low_conf}')
    print('='*80 + '\n')
    
    # Save screenshot
    img.save('screen_analysis.png')
    print('✓ Screenshot saved as screen_analysis.png')

# Run analysis
print_screen_analysis()
```

---

## 🎯 Example 5: Click-By-Text with Retry Logic

```python
import pyautogui, pytesseract, time

def click_with_retry(target_text, max_retries=3, confidence_threshold=50, wait_time=1):
    """
    Robust click function with retry logic
    Returns: True if successful, False if all retries failed
    """
    for attempt in range(max_retries):
        print(f'Attempt {attempt + 1}/{max_retries}: Looking for "{target_text}"')
        
        img = pyautogui.screenshot()
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Search for target text
        for i, text in enumerate(data['text']):
            if (target_text.lower() in text.lower() and 
                int(data['conf'][i]) > confidence_threshold):
                
                x = data['left'][i] + data['width'][i] // 2
                y = data['top'][i] + data['height'][i] // 2
                conf = int(data['conf'][i])
                
                print(f'  ✓ Found "{text}" at ({x}, {y}) [confidence: {conf}%]')
                pyautogui.click(x, y)
                time.sleep(wait_time)
                return True
        
        # Not found, wait before retry
        if attempt < max_retries - 1:
            print(f'  ✗ Not found, retrying in 1s...')
            time.sleep(1)
    
    print(f'  ✗ Failed to find "{target_text}" after {max_retries} attempts')
    return False

# Example usage
click_with_retry('Search', max_retries=3, wait_time=2)
click_with_retry('Submit', max_retries=2, wait_time=1.5)
```

---

## 🪟 Example 6: Window Management

```python
import pygetwindow as gw
import pyautogui
import time

def list_windows():
    """List all open windows"""
    windows = gw.getAllWindows()
    print(f'\nOpen Windows ({len(windows)} total):')
    for i, win in enumerate(windows, 1):
        if win.title:
            print(f'{i:2d}. {win.title}')

def switch_to_application(app_name):
    """Switch focus to an application"""
    wins = gw.getWindowsWithTitle(app_name)
    if wins:
        win = wins[0]
        win.activate()
        time.sleep(0.5)
        print(f'✓ Switched to: {win.title}')
        return True
    else:
        print(f'✗ Application not found: {app_name}')
        list_windows()
        return False

def resize_window(app_name, width, height):
    """Resize a window to specific dimensions"""
    wins = gw.getWindowsWithTitle(app_name)
    if wins:
        win = wins[0]
        win.resizeTo(width, height)
        print(f'✓ Resized {win.title} to {width}x{height}')
        return True
    return False

# Example usage
list_windows()
time.sleep(1)

switch_to_application('Notepad')
time.sleep(1)

resize_window('Notepad', 800, 600)
time.sleep(1)

switch_to_application('Chrome')
```

---

## 🎮 Example 7: Complex Workflow - Multi-Step Task

```python
import pyautogui, pytesseract, subprocess, time

def multi_step_automation():
    """
    Complete workflow:
    1. Open Excel
    2. Create new spreadsheet
    3. Enter data
    4. Save file
    """
    
    print('Starting multi-step automation...\n')
    
    # Step 1: Open Excel
    print('Step 1: Opening Excel...')
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    subprocess.run(['clip'], input=b'excel', check=True)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(3)
    
    # Step 2: Create new blank workbook
    print('Step 2: Creating new workbook...')
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    # Look for "Blank workbook" or similar
    for i, text in enumerate(data['text']):
        if 'blank' in text.lower() and int(data['conf'][i]) > 50:
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            pyautogui.click(x, y)
            break
    
    time.sleep(2)
    
    # Step 3: Enter data in cells
    print('Step 3: Entering data...')
    data_to_enter = ['Name', 'Age', 'City']
    
    for item in data_to_enter:
        subprocess.run(['clip'], input=item.encode('utf-8'), check=True)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')  # Move to next cell
        time.sleep(0.3)
    
    # Step 4: Save file
    print('Step 4: Saving file...')
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    
    subprocess.run(['clip'], input='automation_data.xlsx'.encode('utf-8'), check=True)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(1)
    
    print('✓ Workflow completed!\n')

# Run the workflow
# multi_step_automation()
```

---

## 📊 Example 8: Extract Data from Screen

```python
import pyautogui, pytesseract

def extract_table_data(region=None):
    """
    Extract structured text from screen (useful for table data)
    region: Optional tuple (left, top, right, bottom) to limit extraction area
    """
    img = pyautogui.screenshot()
    
    if region:
        left, top, right, bottom = region
        img = img.crop((left, top, right, bottom))
    
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    results = []
    for i, text in enumerate(data['text']):
        if text.strip():
            y = data['top'][i]
            results.append({
                'text': text,
                'x': data['left'][i],
                'y': y,
                'width': data['width'][i],
                'height': data['height'][i],
                'confidence': int(data['conf'][i])
            })
    
    # Sort by row (y position) then column (x position)
    results.sort(key=lambda r: (r['y'], r['x']))
    
    return results

def print_extracted_data():
    """Display extracted data"""
    data = extract_table_data()
    
    print('\n' + '='*80)
    print('EXTRACTED DATA')
    print('='*80)
    
    current_row = None
    for item in data:
        if current_row != item['y']:
            current_row = item['y']
            print()  # New row
        
        print(f"{item['text']:<20}", end=' ')
    
    print('\n' + '='*80)

# Usage
# print_extracted_data()
```

---

## 🔧 Example 9: Keyboard Input Techniques

```python
import pyautogui, subprocess, time

# Technique 1: Clipboard (Best for special characters)
def input_via_clipboard(text):
    subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
    pyautogui.hotkey('ctrl', 'v')
    print(f'✓ Typed via clipboard: {text}')

# Technique 2: Direct typing (Works everywhere but slow)
def input_via_typewrite(text):
    pyautogui.typewrite(text, interval=0.05)
    print(f'✓ Typed via keyboard: {text}')

# Technique 3: Line-by-line input
def input_multiline(lines):
    for line in lines:
        input_via_clipboard(line)
        pyautogui.press('enter')
        time.sleep(0.2)
    print(f'✓ Typed {len(lines)} lines')

# Example usage
# input_via_clipboard('Hello! Special chars: é@#$%')
# input_via_typewrite('simple text')
# input_multiline(['Line 1', 'Line 2', 'Line 3'])
```

---

## ⏱️ Example 10: Timing & Synchronization

```python
import pyautogui, pytesseract, time
from PIL import ImageChops

def wait_for_element(target_text, timeout=10, check_interval=0.5):
    """Wait for an element to appear on screen"""
    start = time.time()
    
    while time.time() - start < timeout:
        img = pyautogui.screenshot()
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        for i, text in enumerate(data['text']):
            if target_text.lower() in text.lower():
                elapsed = time.time() - start
                print(f'✓ Element found after {elapsed:.1f}s')
                return True
        
        time.sleep(check_interval)
    
    print(f'✗ Element not found within {timeout}s timeout')
    return False

def wait_for_screen_change(timeout=10, sample_delay=0.5):
    """Wait until screen content changes"""
    initial = pyautogui.screenshot()
    start = time.time()
    
    while time.time() - start < timeout:
        current = pyautogui.screenshot()
        
        # Compare images
        diff = ImageChops.difference(initial, current)
        if diff.getbbox():  # If there's any difference
            elapsed = time.time() - start
            print(f'✓ Screen changed after {elapsed:.1f}s')
            return True
        
        time.sleep(sample_delay)
    
    print(f'✗ Screen did not change within {timeout}s')
    return False

# Example usage
# wait_for_element('Loading...', timeout=5)
# wait_for_screen_change(timeout=10)
```

---

## 🚀 Quick Template for New Tasks

Use this template to build new automation:

```python
import pyautogui, pytesseract, subprocess, time

# Configuration
STEP_DELAY = 1.0        # Seconds between steps
CLICK_CONFIDENCE = 50   # OCR confidence threshold for clicking

def automation_task():
    """Your automation task"""
    
    # STEP 1: Prepare
    print('Step 1: [Description]')
    time.sleep(STEP_DELAY)
    
    # STEP 2: Scan screen
    print('Step 2: Scanning screen...')
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    # STEP 3: Find and click element
    print('Step 3: Clicking element...')
    for i, text in enumerate(data['text']):
        if 'target' in text.lower() and int(data['conf'][i]) > CLICK_CONFIDENCE:
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            pyautogui.click(x, y)
            break
    
    time.sleep(STEP_DELAY)
    
    # STEP 4: Type input
    print('Step 4: Entering data...')
    subprocess.run(['clip'], input='your input'.encode('utf-8'), check=True)
    pyautogui.hotkey('ctrl', 'v')
    
    time.sleep(STEP_DELAY)
    
    # STEP 5: Final action
    print('Step 5: Completing task...')
    pyautogui.press('enter')
    
    print('✓ Task completed!')

# Run it
# automation_task()
```

---

## ✅ Checklist Before Running

- [ ] Tesseract OCR installed
- [ ] Required packages installed (`pip install ...`)
- [ ] Screen resolution detected correctly
- [ ] No full-screen exclusive apps running
- [ ] Enough time delays between actions
- [ ] Error handling for missing elements
- [ ] Test with one step at a time first

