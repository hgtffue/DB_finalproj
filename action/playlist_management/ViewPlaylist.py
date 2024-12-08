from ..Action import Action
from DB_utils import search_public_playlists, view_playlist_details, view_user_playlists

class ViewPlaylist(Action):
    def exec(self, conn, user):
        conn.send(
            "\n[INPUT] What would you like to do?\n"
            "  (1) Search public playlists\n"
            "  (2) View playlist details\n"
            "  (3) View your playlists\n"
            "---> ".encode('utf-8')
        )
        option = conn.recv(100).decode("utf-8").strip()

        if option == "1":  # 搜尋公開播放清單
            keyword = self.read_input(conn, "keyword for public playlists")
            try:
                result = search_public_playlists(keyword)
                conn.send(f"\n{result}\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
        
        elif option == "2":  # 查看播放清單詳細資訊
            playlist_id = self.read_input(conn, "playlist ID to view")
            try:
                result = view_playlist_details(playlist_id)
                conn.send(f"\n{result}\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
        
        elif option == "3":  # 查看用戶自己的播放清單
            try:
                result = view_user_playlists(user.get_userid())
                conn.send(f"\n{result}\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
        
        else:
            conn.send("[ERROR] Invalid option. Please try again.\n".encode('utf-8'))
