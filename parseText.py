

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