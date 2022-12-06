import webbrowser

from top100 import Top100Song
from spotify import SpotifyConnect
from dotenv import load_dotenv

load_dotenv()

SONGS = Top100Song()
SPOTIFY = SpotifyConnect()

def get_song_uris(artist_and_song_list:list) -> list:
    """Create list of URIs for """
    song_uris = []
    for artist_and_song in artist_and_song_list:
        song_data = SPOTIFY.get_song_data(artist_and_song['song'], artist_and_song['artist'], SONGS.year)
        try:
            song_uri = song_data['tracks']['items'][0]['uri']
            song_uris.append(song_uri)
        except IndexError:
            continue
    return song_uris

def open_playlist_link(url:str) -> None:
    """Open playlist URL once it is created"""
    mac_chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(mac_chrome_path).open(url)
    

if __name__ == "__main__":
    # Create playlist
    playlist_id = SPOTIFY.create_playlist(year_month_date=SONGS.timeframe)
    
    # Add tracks to playlist
    SPOTIFY.add_tracks_to_playlist(playlist_id=playlist_id["id"], songs_to_add=get_song_uris(SONGS.get_top_100_songs()))

    # Get URL for new playlist
    new_playlist_url = playlist_id['external_urls']['spotify']
    
    # Open URL of new playlist
    open_playlist_link(new_playlist_url)
