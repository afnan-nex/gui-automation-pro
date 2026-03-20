"""
GUI Automation Helper Functions
Reference script with reusable functions for common automation tasks
"""

# ============================================================================
# SCREEN SCANNING & TEXT DETECTION
# ============================================================================

def scan_screen_and_find_text(target_text, confidence_threshold=50):
    """
    Scan the screen and find a specific text element
    Returns: (x, y, confidence) or None if not found
    """
    import pyautogui, pytesseract
    
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    for i, text in enumerate(data['text']):
        if target_text.lower() in text.lower() and int(data['conf'][i]) > confidence_threshold:
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            conf = int(data['conf'][i])
            return (x, y, conf)
    
    return None


def print_all_screen_text():
    """
    Print all visible text on screen with coordinates
    Useful for debugging and understanding layout
    """
    import pyautogui, pytesseract
    
    img = pyautogui.screenshot()
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    print("\n" + "="*80)
    print("VISIBLE TEXT ON SCREEN")
    print("="*80)
    
    for i, text in enumerate(data['text']):
        if text.strip():
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            conf = int(data['conf'][i])
            width = data['width'][i]
            height = data['height'][i]
            print(f"[{text:30s}] @ ({x:4d}, {y:4d}) | Conf: {conf:3d}% | Size: {width}x{height}")
    
    print("="*80 + "\n")


def get_text_in_region(left, top, right, bottom):
    """
    Extract all text from a specific region of the screen
    Useful for focusing on a particular window or area
    """
    import pyautogui, pytesseract
    from PIL import Image
    
    img = pyautogui.screenshot()
    region = img.crop((left, top, right, bottom))
    
    data = pytesseract.image_to_data(region, output_type=pytesseract.Output.DICT)
    
    results = []
    for i, text in enumerate(data['text']):
        if text.strip():
            x = data['left'][i] + data['width'][i] // 2
            y = data['top'][i] + data['height'][i] // 2
            conf = int(data['conf'][i])
            results.append({
                'text': text,
                'x': left + x,
                'y': top + y,
                'confidence': conf
            })
    
    return results


# ============================================================================
# CLICKING & INTERACTION
# ============================================================================

def click_by_text(target_text, confidence_threshold=50, wait_after=1):
    """
    Find and click on an element by its text
    Returns: True if successful, False if not found
    """
    import pyautogui, time
    
    result = scan_screen_and_find_text(target_text, confidence_threshold)
    
    if result:
        x, y, conf = result
        print(f"✓ Clicking '{target_text}' at ({x}, {y}) [confidence: {conf}%]")
        pyautogui.click(x, y)
        if wait_after:
            time.sleep(wait_after)
        return True
    else:
        print(f"✗ Text not found: '{target_text}'")
        return False


def click_by_image(template_path, confidence_threshold=0.75, wait_after=1):
    """
    Find and click on an element by matching a reference image
    Returns: True if successful, False if not found
    """
    import pyautogui, cv2, numpy as np, time
    
    img = pyautogui.screenshot()
    img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    
    template = cv2.imread(template_path, 0)
    if template is None:
        print(f"✗ Template image not found: {template_path}")
        return False
    
    res = cv2.matchTemplate(img_np, template, cv2.TM_CCOEFF_NORMED)
    _, confidence, _, loc = cv2.minMaxLoc(res)
    
    if confidence > confidence_threshold:
        h, w = template.shape
        cx, cy = loc[0] + w//2, loc[1] + h//2
        print(f"✓ Image found at ({cx}, {cy}) [confidence: {confidence:.2%}]")
        pyautogui.click(cx, cy)
        if wait_after:
            time.sleep(wait_after)
        return True
    else:
        print(f"✗ Image not found. Best match: {confidence:.2%}")
        return False


def safe_click(x, y, wait_after=0.5, verify=False):
    """
    Click with validation and optional verification
    """
    import pyautogui, time
    
    # Check if coordinates are valid
    if not (0 <= x <= 1366 and 0 <= y <= 768):
        print(f"✗ Invalid coordinates: ({x}, {y})")
        return False
    
    print(f"→ Clicking at ({x}, {y})")
    pyautogui.click(x, y)
    
    if wait_after:
        time.sleep(wait_after)
    
    return True


# ============================================================================
# WINDOW MANAGEMENT
# ============================================================================

def activate_window(window_title):
    """
    Find and activate a window by title
    Returns: True if successful, False if not found
    """
    import pygetwindow as gw
    
    wins = gw.getWindowsWithTitle(window_title)
    
    if wins:
        win = wins[0]
        win.activate()
        print(f"✓ Activated window: {win.title}")
        return True
    else:
        available = [w.title for w in gw.getAllWindows() if w.title]
        print(f"✗ Window not found: '{window_title}'")
        print(f"Available windows: {available[:5]}")  # Show first 5
        return False


def list_all_windows():
    """
    List all currently open windows
    Useful for debugging
    """
    import pygetwindow as gw
    
    windows = gw.getAllWindows()
    print("\n" + "="*80)
    print(f"OPEN WINDOWS ({len(windows)} total)")
    print("="*80)
    
    for i, win in enumerate(windows, 1):
        if win.title:
            print(f"{i:2d}. {win.title}")
    
    print("="*80 + "\n")


def maximize_window(window_title):
    """
    Maximize a specific window
    """
    import pygetwindow as gw
    
    wins = gw.getWindowsWithTitle(window_title)
    if wins:
        wins[0].maximize()
        print(f"✓ Maximized: {wins[0].title}")
        return True
    else:
        print(f"✗ Window not found: {window_title}")
        return False


