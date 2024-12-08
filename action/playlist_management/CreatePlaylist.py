from ..Action import Action
from DB_utils import create_playlist

class CreatePlaylist(Action):
    def exec(self, conn, user):
        # 讀取播放清單名稱和權限
        playlist_name = self.read_input(conn, "playlist name")
        permissions = self.read_input(conn, "permissions (Public/Private)")

        # 檢查權限是否有效
        while permissions not in ["Public", "Private"]:
            conn.send("[INPUT]Invalid permission. Please enter 'Public' or 'Private': ".encode('utf-8'))
            permissions = self.read_input(conn, "permissions (Public/Private)")

        print({'user_id': user.get_userid(), 'playlist_name': playlist_name, 'permissions': permissions})
        # 呼叫資料庫層函數
        try:
            playlist_id = create_playlist(user.get_userid(), playlist_name, permissions)
            conn.send(f'\nPlaylist created successfully! New Playlist ID: {playlist_id}\n'.encode('utf-8'))
        except Exception as e:
            conn.send(f'\n[ERROR] {str(e)}\n'.encode('utf-8'))
