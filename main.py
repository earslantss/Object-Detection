import cv2 as cv
import numpy as np
import win32gui, win32con, win32ui
from detection import detectImg

# list_window_names()
# exit()

def capture_window_image(window_title):
    hwnd_target = win32gui.FindWindow(None, window_title)
    if hwnd_target == 0:
        print("Window not found")
        return None
    
    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    w = right - left
    h = bot - top

    win32gui.SetForegroundWindow(hwnd_target)

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)

    if result == None:
        return cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    else:
        print("Capture failed")
        return None

points = []

while True:

    screenshot = capture_window_image('Hesap Makinesi')

    cv.imshow('Result', screenshot)

    points = detectImg(needle_img_path='key.jpg',temp_img=screenshot,debug_mode='Rectangles')
    print(points)

    if cv.waitKey(1) == ord('q'):
        break


cv.destroyAllWindows()
