from ..Action import Action
from DB_utils import search_artists

class SearchArtists(Action):
    def exec(self, conn, user):
        keyword = self.read_input(conn, "keyword to search for artists")
        try:
            result = search_artists(keyword)
            conn.send(f"\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
