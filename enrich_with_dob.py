import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from datetime import datetime

allPickleFiles = []
df = pd.DataFrame()

for file in os.listdir():
    if ".pkl" in file:
        allPickleFiles.append(file)
        
for file in allPickleFiles:
    localDf = pd.read_pickle(file)
    concat = [df, localDf]
    df = pd.concat(concat)

df.drop_duplicates(subset=['Date', 'Event Name', 'Event Rounds', 'Round', 'White Name',
       'Black Name', 'Result', 'White ELO', 'Black ELO', 'Moves',
       'White Av CP Loss', 'Black Av CP Loss', 'Analysis Depth'], inplace=True)


df = df.dropna(subset=['White Name'], axis=0)
df = df.dropna(subset=['Black Name'], axis=0)
df = df.dropna(subset=['White ELO'], axis=0)
df = df.dropna(subset=['Black ELO'], axis=0)
df['White ELO'] = df['White ELO'].apply(lambda x: int(x))
df['Black ELO'] = df['Black ELO'].apply(lambda x: int(x))
df['Moves'] = df['Moves'].apply(lambda x: int(x))
df['White Av CP Loss'] = df['White Av CP Loss'].apply(lambda x: float(x))
df['Black Av CP Loss'] = df['Black Av CP Loss'].apply(lambda x: float(x))
df['Analysis Depth'] = df['Analysis Depth'].apply(lambda x: int(x))
df['Date'] = df['Date'].apply(lambda x: str(x).replace(".", "-").replace("??", "01")[:10])
df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))

dob_dict = { "Carlsen": datetime(1990,11,30), 
"Esipenko":datetime(2002,3,22), 
"Firouzja":datetime(2003,6,18),
"Rausis":datetime(1961,4,7),
"Erigaisi":datetime(2003,9,3),
"Gukesh":datetime(2006,5,29),
"Keymer":datetime(2004,11,15),
"Pragg":datetime(2005,8,10),
"Caruana":datetime(1992,7,30),
"Niemann":datetime(2003,6,20),
}

# df.assign(age = lambda x: (x.Date - dob_dict['Niemann']).dt.days)
# df['Age'] = (df['Date'] - dob_dict['Niemann']).dt.days



for key in dob_dict:
    # if (dob_dict[df['White Name']]):
    df['Age White'] = np.where(df['White Name'].str.contains(key), (df['Date'] - dob_dict[key]).dt.days, 0)
    df['Age Black'] = np.where(df['Black Name'].str.contains(key), (df['Date'] - dob_dict[key]).dt.days, 0)

df.to_pickle('games_centipawn_age.pkl')
df.to_csv('teste.csv')