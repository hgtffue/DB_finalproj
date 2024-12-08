# 將音樂加入播放清單
from ..Action import Action
from DB_utils import add_song_to_playlist

class AddSongToPlaylist(Action):
    def exec(self, conn, user):
        # 從用戶端獲取輸入
        playlist_id = self.read_input(conn, "playlist ID")
        song_id = self.read_input(conn, "song ID")

        try:
            # 呼叫資料庫層函數新增歌曲
            add_song_to_playlist(user.get_userid(), playlist_id, song_id)
            conn.send(f'\nSong ID {song_id} successfully added to Playlist ID {playlist_id}.\n'.encode('utf-8'))
        except Exception as e:
            # 如果有錯誤，回傳錯誤訊息
            conn.send(f'\n[ERROR] {str(e)}\n'.encode('utf-8'))
