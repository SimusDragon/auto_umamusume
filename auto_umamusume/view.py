import numpy as np
import pytesseract
import pyautogui
import cv2

from resolution import Screen
screen = Screen()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

TESS_CONFIG_LETTERS = '-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXY --psm 7'
TESS_CONFIG_NUMBERS = '-c tessedit_char_whitelist=0123456789 --psm 7'
    
def get_energy():
    region = screen.scale_region(442, 131, 234, 10)
    image = screenshot(region)
    return total_energy(image)

def total_energy(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 50, 180]), np.array([180, 255, 255]))
    count = (cv2.countNonZero(mask) / (image.shape[0] * image.shape[1])) * 100
    return (cv2.countNonZero(mask) / (image.shape[0] * image.shape[1])) * 100

total_stats = 5
def get_stats():
    stats = []

    region = screen.scale_region(310, 721, 55, 25)
    offset_x = screen.scale_offset_x(95)

    x, y, w, h = region
    images = []

    for i in range(total_stats):
        x_i = x + i * offset_x
        region_i = (x_i, y, w, h)

        image = screenshot(region_i)
        images.append(image)

        text = extract_text(image, TESS_CONFIG_NUMBERS)
        try:
            stats.append(int(text))
        except ValueError:
            stats.append(0)

    total_images = np.hstack(images)
    debugger(total_images, stats)

    return stats

def get_supports():
    total_supports = 0

    offset_y = screen.scale_offset_y(101)
    region = screen.scale_region(860, 234, 65, 11)
    
    x, y, w, h = region
    images = []

    for i in range(total_stats):
        y_i = y + i * offset_y
        region_i = (x, y_i, w, h)

        image = screenshot(region_i)
        images.append(image)

        ignore = support_affinity(image)
        if ignore: continue

        total_supports += 1

    total_images = np.hstack(images)
    debugger(total_images, total_supports)

    return total_supports

def support_affinity(image):
    def count(hsv_range):
        return extract_color(right_half, *hsv_range)

    right_half = image[:, image.shape[1] // 2:]
    total = right_half.shape[0] * right_half.shape[1]

    gray_range = (np.array([115, 5, 80]), np.array([135, 40, 140]))
    orange_range = (np.array([10, 100, 100]), np.array([25, 255, 255]))

    return count(orange_range) > 0 if count(gray_range) / total > 0.25 else True

def get_infirmary():
    region = screen.scale_region(365, 985, 40, 10)
    image = screenshot(region)

    lower = np.array([125, 100, 200])
    upper = np.array([140, 255, 255])

    return extract_color(image, lower, upper)

def get_mood():
    region = screen.scale_region(725, 120, 60, 35)
    image = screenshot(region)

    mood_ranges = [
        (-2, np.array([130, 100, 200]), np.array([150, 255, 255])), # Awful
        (-1, np.array([100, 150, 150]), np.array([120, 255, 255])), # Bad
        (0, np.array([19, 120, 190]), np.array([28, 255, 255])),    # Normal
        (1, np.array([10, 100, 150]), np.array([25, 255, 255])),    # Good
        (2, np.array([160, 100, 150]), np.array([175, 255, 255])),  # Great
    ]

    for mood_value, lower, upper in mood_ranges:
        if extract_color(image, lower, upper) > 0:
            return mood_value

def get_summer():
    region = screen.scale_region(376, 35, 35, 21)
    return read_screen(region, '-c tessedit_char_whitelist=JulAug --psm 8') in ("Jul", "Aug")

def get_goal():
    region = screen.scale_region(460, 85, 50, 25)
    return read_screen(region, '-c tessedit_char_whitelist=EntryGoal --psm 8') in ("Entry", "Goal")

def get_race():
    region = screen.scale_region(260, 95, 60, 40)
    return read_screen(region, '-c tessedit_char_whitelist=Race --psm 8') == "Race"

def get_quick_race():
    region = screen.scale_region(400, 961, 90, 60)
    image = screenshot(region)

    lower = np.array([0, 0, 220])
    upper = np.array([179, 40, 255])

    return extract_color(image, lower, upper) > 0

def get_skillpt():
    region = screen.scale_region(695, 335, 75, 40)
    text = read_screen(region, TESS_CONFIG_NUMBERS)
    return int(text)

def get_event():
    region = screen.scale_region(237, 193, 325, 55)
    config = '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!?# --psm 3'
    return read_screen(region, config)

def get_win():
    region = screen.scale_region(160, 8, 90, 20)
    return read_screen(region, '-c tessedit_char_whitelist=Complete --psm 8') == "Complete"    

def get_lose():
    region = screen.scale_region(535, 260, 80, 35)
    return read_screen(region, '-c tessedit_char_whitelist=Again --psm 8') == "Again"

def get_dialogue():
    region = screen.scale_region(660, 1040, 90, 30)
    image = screenshot(region)

    if not extract_text(image, '-c tessedit_char_whitelist=Quick --psm 8') == "Quick":
        return False

    lower = np.array([35, 150,  80])
    upper = np.array([55, 255, 150])

    return extract_color(image, lower, upper) > 0    

def read_screen(region, config):
    image = screenshot(region)
    text = extract_text(image, config)
    debugger(image, text)
    return text

def screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def extract_text(image, config):
    return pytesseract.image_to_string(image, lang='eng', config=config).strip()

def extract_color(image, lower, upper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return cv2.countNonZero(mask)

def debugger(image, text):
    if False:
        print(text)
        cv2.imshow("Debug", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
