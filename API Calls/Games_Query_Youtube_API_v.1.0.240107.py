# Created By Alliance82
# Created On 1/7/2024
# Connect to Youtube API
import sqlite3, json
import time, datetime as DT
from googleapiclient.discovery import build
import sys
# The below is the path to the file that the API Key is kept in
api_key_path = r'Your API Key file path goes here'
sys.path.append(api_key_path)
from Census_API_Key import apiKey
apiKey = apiKey
sys.path.remove(api_key_path)

# Date math that is for easily changing the dates in the sql query below against the games.db
today = DT.date.today()
connection = sqlite3.connect('games.db')
year_ago = str(today - DT.timedelta(days=365))
last_month=str(today - DT.timedelta(days=31))
next_week=str(today + DT.timedelta(days=8))
next_month=str(today + DT.timedelta(days=31))
today = time.strftime('%Y-%m-%d', time.gmtime())

# Connecting to and querying games.db
connection = sqlite3.connect('games.db')
cursor = connection.cursor()

# Create Gaming Platforms Table
sql_select_query='SELECT gameName, gameID, gameReleaseDate, gamePlatformList FROM games WHERE gameReleaseDate BETWEEN ? AND ? ORDER BY gameReleaseDate ASC'
cursor.execute(sql_select_query, (today,next_week,))
data = cursor.fetchall()
connection.close()
youtubeBaseURL="https://www.youtube.com/watch?v="
connection.close()

# Creating a database to hold the link to the YouTube videos
connection = sqlite3.connect('gameVideos.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE if not exists gameVideos (gameID INT, gameName TEXT, gameReleaseDate TEXT, videoId INT, youtubeURL TEXT, videoTitle TEXT, videoDesc TEXT, PRIMARY KEY (gameID))')
connection.commit()

p=0

# Querying the YouTube API and looping through it for each game that was in the games.db date range
youtube = build('youtube', 'v3', developerKey=apiKey)
for x in range(len(data)):
    p=p+1
    if p < 100:
        youtubeSearch=data[x][0]
        print(youtubeSearch)
        try:
            request = youtube.search().list(
                part='snippet',
                #This is the Xbox channelId
                channelId='UCjBp_7RuDBUYbd1LegWEJ8g',
                type='video',
                q=youtubeSearch
                #q='Halo'
            )
            # Youtube returned the data in json format
            response = request.execute()
            videoItems=response['items']

            # Setting the VideoId and Details into arrays
            videoIds=videoItems[0]['id']
            videoDetails=videoItems[0]['snippet']

            # Game Info from Games db
            gameName=data[x][0]
            gameID=data[x][1]
            gameReleaseDate=data[x][2]

            # Reading the information from the objects
            videoId=videoIds['videoId']
            videoTitle=videoDetails['title']
            videoDesc=videoDetails['description']
            youtubeURL=youtubeBaseURL+videoId
            print("Video Game Name: ", gameName)
            print("Video Game Id: ", gameID)
            print("Video Title: ", videoTitle)
            print("Video Description: ", videoDesc)
            print("Release Date: ", gameReleaseDate)
            print("Video URL: ", youtubeURL)

            # Look to improve this by adding a Video Game Video ID to make each entry unique and store multiple game videos per video game
            cursor.execute("insert or replace into gameVideos (gameID, gameName, gameReleaseDate, videoId, youtubeURL, videoTitle, videoDesc) values (?,?,?,?,?,?,?)", (gameID, gameName, gameReleaseDate, videoId, youtubeURL, videoTitle, videoDesc))
        except:
            print("The game you searched for did not have any results on the Xbox Youtube channel.") 
            
    else:
        print("This would exceed the Youtube Quota so the program is ending")
connection.commit()

# Display the data that was added to the gameVideos database
print("Selecting data from sqldb")
cursor.execute('SELECT * FROM gameVideos')
gameVideoInfo= cursor.fetchall()

connection.close()
print(gameVideoInfo)
