import cv2
import numpy as np


def create_masked_image(img, h, w):
    """To create a masked area around the signature"""

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    
    # pre-processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray1 = gray.copy()
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    cv2.rectangle(gray, (0, 0), (w, h), (0, 0, 0), int((h*w/(h+w))*(1/100)))
    gray = cv2.Canny(gray, 0, 255)
    gray = cv2.dilate(gray, kernel, iterations=2)
    
    # creating the mask
    mask = np.zeros_like(gray1)
    contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for cnt in contours:
        areas.append(cv2.contourArea(cnt))
    max_i = areas.index(max(areas))
    cv2.drawContours(mask, contours, max_i, 255, -1)
    eroded = cv2.erode(mask, kernel, iterations=30)
    mask = cv2.bitwise_not(eroded)
    masked_image = cv2.add(gray1, mask)

    return masked_image


def crop_image(thresh_gray):
    """crop rectangular region around black pixels"""
    
    points = np.argwhere(thresh_gray == 0)  
    points = np.fliplr(points)  
    x, y, w, h = cv2.boundingRect(points) 
    x, y, w, h = x - 10, y - 10, w + 20, h + 20  
    crop = thresh_gray[y:y + h, x:x + w] 
    
    return crop


def enhance_and_crop(image):
    """"""
    
    # removing unwanted pixels
    try:
        height, width, _ = image.shape
    except:
        height, width = image.shape
    masked = create_masked_image(image, height, width)

    # get the threshold'ed crop
    _, thresh_gray = cv2.threshold(masked, thresh=100, maxval=255, type=cv2.THRESH_BINARY)
    crop = crop_image(thresh_gray)
    _, thresh_crop = cv2.threshold(crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)
    output = crop_image(thresh_crop)

    # display output
    height, width = output.shape
    final_show = cv2.resize(output, (width // 3, height // 3))
    cv2.imshow("Cropped and threshold'ed image", final_show)
    cv2.waitKey(0)

    return output


# signature output
image = cv2.imread(r'D:\test_files\Capture.PNG')
output = enhance_and_crop(image)

cv2.destroyAllWindows()
