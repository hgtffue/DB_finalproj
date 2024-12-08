from .Action import Action
from DB_utils import verify_old_password, update_user_password

class UpdateUserPassword(Action):
    def exec(self, conn, user):
        old_password = self.read_input(conn, "current password")
        new_password = self.read_input(conn, "new password")

        try:
            # 驗證舊密碼
            if not verify_old_password(user.get_userid(), old_password):
                conn.send("[ERROR] Current password is incorrect.\n".encode('utf-8'))
                return

            # 更新密碼
            update_user_password(user.get_userid(), new_password)
            conn.send("Password successfully updated.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
