from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.UpdateUserName import UpdateUserName
from action.UpdateUserPassword import UpdateUserPassword
from action.playlist_management.CreatePlaylist import CreatePlaylist
from action.playlist_management.RemoveSongFromPlaylist import RemoveSongFromPlaylist
from action.playlist_management.AddSongToPlaylist import AddSongToPlaylist
from action.playlist_management.ViewPlaylist import ViewPlaylist
from action.music_management.SearchMusics import SearchMusics
from action.music_management.SearchAlbums import SearchAlbums
from action.music_management.SearchArtists import SearchArtists
from action.music_management.ViewSongDetails import ViewSongDetails
from action.music_management.ViewAlbumDetails import ViewAlbumDetails
from action.music_management.ViewTop20Songs import ViewTop20Songs
from action.music_management.ViewPersonalizedPlaylist import ViewPersonalizedPlaylist
from action.music_management.ViewRandomSongs import ViewRandomSongs

class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        # 定義使用者可用的操作
        self.user_action = [
            SearchMusics("Search Songs"),
            ViewSongDetails("View Song Details"),
            SearchAlbums("Search Albums"),
            SearchArtists("Search Artists"),
            ViewAlbumDetails("View Album Details"),
            CreatePlaylist("Create Playlist"),
            AddSongToPlaylist("Add Song to Playlist"),
            RemoveSongFromPlaylist("Remove Song from Playlist"),
            ViewPlaylist("View Playlist"),
            ViewTop20Songs("View Top 20 Songs"),
            ViewPersonalizedPlaylist("View Personalized Playlist"),
            ViewRandomSongs("View Random Songs"),
            UpdateUserName("Update Username"),
            UpdateUserPassword("Update Password"),
            Logout("Logout"),
            Exit("Leave System")
        ]
