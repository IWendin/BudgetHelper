import pandas as pd
from getPurchase import * 

def saveToExcel(excelFile, parsedText):
    # Read file
    budget_sheet = pd.read_excel(excelFile, sheet_name=0)

    # Fill content
    purchaseDf = GetPurchase(parsedText)
    #print("The purchase was: \n", purchaseDf)
    budget_sheet = pd.concat([budget_sheet, purchaseDf])
    # print("The updated file has content: \n", budget_sheet)

    # Write to file 
    budget_sheet.to_excel(excelFile, index=False)
    print("The saved budget sheet has content: \n", budget_sheet)
