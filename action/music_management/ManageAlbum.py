from ..Action import Action
from DB_utils import (
    view_all_albums,
    add_album,
    delete_album,
    add_songs_to_album,
    remove_song_from_album
)

class ManageAlbum(Action):
    def exec(self, conn, user):
        conn.send(
            "\n[INPUT] What do you want to do?\n"
            "  (1) View All Albums\n"
            "  (2) Add New Album\n"
            "  (3) Delete an Album\n"
            "  (4) Add Songs to an Album\n"
            "  (5) Remove a Song from an Album\n"
            "---> ".encode('utf-8')
        )
        option = conn.recv(100).decode("utf-8").strip()

        if option == "1":  # 浏览所有专辑
            try:
                result = view_all_albums()
                conn.send(f"\nAll Albums:\n{result}\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "2":  # 新增专辑
            album_name = self.read_input(conn, "new album name")
            try:
                album_id = add_album(album_name)
                conn.send(f"New album added successfully with ID: {album_id}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "3":  # 删除专辑
            album_id = self.read_input(conn, "album ID to delete")
            try:
                delete_album(album_id)
                conn.send(f"Album ID {album_id} successfully deleted.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "4":  # 将歌曲加入专辑
            album_id = self.read_input(conn, "album ID")
            song_ids = self.read_input(conn, "comma-separated song IDs").split(',')
            try:
                add_songs_to_album(album_id, song_ids)
                conn.send(f"Songs successfully added to album ID {album_id}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "5":  # 从专辑中移除歌曲
            album_id = self.read_input(conn, "album ID")
            song_id = self.read_input(conn, "song ID to remove")
            try:
                remove_song_from_album(song_id, album_id)
                conn.send(f"Song ID {song_id} successfully removed from album ID {album_id}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        else:
            conn.send("[ERROR] Invalid option. Please try again.\n".encode('utf-8'))
