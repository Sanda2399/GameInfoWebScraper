import pytz
import requests
from flask import Flask
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread

# Creation of Flask app
app = Flask('GameInfoBot')

# ------ Data Storage ------
gameNames = []
gamePrices = []
gameLinks = []

gameData = {}
gameData['catalog'] = []

# ---------- CODE ---------
def jsonDataForGames():
    # Adds the current time of the recent page check.
    timeZone_NY = pytz.timezone('US/Eastern')
    dateTime_NY = datetime.now(timeZone_NY)
    currentTime = dateTime_NY.strftime("%H:%M:%S - (%d/%m)")

    # Fake browser header
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # Make a request to the given link.
    response = requests.get('https://limitedrungames.com/collections/in-stock-switch', headers=header)

    # Parse and store the page data
    pageData = BeautifulSoup(response.text, 'html.parser')


    #  1.  ---------- Get the name of the newest limited run games for switch ----------
    for gameTitle in pageData.find_all('div', class_ = 'title'):
        gameNames.append(gameTitle.text)


    # 2. ---------- Get the prices ----------
    for gamePrice in pageData.find_all('span', class_ = 'theme-money'):
        gamePrices.append(gamePrice.text)


    # removal of the double prices. Iterates through the current gamePrice list by 2 (landing on every odd number starting from 1)
    # and adds the current selected price to the new list.
    updatedGamePrices = []
    for i in range(1, len(gamePrices), 2):
        updatedGamePrices.append(gamePrices[i])


    # 3. ---------- Get product links ----------
    for link in pageData.find_all('a', class_ = 'product-link'):
        fullLink = link.get('href')
        fullLink = 'https://limitedrungames.com/' + fullLink

        gameLinks.append(fullLink)


    # 4. ---------- Creates a 'catalog' that holds the name, price and images for a game. ----------
    for (gameName, gamePrice, gameLink) in zip(gameNames, updatedGamePrices, gameLinks):
        gameObject = {"name" : gameName, "price" : gamePrice, "productLink" : gameLink, "availibleOnSiteSince" : currentTime}

        gameData['catalog'].append(gameObject)
    
    return gameData
    

# ---------- Turns each object in the catalog into a JSON object ----------    
@app.route('/')
def getGameData():
    return jsonDataForGames()