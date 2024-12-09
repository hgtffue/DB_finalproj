from ..Action import Action
from DB_utils import create_personalized_playlist

class CreatePersonalizedPlaylist(Action):
    def exec(self, conn, user):
        # 输入用户 ID、管理员 ID 和推荐日期
        target_user_id = self.read_input(conn, "user ID to create playlist for")
        admin_id = self.read_input(conn, "admin/system ID creating the playlist")
        input_date = self.read_input(conn, "date for the playlist (YYYY-MM-DD)")

        # 输入推荐歌曲 ID
        conn.send("[INPUT] Enter 20 comma-separated song IDs for recommendation: ".encode('utf-8'))
        song_ids_input = conn.recv(1024).decode('utf-8').strip()
        song_ids = song_ids_input.split(',')

        if len(song_ids) != 20:
            conn.send("[ERROR] Please provide exactly 20 song IDs.\n".encode('utf-8'))
            return

        try:
            # 调用数据库函数创建推荐歌单
            result = create_personalized_playlist(target_user_id, admin_id, input_date, song_ids)
            conn.send(f"{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
