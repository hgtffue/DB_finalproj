from ..Action import Action
from DB_utils import update_user_role

class UpdateUserRole(Action):
    def exec(self, conn, user):
        user_id = self.read_input(conn, "user ID to update role for")
        new_role = self.read_input(conn, "new role (e.g., 'Admin', 'User')")

        try:
            # 呼叫資料庫函數更新用戶角色
            update_user_role(user_id, new_role)
            conn.send(f"User ID {user_id} successfully updated to role: {new_role}.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
