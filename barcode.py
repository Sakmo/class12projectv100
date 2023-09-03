#Adm No 35 ---> G46-00035

import cv2
from pyzbar import pyzbar
import warnings

def read_barcodes_for_each_frame(frame):
    warnings.filterwarnings('ignore')
    barcodes_in_frame = pyzbar.decode(frame) #returns empty list if no barcodes found
    s = 0
    for barcode in barcodes_in_frame: #wont run if no barcodes found
        barcode_info = barcode.data.decode('utf-8')  #scanned string
        try:
            s = int(barcode_info[-3:])
        except:
            print('Invalid Barcode, enter manually:')
            return None, frame
    return s,frame

def scan():
    s = 0
    manualEntry = False
    camera = cv2.VideoCapture(1)  #0 for iriun, 1 for laptop camera
    ret, frame = camera.read()    #2
    while ret and s==0:
        ret, frame = camera.read()
        s, frame_with_barcode = read_barcodes_for_each_frame(frame)
        cv2.imshow('ID Card Scanner (Press ESC to enter manually)', frame_with_barcode)
        if cv2.waitKey(1)==27:  #27 is the cv2 order of escape key
            manualEntry = True
            break
    camera.release()
    cv2.destroyAllWindows()
    if manualEntry:
        return None
    else:
        return s
