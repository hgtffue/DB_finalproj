# 新增音樂
from ..Action import Action
from DB_utils import append_music

class AddMusic(Action):
    def exec(self, conn, **kwargs):
        # 讀取用戶輸入
        song_name = self.read_input(conn, "song name")
        artist_name = self.read_input(conn, "artist name")
        language = self.read_input(conn, "language")
        duration_in_seconds = self.read_input(conn, "duration (in seconds)")

        # 確保 duration 是有效數字
        while not duration_in_seconds.isdigit():
            conn.send("[INPUT]Duration must be a numeric value. Please enter again: ".encode('utf-8'))
            duration_in_seconds = self.read_input(conn, "duration (in seconds)")

        # 呼叫 DB 函數新增音樂
        music_id = append_music(song_name, artist_name, language, int(duration_in_seconds))

        # 向客戶端返回操作成功訊息
        conn.send(f'\nCreate new music successfully! New Music ID: {music_id}\n'.encode('utf-8'))