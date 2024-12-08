from ..Action import Action
from DB_utils import search_albums

class SearchAlbums(Action):
    def exec(self, conn, user):
        keyword = self.read_input(conn, "keyword to search for albums")
        try:
            result = search_albums(keyword)
            conn.send(f"\n{result}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))
