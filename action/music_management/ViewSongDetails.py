from ..Action import Action
from DB_utils import view_song_details

class ViewSongDetails(Action):
    def exec(self, conn, user):
        song_id = self.read_input(conn, "song ID to view details")
        try:
            result = view_song_details(song_id)
            conn.send(f"\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
