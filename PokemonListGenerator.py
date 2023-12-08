# coding: utf-8
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
from bs4 import BeautifulSoup

d = webdriver.Chrome(ChromeDriverManager().install())
wikiURL = "https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon"
content = urllib.request.urlopen(wikiURL).read()
soup = BeautifulSoup(content, "lxml")
finalPokemonNumber = 809  #Only want pokemonNumber <= 809 because I haven't played the games where pokemon number 810 onwards came out
# Want to be able to extract the pokemon number from the string of the format "###: name"
def pokemonNumber(elem):
    if str(elem[0]).isdigit() and str(elem[3]) == ":":
        f = elem[0] + elem[1] + elem[2]
        return(int(f));
    else:
        return(finalPokemonNumber + 1); 

# The wikipedia page has many additional characters added on to show what type of Pokemon they are (legendary, etc)
def fixvalues(input):
    banned = ['[','/', '~', '%', '*', '♯','‡','♭','※','†','§']
    for x in range(0, len(input)):
        if input[x] in banned:
            return(e[:x]);
    return(input);

fullPokemonList = []
isPokemonNumber = False
currentPokemon = ''
tables = soup.findAll("table", { "class" : "wikitable" })
pokemonTable = tables[2]

#Idea is to loop over each element of the table row by row, and add the pokemon name to the pokemon number to get the format '###: name'
for row in pokemonTable.findAll("tr"):
    for entry in row.findAll("td"): 

        if isPokemonNumber:
            currentPokemon += entry.getText()
            isPokemonNumber = False
            if currentPokemon != '':
                fullPokemonList.append(currentPokemon.strip("\n"))
                currentPokemon = ''
        if entry.getText().strip().isnumeric() or "N/A" in entry.getText():

            isPokemonNumber = True
            currentPokemon = entry.getText().strip() + ": "

filteredPokemonList = []
for x in fullPokemonList:
    y = fixvalues(x)
    if pokemonNumber(y) <= finalPokemonNumber: 
        filteredPokemonList.append(y[5:]) #Extracts the name from "###: name"


##Finished extracting and formatting the desired pokemon, now run them through a website to check their availability

usernameList = []

for pokemon in filteredPokemonList:
    isAvailable = True
    nameCheckerURL = 'https://lols.gg/en/name/checker/euw/{}/'.format(pokemon)
    d.get(nameCheckerURL)
    try:
        result = d.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div/form/div/h4')
    except:
        continue

## If any of the result is a number then we know that it is unavailable
    for char in result.text.split():
        if char.isdigit():
            daysUntilAvailable = int(char)
            isAvailable = False

## Noticed sometimes the website would return negative days if it was available
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