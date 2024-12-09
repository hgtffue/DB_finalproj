from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.UpdateUserName import UpdateUserName
from action.UpdateUserPassword import UpdateUserPassword
from action.SearchAndView import SearchAndView
from action.ViewPlaylist import ViewPlaylist
from action.music_management.ViewTop20Songs import ViewTop20Songs
from action.music_management.ViewPersonalizedPlaylist import ViewPersonalizedPlaylist
from action.music_management.ViewRandomSongs import ViewRandomSongs
from action.PlaylistManagement import PlaylistManagement

class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        # 定義使用者可用的操作
        self.user_action = [
            SearchAndView("Search and View"),
            PlaylistManagement("Playlist Management"),
            ViewPlaylist("View Playlist"),
            ViewTop20Songs("View Top 20 Songs"),
            ViewPersonalizedPlaylist("View Personalized Playlist"),
            ViewRandomSongs("View Random Songs"),
            UpdateUserName("Update Username"),
            UpdateUserPassword("Update Password"),
            Logout("Logout"),
            Exit("Leave System")
        ]
