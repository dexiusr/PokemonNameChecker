# coding: utf-8

import urllib.request
from bs4 import BeautifulSoup
outputFile = open(r"/Users/dexiusram/Desktop/Programs/Webtests/pokemonList.txt", "w")
URL = "https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon"
content = urllib.request.urlopen(URL).read()
soup = BeautifulSoup(content, "lxml")

finalPokemonNumber = 809 #Only want pokemonNumber <= 809 because I haven't played the games where pokemon number 810 onwards came out

# Want to be able to extract the pokemon number from the string of the format "###: name"
def pokemonNumber(elem):
    if str(elem[0]).isdigit() and str(elem[3]) == ":":
        f = elem[0] + elem[1] + elem[2]
        return(int(f));
    else:
        return(999);

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



for x in fullPokemonList:
    y = fixvalues(x)
    if pokemonNumber(y) <= finalPokemonNumber:
        outputFile.write(y[5:]+"\n") #Extracts the name from "###: name"

outputFile.close()
