from ..Action import Action
from DB_utils import list_all_users

class ListAllUsers(Action):
    def exec(self, conn, user):
        try:
            # 呼叫資料庫函數，取得所有用戶列表
            result = list_all_users()
            conn.send(f"\nAll Users:\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
