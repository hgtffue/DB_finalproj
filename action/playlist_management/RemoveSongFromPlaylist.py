from ..Action import Action
from DB_utils import remove_song_from_playlist

class RemoveSongFromPlaylist(Action):
    def exec(self, conn, user):
        # 從用戶端獲取輸入
        playlist_id = self.read_input(conn, "playlist ID")
        song_id = self.read_input(conn, "song ID")

        try:
            # 調用資料庫層函數移除歌曲
            remove_song_from_playlist(user.get_userid(), playlist_id, song_id)
            conn.send(f'\nSong ID {song_id} successfully removed from Playlist ID {playlist_id}.\n'.encode('utf-8'))
        except Exception as e:
            # 如果有錯誤，回傳錯誤訊息
            conn.send(f'\n[ERROR] {str(e)}\n'.encode('utf-8'))
