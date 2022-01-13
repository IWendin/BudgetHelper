import pandas as pd

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