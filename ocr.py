from datetime import date
import cv2
import pytesseract
import csv
import pandas as pd
import numpy as np

from datetime import datetime 
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract.pytesseract import Output

from parseText import ParseText

## tesseract_cmd for VS Code to find tesseract. NOTE! Update PATH to fit your installation location
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/5.3.1_1/bin/tesseract'  
##"C:/Program Files/Tesseract-OCR/tesseract.exe"

# ---------- Functions ---------- #

# def ParseText(textDetails):
#     parsedText = []
#     wordList = []
#     lastWord = ''
#     for word in textDetails['text']:
#         if word != '':
#             wordList.append(word)
#             lastWord = word
#         if (lastWord != '' and word == '') or (word == textDetails['text'][-1]):
#             parsedText.append(wordList)
#             wordList = []
#     return parsedText

def GetExpense(parsedText: list) -> float:
    #print(parsedText)
    breakNext = False
    for list in parsedText:
        for element in list:
            if(breakNext):
                #print("Content of identified element: "+element)
               # break
               element = str(element).replace(',','.')
               return float(element)
            if(element == "KORTKOP" or element == "KORTKÖP"):
                breakNext = True

def GetPurchase(parsedText):
    # print(parsedText)
    budgetDf = pd.DataFrame({'Ware': [0], 'Expense': [0], 'Date': [0], 'Store': [0], 'Category': [0]})
    # print(budgetDf)
    addDate = False
    addExpense = False
    for list in parsedText:
        for element in list:
            if(addDate):
                dateObject = pd.to_datetime(str(element), format="%Y-%m-%d")
                budgetDf['Date'] = dateObject
                # print(budgetDf)
                addDate = False
            if(addExpense):
                element = str(element).replace(',','.')
                budgetDf['Expense'] = float(element)
                # print(budgetDf)
                return budgetDf
            if(element == "KORTKOP" or element == "KORTKÖP"):
                    addExpense = True
            if(element == "Datum:"):
                    addDate = True



    
#------# Preprocessing #------#

img = cv2.imread('kvitton/kvitto.jpg')

# make gray
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# make binary
im = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

## Adaptive is not an improvement
#im = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 5) 

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
purchase = GetExpense(parsedText)

# ----- # Save to txt # ------ # 
with open('result_text_adaptive.txt', 'w', newline='') as file:
    csv.writer(file, delimiter=" ").writerows(parsedText)

# ----- # Save to Excel # ----- #
excelFile = 'Budget.xlsx'

# Read file
budget_sheet = pd.read_excel(excelFile, sheet_name=0)
print("The loaded budget sheet has content: \n", budget_sheet)

# Fill content
purchaseDf = GetPurchase(parsedText)
#print("The purchase was: \n", purchaseDf)
budget_sheet = pd.concat([budget_sheet, purchaseDf])
# print("The updated file has content: \n", budget_sheet)

# Write to file 
budget_sheet.to_excel(excelFile, index=False)