# ============================================================================
# TEXT INPUT
# ============================================================================

def type_text_safe(text, method='clipboard', interval=0.05):
    """
    Type text safely using clipboard (recommended for special characters)
    method: 'clipboard' (fast) or 'typewrite' (slow but works everywhere)
    """
    import pyautogui, subprocess, time
    
    if method == 'clipboard':
        try:
            subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
            pyautogui.hotkey('ctrl', 'v')
            print(f"✓ Typed (clipboard): {text[:50]}...")
            return True
        except Exception as e:
            print(f"✗ Clipboard paste failed: {e}")
            return False
    
    elif method == 'typewrite':
        pyautogui.typewrite(text, interval=interval)
        print(f"✓ Typed (keyboard): {text[:50]}...")
        return True
    
    return False


def clear_field_and_type(text):
    """
    Clear current field and type new text
    """
    import pyautogui
    
    pyautogui.hotkey('ctrl', 'a')  # Select all
    type_text_safe(text, method='clipboard')


# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

def keyboard_shortcut(modifier, key):
    """
    Execute a keyboard shortcut
    Examples: ('ctrl', 'a'), ('alt', 'tab'), ('win', 'd')
    """
    import pyautogui
    
    shortcuts = {
        'select_all': ('ctrl', 'a'),
        'copy': ('ctrl', 'c'),
        'paste': ('ctrl', 'v'),
        'save': ('ctrl', 's'),
        'undo': ('ctrl', 'z'),
        'redo': ('ctrl', 'y'),
        'switch_window': ('alt', 'tab'),
        'show_desktop': ('win', 'd'),
        'run_dialog': ('win', 'r'),
        'cut': ('ctrl', 'x'),
        'find': ('ctrl', 'f'),
        'replace': ('ctrl', 'h'),
    }
    
    if isinstance(modifier, str) and modifier in shortcuts:
        m, k = shortcuts[modifier]
        pyautogui.hotkey(m, k)
    else:
        pyautogui.hotkey(modifier, key)
    
    print(f"✓ Executed: {modifier}+{key}")


# ============================================================================
# SCROLLING & MOUSE
# ============================================================================

def scroll_down(units=5, wait_after=0.5):
    """Scroll down"""
    import pyautogui, time
    pyautogui.scroll(-units)
    if wait_after:
        time.sleep(wait_after)
    print(f"✓ Scrolled down {units} units")


def scroll_up(units=5, wait_after=0.5):
    """Scroll up"""
    import pyautogui, time
    pyautogui.scroll(units)
    if wait_after:
        time.sleep(wait_after)
    print(f"✓ Scrolled up {units} units")


def move_mouse(x, y):
    """Move mouse to coordinates"""
    import pyautogui
    pyautogui.moveTo(x, y)
    print(f"✓ Mouse moved to ({x}, {y})")


def double_click(x, y, wait_after=0.5):
    """Double-click at coordinates"""
    import pyautogui, time
    pyautogui.click(x, y)
    pyautogui.click(x, y)
    if wait_after:
        time.sleep(wait_after)
    print(f"✓ Double-clicked at ({x}, {y})")


def right_click(x, y, wait_after=0.5):
    """Right-click at coordinates"""
    import pyautogui, time
    pyautogui.click(x, y, button='right')
    if wait_after:
        time.sleep(wait_after)
    print(f"✓ Right-clicked at ({x}, {y})")


# ============================================================================
# FORMS & DATA ENTRY
# ============================================================================

def fill_form(fields):
    """
    Fill multiple form fields sequentially
    fields: list of {'text': 'Label', 'value': 'Input'} dicts
    """
    import time
    
    print("\n" + "="*80)
    print("FILLING FORM")
    print("="*80)
    
    for field in fields:
        label = field['text']
        value = field['value']
        
        print(f"→ Finding field: {label}")
        if click_by_text(label, wait_after=0.5):
            type_text_safe(value)
            time.sleep(0.3)
    
    print("="*80 + "\n")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def wait_for_screen_change(timeout=10, sample_delay=0.5):
    """
    Wait until screen content changes (useful for page loads, dialogs)
    """
    import pyautogui, time
    
    # Take initial screenshot
    initial = pyautogui.screenshot()
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        current = pyautogui.screenshot()
        if current != initial:
            print(f"✓ Screen changed after {time.time() - start_time:.1f}s")
            return True
        time.sleep(sample_delay)
    
    print(f"✗ Screen did not change within {timeout}s timeout")
    return False


def take_screenshot(filename):
    """
    Take and save a screenshot for debugging
    """
    import pyautogui
    
    img = pyautogui.screenshot()
    img.save(filename)
    print(f"✓ Screenshot saved: {filename}")


# ============================================================================
# EXAMPLE USAGE (uncomment to test)
# ============================================================================

if __name__ == "__main__":
    # Print all visible text
    # print_all_screen_text()
    
    # List all windows
    # list_all_windows()
    
    # Example: Click by text
    # click_by_text("Submit", wait_after=2)
    
    # Example: Type text
    # type_text_safe("Hello World", method='clipboard')
    
    # Example: Fill a form
    # fill_form([
    #     {'text': 'Name', 'value': 'John Doe'},
    #     {'text': 'Email', 'value': 'john@example.com'},
    # ])
    
    pass
