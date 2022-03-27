import pandas as pd

def GetPurchase(parsedText):
    # print(parsedText)
    budgetDf = pd.DataFrame({'Date': [0], 'Expense': [0], 'Store': [0], 'Category': [0]})
    # print(budgetDf)
    addDate = 0
    addExpense = False
    addStore = True
    countTotalt = 0
    for list in parsedText:
        for element in list:
            if(addDate == 1):
                dateObject = pd.to_datetime(str(element), format="%Y-%m-%d")
                budgetDf['Date'] = dateObject
                # print(budgetDf)
                addDate+1
            if(addExpense):
                element = str(element).replace(',','.')
                budgetDf['Expense'] = float(element)
                # print(budgetDf)
                return budgetDf
            if(element == "KORTKOP" or element == "KORTKÖP" or (element == "Totalt" and countTotalt == 1)):
                addExpense = True
            elif(element == "Totalt"):
                countTotalt = 1
            if(element == "Datum:"):
                addDate+1
            if((element == 'HEMKÖP' or element == 'HEMKOP' or element == 'Coop') and addStore):
                element = str(element)
                budgetDf['Store'] = element
                addStore = False

            