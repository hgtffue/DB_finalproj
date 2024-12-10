from ..Action import Action
from DB_utils import view_personalized_playlist
import datetime

class ViewPersonalizedPlaylist(Action):
    def exec(self, conn, user):
        # 獲取當前日期
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # current_date = ("2024-11-29")
        try:
            # 呼叫資料庫函數，取得個人化歌單資訊
            result = view_personalized_playlist(user.get_userid(), current_date)
            conn.send(f"\nYour Personalized Playlist for {current_date}:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
