from ..Action import Action
from DB_utils import view_random_songs
import random

class ViewRandomSongs(Action):
    def exec(self, conn, user):
        # 隨機生成 20 個歌曲 ID（假設歌曲 ID 在 1-100 范圍內）
        random_ids = random.sample(range(1, 101), 20)
        try:
            result = view_random_songs(random_ids)
            conn.send(f"\nRandom 20 Songs:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
