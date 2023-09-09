import cv2
import pytesseract
import csv

from PIL import Image, ImageEnhance, ImageFilter
from pytesseract.pytesseract import Output

from parseText import ParseText

## tesseract_cmd for VS Code to find tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/5.3.1_1/bin/tesseract' 
#"C:/Program Files/Tesseract-OCR/tesseract.exe"

#------# Functions #----------#

# def ParseText(testDetails):
#     parseText = []
#     wordList = []
#     lastWord = ''
    # for word in details['text']:
    #     if word != '':
    #         wordList.append(word)
    #         lastWord = word
    #     if (lastWord != '' and word == '') or (word == details['text'][-1]):
    #         parseText.append(wordList)
    #         wordList = []
    # return parsedText

#------# Preprocessing #------#

img = cv2.imread('kvitton/kvitto.jpg')

# make gray
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# make binary
im = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

## Potential improvement
#im = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 5) 

cv2.imshow('the image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

#------# Read image #------#

# Configurations
config = r'--oem 3 --psm 6'

details = pytesseract.image_to_data(im, output_type=Output.DICT, config=config, lang='eng')
# print(details.keys())

#------# Make boxes #------#
totalBoxes = len(details['text'])

for sequenceNumber in range(totalBoxes):
        #print(int(float(details['conf'][sequenceNumber])))
    if int(float(details['conf'][sequenceNumber])) >30:
        (x,y,w,h) = (details['left'][sequenceNumber], details['top'][sequenceNumber], details['width'][sequenceNumber], details['height'][sequenceNumber])
        imThresh = cv2.rectangle(im, (x,y), (x+w, y+h), (0,255,0), 2)

#cv2.imshow('Captured text', imThresh)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#------# Parse text #------#
parsedText = ParseText(details)

# ----- # Save to txt # ------ # 
with open('result_text_adaptive.txt', 'w', newline='') as file:
    csv.writer(file, delimiter=" ").writerows(parsedText)   