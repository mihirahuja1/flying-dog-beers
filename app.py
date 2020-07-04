import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
###################################


import pandas as pd
import numpy as np
#!pip install spotipy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid= '388deb60ed474976aa449508fd1b52b9'
secret= '94817b949ec94ea1964833e07a432bde'
#Auth
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)



#sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#Get Playlist ID
pl_id = 'spotify:playlist:37i9dQZF1EpA4QQqqjQW8S'
offset = 0
track_ids = []
while True:
    response = sp.playlist_tracks(pl_id,
                                  offset=offset,
                                  fields='items.track.id,total')
    track_ids.append(response['items'])
    print(response['items'])
    offset = offset + len(response['items'])
    #print(offset, "/", response['total'])

    if len(response['items']) == 0:
        break
        
#Get track info        
def get_track_info(track_uri):
  track_info = sp.track(track_uri)
  artist_name = track_info['album']['artists'][0]['name']
  track_name = track_info['name']
  return track_name

song_df = pd.DataFrame()
list_of_songs = []

#Append songs to playlist
for i in range(0,len(track_ids[0])):
  print(track_ids[0][i]['track']['id'])
  list_of_songs.append(track_ids[0][i]['track']['id'])
    
songs_df = pd.DataFrame(list_of_songs,columns=['Track_URI'])
main_df = pd.DataFrame()
cnt=0

def create_audio_features_df(song):
  global cnt
  global main_df
  d = sp.audio_features(song)[0]
  new_df = pd.DataFrame(d.values())
  new_df = new_df.transpose()
  #print(new_df)
  if cnt == 0:
    main_df = new_df
  else:
    #print('here')
    x = pd.concat([main_df, new_df], ignore_index=True)
    main_df = x
  cnt+=1
  #return main_df
songs_df['Track_URI'].apply(lambda x: create_audio_features_df(x))  
#main_df.columns
main_df.columns = main_df.columns.astype(str)
main_df= main_df[['0','1','2','3','4','5','6','7','8','9','10']]
main_df.columns = ['danceability', 'energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo']
songs_df = pd.concat([songs_df, main_df], axis=1)
songs_df['Track_Name'] = songs_df['Track_URI'].apply(lambda x: get_track_info(x))
print(songs_df)
###################################



########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
