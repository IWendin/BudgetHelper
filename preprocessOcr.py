import cv2
import pytesseract
import csv

from PIL import Image, ImageEnhance, ImageFilter
from pytesseract.pytesseract import Output

## tesseract_cmd for VS Code to find tesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

#------# Preprocessing #------#

im = cv2.imread('kvitton/kvitto.jpg')

# make gray
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# make binary
im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow('the image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()

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

cv2.imshow('Captured text', imThresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

#------# Parse text #------#
parseText = []
wordList = []
lastWord = ''
for word in details['text']:
    if word != '':
        wordList.append(word)
        lastWord = word
    if (lastWord != '' and word == '') or (word == details['text'][-1]):
        parseText.append(wordList)
        wordList = []

with open('result_text.txt', 'w', newline='') as file:
    csv.writer(file, delimiter=" ").writerows(parseText)