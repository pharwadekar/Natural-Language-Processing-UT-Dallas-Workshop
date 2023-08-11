################################################################################
##      FILE:            pranav_harwadekar_dateFinder.py      
##      AUTHOR:          Pranav Harwadekar           
##      DESCRIPTION:     Provided a plain text file like (text_news.txt), this python program extracts dates referenced in the text as “date” object while using nltk sentence tokenizer to properly split text using common sentence delimiters   
##      DEPENDENCIES:    Created with Python 3.11.4 (Python version); Uses nltk, re, datetime, nltk.tokenize libraries/packages
################################################################################

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from datetime import datetime, date, timedelta

inFile = open(r"c:\\Users\prana\Downloads\NLP Workshop Python UT Dallas\text_web.txt", encoding='UTF8')

text = inFile.read()
text = text.split("<p>")

patternsList = ["\d\d\d\d-\d\d-\d\d",   #YYYY-MM-DD Format
                "\d\d/\d\d/\d{4}",      #MM/DD/YYYY
                "\d\d/\d\d/(?!20)\d{2}",#MM/DD/YY
                r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d\d\d\d\b",           #BB DD, YYYY
                r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b"          #bb DD, YYYY
                ]


patternMapping = ["%Y-%m-%d",
                 "%m/%d/%Y",
                 "%m/%d/%y",
                 "%B %d, %Y",
                 "%b %d, %Y"
                 ]


masterDays = ["monday", "tuesday","wednesday", "thursday", "friday", "saturday", "sunday"]

for txt in text:
    for sent in sent_tokenize(txt):
        resArr = []

        if "today" in sent.lower():
            res = date.today()
            resArr.append(res)
        if "yesterday" in sent.lower():
            res = date.today() - timedelta(days = 1)
            resArr.append(res)
        if "tomorrow" in sent.lower():
            res = date.today() + timedelta(days = 1)
            resArr.append(res)
        todaysIndex = datetime.now().weekday()
        futDays = re.findall("(next)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", sent, flags = re.IGNORECASE)
        if futDays != []:
            dayStr = str(futDays[0])[10:-2].lower()
            tod = datetime.now()
            diff = masterDays.index(dayStr) - todaysIndex
            if diff > 0:
                sum = diff + tod.day
                modifiedDate = tod.replace(day = sum).date()
                resArr.append(modifiedDate)
            else:
                sum = diff + tod.day + 7
                modifiedDate = tod.replace(day = sum).date()
                resArr.append(modifiedDate)
        
        pastDays = re.findall("(last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", sent, flags = re.IGNORECASE)
        if pastDays != []:
            dayStr = str(pastDays[0])[10:-2].lower()
            tod = datetime.now()
            diff = todaysIndex - masterDays.index(dayStr)
            if diff > 0:
                sum = tod.day - diff
                modifiedDate = tod.replace(day = sum).date()
                resArr.append(modifiedDate)
            else:
                sum = tod.day - diff - 7
                modifiedDate = tod.replace(day = sum).date()
                resArr.append(modifiedDate) 

        thisWeekday = re.findall("(this)\sweekday",sent, flags = re.IGNORECASE)
        if thisWeekday != []:
            tod = datetime.now()
            sum = tod.day - todaysIndex
            for i in range(5):
                modifiedDate = tod.replace(day = sum)
                resArr.append(modifiedDate.date())
                sum +=1
                #todaysIndex - print(i)#todaysIndexcc



        for index, pattern in enumerate(patternsList):
            result = re.findall(pattern, sent, flags=re.IGNORECASE)
            if not(result == []):
                resArr.append(result)
                for i, dates in enumerate(resArr):
                    dateObj = datetime.strptime(result[i], patternMapping[index])
                    resArr.remove(result)
                    resArr.append(dateObj.date())
                    break
        if resArr != []:
            printingTxt = "("
            for result in resArr:
                printingTxt += str(result)
                printingTxt += ", "          
            printingTxt += "\"" + str(sent) +"\")"
            print(printingTxt)
inFile.close()