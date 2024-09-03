import numpy as np
import cv2
from tkinter import Tk, filedialog

def display_fullscreen(image):
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def pencil_sketch(img, ksize, gamma):
    # Step-1: Convert image into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Step-2: Apply Gaussian blur to the image
    blur = cv2.GaussianBlur(gray, (ksize, ksize), 0)
    # Step-3: Division image
    division_img = cv2.divide(gray, blur, scale=256)
    # Step-4: Adjusting gamma factor
    if gamma == 0:
        gamma = 0.01
    elif gamma < 0:
        raise Exception('Cannot Be Negative', 'Gamma value cannot be a negative number (range = 0-1)')
    elif gamma > 1:
        raise Exception('Cannot Be Greater Than 1', 'Gamma value cannot be greater than 1 (range = 0-1)')

    invgamma = 1 / gamma
    lut = np.array([((i / 255) ** invgamma) * 255 for i in range(0, 256)])
    pencil_sketch_img = cv2.LUT(division_img.astype('uint8'), lut.astype('uint8'))

    return pencil_sketch_img

def get_image_from_user():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    return file_path

if __name__ == "__main__":
    image_path = get_image_from_user()
    if image_path:
        img = cv2.imread(image_path)
        if img is not None:
            display_fullscreen(img)
            pencil_img = pencil_sketch(img, 5, 0.5)
            display_fullscreen(pencil_img)
        else:
            print("Error: Could not read the image.")
    else:
        print("No image selected.")
