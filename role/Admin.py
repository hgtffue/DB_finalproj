# 管理員邏輯
from .User import User

from action.user_management.ListAllUsers import ListAllUsers
from action.user_management.UpdateUserRole import UpdateUserRole
from action.user_management.QueryPlayHistory import QueryPlayHistory
from action.user_management.CreatePersonalizedPlaylist import CreatePersonalizedPlaylist
from action.UpdateSong import UpdateSong
from action.music_management.ManageAlbum import ManageAlbum


class Admin(User):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)
        self.user_action =  super().get_available_action() + [
                                ListAllUsers("List All Users"),
                                UpdateUserRole("Update User Role"),
                                UpdateSong("Update song information"),
                                QueryPlayHistory("Query play history"),
                                ManageAlbum("Manage Album"),
                                CreatePersonalizedPlaylist("Create Personalized Playlist")
                            ]
        

    def isAdmin(self):
        return True