import os
import spotipy


class SpotifyConnect():
    """Connect to spotify API
    
    Functionality:
        * Connect to spotify API
        * Search for song data
        * Create a playlist
        * Add tracks to that playist
    
    Attributes:
        client_id: spotify client id from spotify for dev app
        client_secret: spotify client secret from spotify for dev app
        redirect_uri: where to redirect for authentication
        user_id: the spotify user ID we get back after authentication
        spotify_instance: reusable spotipy.Spotify class for later functions
    """
    
    def __init__(self) -> None:
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
        self.user_id = None
        self.spotify_instance = self._login()
        
        
    def _get_credentials(self) -> spotipy.oauth2.SpotifyOAuth:
        """Connect to spotify with spotipy oauth"""
        spotify_auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=self.client_id, 
                                              client_secret=self.client_secret, 
                                              redirect_uri=self.redirect_uri,
                                              scope="playlist-modify-private",
                                              show_dialog=True,)
        return spotify_auth_manager
        
    def _login(self) -> spotipy.Spotify:
        """Create spotipy.Spotify class and set the user id"""
        spotify = spotipy.Spotify(auth_manager=self._get_credentials())
        self.user_id = spotify.current_user()["id"]
        return spotify
        
    def get_song_data(self, track:str, artist:str, year:str) -> list:
        """Search spotify for specific tracks based on artist, track name and year"""
        song_data = self.spotify_instance.search(q=f"track: {track} artist: {artist} year: {year}", 
                                                 type="track",)
        return song_data

    def create_playlist(self, year_month_date:str) -> spotipy.Spotify.user_playlist_create:
        """Create a new playlist in current user id account"""
        return self.spotify_instance.user_playlist_create(user=self.user_id,
                                                          public=False,
                                                          name=f"Top 100 Songs - {year_month_date}",)
    
    def add_tracks_to_playlist(self, playlist_id:str, songs_to_add:list) -> None:
        """Add tracks to playlist in current user id account based on list of tracks"""
        self.spotify_instance.user_playlist_add_tracks(user=self.user_id, 
                                                       playlist_id=playlist_id, 
                                                       tracks=songs_to_add,)
        print("Success")
