# Created By Alliance82
# Created On 9/12/2021
# Connects to the RAWG.IO Video Game Database API and returns video game information and is stored locally for personal use
import sqlite3
import json
import urllib.request
import time
import datetime as DT
import sys

# The below is the path to the file that the API Key is kept in
api_key_path = r'Your API Key file path goes here'
sys.path.append(api_key_path)
from Census_API_Key import apiKey
apiKey = apiKey
sys.path.remove(api_key_path)

# Variable to be used in the API call and pagination
today = DT.date.today()
week_ago = str(today - DT.timedelta(days=7))
today = time.strftime('%Y-%m-%d', time.gmtime())
startDate=week_ago
endDate=today
page_size=50
platforms="1,14,80,186"

print("Date: " + today)
print("Last Week: ", week_ago)
#Our JSON request to retrieve data about asteroids approaching planet Earth.
url ="https://api.rawg.io/api/games?key=" + apiKey+"&dates=2020-09-01,2025-12-31"+ "&platforms=" + platforms + "&page_size="+str(page_size)
baseURL="https://api.rawg.io/api/games" + apiKey
print("URL: ", url)
response = urllib.request.urlopen(url)
result = json.loads(response.read())
#print(result)
games = result["results"]
nextURL = str(result["next"])
prevURL = str(result["previous"])
totalRecords=result["count"]
totalPages=totalRecords/page_size
a=0

#Connect to SQL Lite DB
connection = sqlite3.connect('games.db')
cursor = connection.cursor()
#Create Gaming Platforms Table
cursor.execute('CREATE TABLE if not exists games (gameID INT, gameName TEXT, gameReleaseDate TEXT, gameBackground_Image TEXT, metacritic INT, gamePlatformList TEXT, gamePlatformIDList TEXT, gameGenreList TEXT, PRIMARY KEY (gameID))')
connection.commit()
gamePlatforms=games[0]['platforms']
print("There are a total of " + str(totalRecords) + " and a page size of " + str(page_size) + " so there will be " + str(totalPages) + " total pages")

while a <= totalPages:
  a+=1
  print(a)
  url ="https://api.rawg.io/api/games?key=" + apiKey +"&dates=2000-09-01,2025-12-31" + "&platforms=" + platforms + "&page_size=" + str(page_size) + "&page=" + str(a)
  print("URL: ", url)
  nextURL = str(result["next"])
  print(nextURL)
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  #print(result)
  games = result["results"]
  nextURL = str(result["next"])
  prevURL = str(result["previous"])
  games = result["results"]
  gamePlatforms=games[0]['platforms']

  for x in range(len(games)):
        try:
          print(x)
          gameID=str(games[x]['id'])
          gameName=str(games[x]['name'])
          gameReleaseDate=str(games[x]['released'])
          gameBackground_Image=str(games[x]['background_image'])
          metacritic=str(games[x]['metacritic'])
          gamePlatforms=games[x]['platforms']
          gameGenres=games[x]['genres']
          gamePlatformList=""
          gamePlatformIDList=""
          gameGenreList=""


          for y in range(len(gamePlatforms)):
              try:
                  #print("start loop")
                  gamePlatformVar=gamePlatforms[y]['platform']['name']
                  gamePlatformIDVar=str(gamePlatforms[y]['platform']['id'])
                  #print(gamePlatformVar)
                  if y==1:
                    gamePlatformList=gamePlatformVar
                    gamePlatformIDList=str(gamePlatformIDVar)
                  else:
                    gamePlatformList=gamePlatformList+", "+gamePlatformVar
                    gamePlatformIDList=str(gamePlatformIDList+", "+gamePlatformIDVar)
              except:
                  print("Unable to access all data about game platforms.") 

          for z in range(len(gameGenres)):
              try:
                  #print("start loop")
                  gameGenreVar=gameGenres[z]['name']
                  #print(gamePlatformVar)
                  if z==1:
                    gameGenreList=gameGenreVar
                  else:
                    gameGenreList=gameGenreList + ", "+ gameGenreVar
              except:
                  print("Unable to access all data about game genres.") 
          print("gameName: " + gameName + "Game ID: " + gameID + "Game Genres: " + gameGenreList)
          print("Inserting data into games sqldb")
          cursor.execute("insert into games (gameID, gameName, gameReleaseDate, gameBackground_Image, metacritic, gamePlatformList, gamePlatformIDList, gameGenreList) values (?,?,?,?,?,?,?,?)", (gameID, gameName, gameReleaseDate, gameBackground_Image, metacritic, gamePlatformList, gamePlatformIDList, gameGenreList))

        except:
          print("Unable to sotre all data.")  
  print("--------------------")

connection.commit()
print("Selecting data from sqldb")
cursor.execute('SELECT * FROM games')
data = cursor.fetchall()
connection.close()
print(data)
