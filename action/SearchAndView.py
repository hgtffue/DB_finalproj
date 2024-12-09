from .Action import Action
from DB_utils import (
    search_albums,
    search_artists,
    search_songs,
    view_album_details,
    view_song_details
)


class SearchAndView(Action):
    def exec(self, conn, user):
        # 显示功能菜单
        conn.send(
            "\n[INPUT] What do you want to do?\n"
            "  (1) Search Albums\n"
            "  (2) Search Artists\n"
            "  (3) Search Songs\n"
            "  (4) View Album Details\n"
            "  (5) View Song Details\n"
            "---> ".encode('utf-8')
        )

        option = conn.recv(100).decode("utf-8").strip()

        if option == "1":  # 搜索专辑
            self.search_albums(conn)
        elif option == "2":  # 搜索艺术家
            self.search_artists(conn)
        elif option == "3":  # 搜索歌曲
            self.search_songs(conn)
        elif option == "4":  # 查看专辑详情
            self.view_album_details(conn)
        elif option == "5":  # 查看歌曲详情
            self.view_song_details(conn)
        else:
            conn.send("[ERROR] Invalid option. Please try again.\n".encode('utf-8'))

    def search_albums(self, conn):
        """搜索专辑"""
        keyword = self.read_input(conn, "keyword to search for albums")
        try:
            result = search_albums(keyword)
            conn.send(f"\nSearch Results for Albums:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

    def search_artists(self, conn):
        """搜索艺术家"""
        keyword = self.read_input(conn, "keyword to search for artists")
        try:
            result = search_artists(keyword)
            conn.send(f"\nSearch Results for Artists:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

    def search_songs(self, conn):
        """搜索音乐"""
        keyword = self.read_input(conn, "keyword to search for songs")
        try:
            result = search_songs(keyword)
            conn.send(f"\nSearch Results for Songs:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

    def view_album_details(self, conn):
        """查看专辑详情"""
        album_id = self.read_input(conn, "album ID to view details")
        try:
            result = view_album_details(album_id)
            conn.send(f"\nAlbum Details:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

    def view_song_details(self, conn):
        """查看歌曲详情"""
        song_id = self.read_input(conn, "song ID to view details")
        try:
            result = view_song_details(song_id)
            conn.send(f"\nSong Details:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
