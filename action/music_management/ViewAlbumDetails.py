from ..Action import Action
from DB_utils import view_album_details

class ViewAlbumDetails(Action):
    def exec(self, conn, user):
        album_id = self.read_input(conn, "album ID to view details")
        try:
            result = view_album_details(album_id)
            conn.send(f"\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
