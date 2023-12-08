from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

inputFile = open(r"/Users/dexiusram/Desktop/Programs/Webtests/pokemonList.txt", "r")
d = webdriver.Chrome(ChromeDriverManager().install())



pokemonList = []
usernameList = []

## Setup the list of pokemon
for x in inputFile:
    pokemonList.append(x.strip("\n"))
inputFile.close()



for pokemon in pokemonList:
    isAvailable = True
    url = 'https://lols.gg/en/name/checker/euw/{}/'.format(pokemon)
    d.get(url)
    try:
        result = d.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div/form/div/h4')
    except:
        continue

## If any of the result is a number then we know that it is unavailable
    for char in result.text.split():
        if char.isdigit():
            daysUntilAvailable = int(char)
            isAvailable = False

## Noticed sometimes the website would return negative days
    if isAvailable or daysUntilAvailable <= 0:
        usernameList.append(((pokemon) + " is available", 0))
    else:
        usernameList.append((pokemon + " is available in {} days".format(stored), stored))

## So the website doesnt block me out
    time.sleep(1.5)

outputFile = open(r"/Users/dexiusram/Desktop/Programs/Webtests/userlist.txt", "w")


def secondCharacter(i):
    return(int(i[1]));

usernameList.sort(key=secondCharacter)
for x in range(0, len(usernameList)):
    outputFile.write("{}\n".format(usernameList[x][0]))
d.quit()
outputFile.close()