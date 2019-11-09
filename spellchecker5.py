import re
import time
import datetime
from difflib import SequenceMatcher

file = open("EnglishWords.txt", 'r')
dictWords = file.readlines()
#getting rid of the '\n' in each element by getting rid of the last two characters
#also get rid of all the leading and trailing whitespaces in each line of the file (in case there are any)
dictWords = [word[:len(word)-1].strip() for word in dictWords]

def getTextFromFile(filename):
    content = ""
    try:
        #using a try-except block here just in case the user enters a filename that doesn't exist
        file = open(filename, 'r')
        content = file.read()
    except:
        #file was not found
        print("ERROR: File not found!")
    return content.lower()

def getLikeliestWord(word):
    maxScore = 0.0
    maxScoreWord = ""
    for dictWord in dictWords:#iterate over every word in the list that contains all the valid words
        score = SequenceMatcher(None, word, dictWord).ratio()
        if score > maxScore:
            #if current score is greater than previously encountered max, the max becomes current
            #additionally, the maxScoreWord is assigned the corresponding word from the list
            maxScore = score
            maxScoreWord = dictWord
    return maxScoreWord

def processInput(sentence, filename):
    sentence = sentence.strip()
    #re pattern is used to recognise anything that is not a digit or a letter (alphanumeric)
    rePattern = "[^'\-a-zA-Z]+"
    #replace every non alphanumeric character in the string with a whitespace
    sentence = re.sub(rePattern, ' ', sentence)
    #getting the words in the input by splitting the input string by occurences of the whitespace character
    sentenceWords = sentence.split(" ")
    #get rid of all the empty string literals from the list
    sentenceWords = list(filter(lambda x: x != '', sentenceWords))
    sentenceWords = list(map(lambda x: x.replace("'", "") if "'" in x else x, sentenceWords))
    sentenceWords = list(map(lambda x: x.replace("-", "") if "-" in x else x, sentenceWords))
    #the number of correctly spelt words in incremented every time we encounter such a word in the input
    correctWords = 0
    addedWords = 0
    ignoredWords = 0
    markedWords = 0
    totalWords = len(sentenceWords)
    for (index, word) in enumerate(sentenceWords):
        #iterating over every word in the input
        #let the user know if it is spelled correctly ot not 
        if word in dictWords:
            correctWords += 1
        else:
            while True:
                print("\n  W O R D   N O T   F O U N D\n")
                print("\n"+word+" not found \n")
                likeliestWord = getLikeliestWord(word)
                print("Did you mean "+likeliestWord)
                choice = input("Enter [y] or [n]: ").lower()[0]#using [0] in case they type "yes" or "no"
                if choice == "n":
                    while True:
                        print("\n  W O R D   N O T   F O U N D\n")
                        print("\n"+word+" not found \n")
                        print("1. Ignore the word.")
                        print("2. Mark the word as incorrect.")
                        print("3. Add word to dictionary. \n")

                        choice = input("Enter choice: ")
                        if choice == "1":
                            #encapsulate the word with '!'
                            ignoredWords += 1
                            sentenceWords[index] = "!"+word+"!"
                            break
                        elif choice == "2":
                            #encapsulate the word with '?'
                            markedWords += 1
                            sentenceWords[index] = "?"+word+"?"
                            break
                        elif choice == "3":
                            #encapsulate the word with '*'
                            #add the word to the dictionary file
                            addedWords += 1
                            dictFile = open("EnglishWords.txt", 'a+')
                            dictFile.write(word+"\n")
                            dictFile.close()
                            sentenceWords[index] = "*"+word+"*"
                            break
                        else:
                            #if the choice is not valid, loop again and display choice menu
                            print("ERROR: Choice not Found! \n")
                    break
                elif choice == "y":
                    sentenceWords[index] = likeliestWord
                    break
                print("ERROR: Invalid choice!")
                    

    incorrectWords = totalWords - correctWords
    print("Number of words:", totalWords)
    print("Number of correctly spelt words:", correctWords)
    print("Number of incorrectly spelt words:", incorrectWords)
    print("\t Number ignored:", ignoredWords)
    print("\t Number added to dictionary:", addedWords)
    print("\t Number maked:", markedWords,"\n")
    #make the output file with sentenceWords
    outputString = ' '.join(sentenceWords)
    file = open("out_"+filename, 'w')
    date = datetime.date.today().strftime("%d-%m-%Y")
    time = datetime.datetime.now().time().strftime("%H:%M")
    file.write(date + " " + time + "\n")
    file.write("Number of words: "+str(totalWords)+"\n")
    file.write("Number of correctly spelt words: "+str(correctWords)+"\n")
    file.write("Number of incorrectly spelt words: "+str(incorrectWords)+"\n")
    file.write("\t Number ignored: "+str(ignoredWords)+"\n")
    file.write("\t Number added to dictionary: "+str(addedWords)+"\n")
    file.write("\t Number marked: "+str(markedWords)+"\n\n")
    file.write(outputString)

while True:
    sentence = ""
    #if user chooses to input without file, then default filename is set to this
    filename = "shellInput.txt"
    print("\n  S P E L L   C H E C K E R  \n")
    print("1. Check a file")
    print("2. Check a sentence\n")
    print("0. Quit\n")
    choice = input("Enter choice: ")
    print()
    startTime = time.time()
    if choice == "1":
        print("\n  L O A D   F I L E \n")
        #filename is changed if they choose to provide the input from a file
        filename = input("Enter the name of the file to spellcheck: ")
        sentence = getTextFromFile(filename)
        if sentence == "":
            #there was an error in reading the file
            #try getting the input from the user again
            continue
    elif choice == "2":
        print("\n  I N P U T \n")
        #get input from shell
        sentence = input("Enter sentence to spellcheck: ").lower()
    elif choice == "0":
        #user chose to exit so break from loop
        break
    else:
        #choice was not defined to display menu again
        print("ERROR: Invalid Choice!")
        continue
    processInput(sentence, filename)
    endTime = time.time()
    print("\n Time elapsed", (endTime - startTime), "microseconds\n")
    choice = input("Press q [enter] to quit or any other key [enter] to go again: ")
    if choice == 'q':
        break
