import pyautogui
import webbrowser
import time

def search_and_click():
    # 1. Open the browser and go to Google
    search_query = "india vs newzealand T20 schedule"
    url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    
    print("Opening browser...")
    webbrowser.open(url)
    
    # 2. Wait for the page to load 
    # (Adjust this if your internet is slow)
    time.sleep(10) 
    
    # 3. Locate the first link
    # Since search results move, we use a shortcut: 
    # Press 'TAB' until we hit the first result or use coordinates.
    # A reliable way on Google is to press 'TAB' about 15-20 times 
    # OR just click at a standard coordinate.
    
    # Let's use a common coordinate for the first result on most screens:
    # Note: (400, 450) is a rough estimate for the first result.
    print("Clicking the first result...")
    pyautogui.click(400, 450) 

if __name__ == "__main__":
    search_and_click()