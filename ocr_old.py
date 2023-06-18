from datetime import date
import cv2
import pytesseract
import csv
import pandas as pd
import numpy as np
from saveToExcel import *

from datetime import datetime 
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract.pytesseract import Output

## tesseract_cmd for VS Code to find tesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# ---------- Functions ---------- #

def ParseText(textDetails):
    parsedText = []
    wordList = []
    lastWord = ''
    for word in textDetails['text']:
        if word != '':
            wordList.append(word)
            lastWord = word
        if (lastWord != '' and word == '') or (word == textDetails['text'][-1]):
            parsedText.append(wordList)
            wordList = []
    return parsedText

# Not used when writing to excel sheet.
# Takes in the parsed text as a list,
# returns the price as float
def GetExpense(parsedText: list) -> float:
    #print(parsedText)
    breakNext = False
    countTotalt = 0
    for list in parsedText:
        for element in list:
            if(breakNext):
                # print("Content of identified element: "+element)
                # break
                element = str(element).replace(',','.')
                return float(element)
            if ((element == "Totalt" and countTotalt == 1) or element == "KORTKÖP"):
                breakNext = True
            elif (element == "Totalt"):
                countTotalt+1

#------# Preprocessing #------#

im = cv2.imread('kvitton/kvitto2.jpg')

# make gray
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# make binary
im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Control - show the image
# cv2.imshow('the image', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

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

# Control - show the image
# cv2.imshow('Captured text', imThresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#------# Parse text #------#
parsedText = ParseText(details)
# purchase = GetExpense(parsedText)       # Old storage solution
print("The parsed text: \n", parsedText)
#print("The purchase was: ", purchase)

# ----- # Save to txt # ------ # 
with open('result_text.txt', 'w', newline='') as file:
    csv.writer(file, delimiter=" ").writerows(parsedText)

# ----- # Save to Excel # ----- #
excelFile = 'Budget.xlsx'
saveToExcel(excelFile, parsedText)