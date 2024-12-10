from .Action import Action
from DB_utils import create_playlist, add_song_to_playlist, remove_song_from_playlist
from threading import Lock

create_playlist_lock = Lock()


class PlaylistManagement(Action):
    def exec(self, conn, user):
        # 显示可用操作
        conn.send(
            "\n[INPUT] What do you want to do?\n"
            "  (1) Create Playlist\n"
            "  (2) Add Song to Playlist\n"
            "  (3) Remove Song from Playlist\n"
            "---> ".encode('utf-8')
        )

        option = conn.recv(100).decode("utf-8").strip()

        if option == "1":  # 创建播放清单
            self.create_playlist(conn, user)
        elif option == "2":  # 将音乐加入播放清单
            self.add_song_to_playlist(conn, user)
        elif option == "3":  # 从播放清单移除音乐
            self.remove_song_from_playlist(conn, user)
        else:
            conn.send("[ERROR] Invalid option. Please try again.\n".encode('utf-8'))

    def create_playlist(self, conn, user):
        """创建播放清单"""
        create_playlist_lock.acquire()
        playlist_name = self.read_input(conn, "playlist name")
        permissions = self.read_input(conn, "permissions (Public/Private)")

        # 检查权限是否有效
        while permissions not in ["Public", "Private"]:
            conn.send("[INPUT]Invalid permission. Please enter 'Public' or 'Private': ".encode('utf-8'))
            permissions = self.read_input(conn, "permissions (Public/Private)")

        try:
            playlist_id = create_playlist(user.get_userid(), playlist_name, permissions)
            conn.send(f'\nPlaylist created successfully! New Playlist ID: {playlist_id}\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\n[ERROR] {str(e)}\n'.encode('utf-8'))
        create_playlist_lock.release()

    def add_song_to_playlist(self, conn, user):
        """将音乐加入播放清单"""
        create_playlist_lock.acquire()
        playlist_id = self.read_input(conn, "playlist ID")
        song_id = self.read_input(conn, "song ID")

        try:
            add_song_to_playlist(user.get_userid(), playlist_id, song_id)
            conn.send(f'\nSong ID {song_id} successfully added to Playlist ID {playlist_id}.\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\n[ERROR] {str(e)}\n'.encode('utf-8'))
        create_playlist_lock.release()

    def remove_song_from_playlist(self, conn, user):
        """从播放清单移除音乐"""
        create_playlist_lock.acquire()
        playlist_id = self.read_input(conn, "playlist ID")
        song_id = self.read_input(conn, "song ID")

        try:
            remove_song_from_playlist(user.get_userid(), playlist_id, song_id)
            conn.send(f'\nSong ID {song_id} successfully removed from Playlist ID {playlist_id}.\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\n[ERROR] {str(e)}\n'.encode('utf-8'))
        create_playlist_lock.release()
