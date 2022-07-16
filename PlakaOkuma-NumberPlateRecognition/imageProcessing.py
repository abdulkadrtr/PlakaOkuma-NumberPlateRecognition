import cv2
import imutils
import numpy as np
import save
from unittest import result
import easyocr

def rec(img):
    #Filtreleme islemi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    try:
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.017 * peri, True)
            if len(approx) == 4:
                screenCnt = approx
                break
        if screenCnt is None:
            detected = 0
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
        #Maskeleme islemi
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        #Kırma islemi
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
        #EasyOCR islemi
        reader = easyocr.Reader(['en'])
        text = reader.readtext(Cropped)
        text = text[0][1]
        text = text.replace(" ", "")
        text = text.upper()
        sonuc = 0
        if(len(text)>=7):
            if(int(text[0]) and int(text[1])):
                if(str(text[4])):
                    if(int(text[5:])):
                        sonuc=1
                else:
                    if(int(text[4:])):
                        sonuc=1
        if(sonuc==1):
            save.write(text)
            print(text)
    except Exception:
        pass
    return img