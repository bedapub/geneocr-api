import cv2
from pytesseract import Output
import pytesseract
import imutils

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\geserp\Anaconda3\Library\bin\tesseract.exe'


def rotate_image(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)

    # display the orientation information
    print("[INFO] detected orientation: {}".format(
        results["orientation"]))
    print("[INFO] rotate by {} degrees to correct".format(
        results["rotate"]))
    print("[INFO] detected script: {}".format(results["script"]))

    rotated = imutils.rotate_bound(image, angle=results["rotate"])

    return rotated