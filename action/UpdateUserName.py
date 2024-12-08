from .Action import Action
from DB_utils import update_user_name

class UpdateUserName(Action):
    def exec(self, conn, user):
        new_name = self.read_input(conn, "new user name")
        try:
            update_user_name(user.get_userid(), new_name)
            conn.send(f"User name successfully updated to {new_name}.\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
