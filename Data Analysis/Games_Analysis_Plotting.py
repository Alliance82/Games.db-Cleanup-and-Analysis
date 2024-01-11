# Created By Alliance82
# Created On 12/28/23
# This was created to explore the data that was previously pulled from the RAWG.io API
import numpy as np
import pandas as pd
import sqlite3, json
#import time, datetime as DT
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#Connect to SQL Lite DB
#today = DT.date.today()
connection = sqlite3.connect('games.db')

# Connects to the games.db file and describes the data the is returned
df = pd.read_sql(sql="SELECT * FROM games", con=connection)
print(df.describe())

# Prints out all of the columns in the games.db file
for col in df:
    print(col)

# Redefines the dataframe and only returns the columns of data for Release Date, Game Name and Genres
df = pd.read_sql(sql="SELECT gameName, gameReleaseDate, gameGenreList FROM games", con=connection)
print(df)
print(df.describe())

# Split the gameGenreList column by comma and create a new dataframe
new_df = df['gameGenreList'].str.split(',', expand=True)
# Rename the columns of the new dataframe
new_df.columns = ['gameGenreList_' + str(col) for col in new_df.columns]
# Concatenate the original dataframe with the new one
df = pd.concat([df, new_df], axis=1)
# Drop the original gameGenreList column
df = df.drop('gameGenreList', axis=1)
# The below condenses the multiple Genre columns into a single column creating a new row
df = pd.melt(df, id_vars=['gameName', 'gameReleaseDate'], value_vars=new_df.columns)
# Drop the rows with missing values
df = df.dropna()
# Drop the variable column
df = df.drop('variable', axis=1)
# Rename the value column to gameGenreList
df = df.rename(columns={'value': 'gameGenreList'})
# Convert the gameReleaseDate column to a numeric type
#df['gameReleaseDate'] = pd.to_numeric(df['gameReleaseDate'])
# Convert the gameReleaseDate column from UNIX format to datetime format
#df['gameReleaseDate'] = pd.to_datetime(df['gameReleaseDate'], unit='s')
# Trim the column that was previously comma delimited in case there is whitespace
df['gameGenreList'] = df['gameGenreList'].str.strip()
df['gameReleaseDate'] = pd.to_datetime(df['gameReleaseDate'], format='%Y-%m-%d')

# Setting up the x, y plot
plt.plot(df['gameReleaseDate'],df['gameGenreList'], 'o')
plt.xlabel('Release Date')
plt.ylabel('Genre(s)')
plt.title('Video Game Release Dates vs Genres')
# Prettier plotting with seaborn
sns.set(font_scale=1.5)
# Ticks instead of whitegrid in order to demonstrate changes to plot ticks better
sns.set_style("ticks")
# Create a date formatter object
date_form = mdates.DateFormatter("%m-%d-%Y")
# Set the date formatter for the x-axis
plt.gca().xaxis.set_major_formatter(date_form)
# Create a date locator object
date_loc = mdates.AutoDateLocator()
# Set the date locator for the x-axis
plt.gca().xaxis.set_major_locator(date_loc)
# rotate y tick labels by 45 degrees
plt.yticks(rotation=45)
plt.xticks(rotation=45)
plt.show()
