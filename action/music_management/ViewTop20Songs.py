from ..Action import Action
from DB_utils import view_top_20_songs
import datetime

class ViewTop20Songs(Action):
    def exec(self, conn, user):
        # 獲取當前日期(可能要自己設置一個日期)
        # current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_date = '2024-11-24'
        try:
            # 呼叫資料庫函數，取得排行榜資訊
            result = view_top_20_songs(current_date)
            conn.send(f"\nTop 20 Songs in the Last 7 Days:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
