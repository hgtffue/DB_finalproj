from ..Action import Action
from DB_utils import query_user_play_history

class QueryPlayHistory(Action):
    def exec(self, conn, user):
        # 获取用户输入的目标用户 ID
        target_user_id = self.read_input(conn, "user ID to query play history for")
        try:
            # 调用数据库函数获取播放记录
            result = query_user_play_history(target_user_id)
            if result.strip():
                conn.send(f"\nPlay History for User ID {target_user_id}:\n{result}\n".encode('utf-8'))
            else:
                conn.send(f"\nNo play history found for User ID {target_user_id}.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
