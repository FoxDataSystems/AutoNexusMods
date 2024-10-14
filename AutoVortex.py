import pyautogui
import cv2
import numpy as np
import time
from screeninfo import get_monitors
import pytesseract
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(filename='mod_download_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path as needed

def find_download_button():
    # Get the left screen (assuming it's the second monitor)
    monitors = get_monitors()
    target_screen = monitors[1]  # Index 1 for the second monitor
    
    # Take a screenshot of the target screen
    screenshot = pyautogui.screenshot(region=(target_screen.x, target_screen.y, 
                                              target_screen.width, target_screen.height))
    
    # Convert the image from RGB to BGR color space
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Define the color range for orange (in BGR)
    lower_orange = np.array([32, 97, 158])
    upper_orange = np.array([40, 123, 200])
    
    # Create a mask for orange color
    mask = cv2.inRange(screenshot, lower_orange, upper_orange)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Check if the contour is large enough to be a button
        if w > 50 and h > 20:
            # Use OCR to check if "Download" is written on the button
            button_image = screenshot[y:y+h, x:x+w]
            text = pytesseract.image_to_string(button_image).strip().lower()
            if text == "download":
                # Adjust coordinates based on screen position
                return target_screen.x + x + w//2, target_screen.y + y + h//2
    
    return None

def find_slow_download_button():
    # Get the left screen (assuming it's the second monitor)
    monitors = get_monitors()
    target_screen = monitors[1]  # Index 1 for the second monitor
    
    # Take a screenshot of the target screen
    screenshot = pyautogui.screenshot(region=(target_screen.x, target_screen.y, 
                                              target_screen.width, target_screen.height))
    
    # Convert the image from RGB to BGR color space
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Define the color range for the button (in BGR)
    target_color = np.array([220, 220, 221])  # BGR equivalent of rgb(221,220,220)
    color_range = 10  # Adjust this value if needed for color matching tolerance
    
    # Create a mask for the target color
    mask = cv2.inRange(screenshot, target_color - color_range, target_color + color_range)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Check if the contour is large enough to be a button
        if w > 50 and h > 20:
            # Use OCR to check if "Slow DOWNLOAD" is written on the button
            button_image = screenshot[y:y+h, x:x+w]
            text = pytesseract.image_to_string(button_image).strip().lower()
            if "slow download" in text:
                # Adjust coordinates based on screen position
                return target_screen.x + x + w//2, target_screen.y + y + h//2
    
    return None

def wait_for_download_completion(timeout_minutes=15):
    start_time = datetime.now()
    while (datetime.now() - start_time) < timedelta(minutes=timeout_minutes):
        # Check if we're back on the Vortex screen
        if find_download_button():
            return True
        time.sleep(5)  # Check every 10 seconds
    print("Download button is not there yet...")
    return False

def download_mod(mod_number):
    logging.info(f"Attempting to download mod {mod_number}")
    
    # Find and click the orange Download button
    button_pos = find_download_button()
    if button_pos:
        pyautogui.click(button_pos)
        logging.info("Clicked orange Download button")
        time.sleep(2)  # Wait for the new screen to load
        
        # Find and click the Slow DOWNLOAD button
        slow_button_pos = find_slow_download_button()
        if slow_button_pos:
            pyautogui.click(slow_button_pos)
            logging.info("Clicked Slow DOWNLOAD button")
            
            # Wait for download completion or timeout
            if wait_for_download_completion():
                logging.info(f"Mod {mod_number} downloaded successfully")
                return True
            else:
                logging.warning(f"Download timeout for mod {mod_number}")
                return False
        else:
            logging.warning("Slow DOWNLOAD button not found")
            return False
    else:
        logging.warning("Orange Download button not found")
        return False

def main():
    num_mods = 50
    for i in range(num_mods):
        mod_number = i + 1
        attempts = 0
        max_attempts = 300
        
        while attempts < max_attempts:
            if download_mod(mod_number):
                break
            attempts += 1
            if attempts < max_attempts:
                logging.info(f"Retrying mod {mod_number} (Attempt {attempts + 1})")
                time.sleep(5)  # Wait before retrying
        
        if attempts == max_attempts:
            logging.error(f"Failed to download mod {mod_number} after {max_attempts} attempts")
            logging.info("Exiting the script due to repeated failures")
            break
        
        time.sleep(5)  # Wait between mod downloads

if __name__ == "__main__":
    main()