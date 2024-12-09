from .Action import Action
from DB_utils import (
    update_song_name,
    update_song_artist,
    update_song_language,
    update_song_duration,
    add_song,
    delete_song
)

class UpdateSong(Action):
    def exec(self, conn, user):
        conn.send(
            "\n[INPUT] What do you want to do?\n"
            "  (1) Update Song Name\n"
            "  (2) Update Song Artist\n"
            "  (3) Update Song Language\n"
            "  (4) Update Song Duration\n"
            "  (5) Add a New Song\n"
            "  (6) Delete a Song\n"
            "---> ".encode('utf-8')
        )
        option = conn.recv(100).decode("utf-8").strip()

        if option == "1":  # 修改歌曲名稱
            song_id = self.read_input(conn, "song ID")
            new_name = self.read_input(conn, "new song name")
            try:
                update_song_name(song_id, new_name)
                conn.send(f"Song ID {song_id} successfully updated to name: {new_name}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "2":  # 修改歌曲歌手
            song_id = self.read_input(conn, "song ID")
            new_artist = self.read_input(conn, "new artist name")
            try:
                update_song_artist(song_id, new_artist)
                conn.send(f"Song ID {song_id} successfully updated to artist: {new_artist}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "3":  # 修改歌曲語言
            song_id = self.read_input(conn, "song ID")
            new_language = self.read_input(conn, "new language")
            try:
                update_song_language(song_id, new_language)
                conn.send(f"Song ID {song_id} successfully updated to language: {new_language}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "4":  # 修改歌曲時長
            song_id = self.read_input(conn, "song ID")
            new_duration = self.read_input(conn, "new duration (seconds)")
            try:
                update_song_duration(song_id, new_duration)
                conn.send(f"Song ID {song_id} successfully updated to duration: {new_duration} seconds.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "5":  # 新增一首歌
            song_name = self.read_input(conn, "song name")
            artist_name = self.read_input(conn, "artist name")
            language = self.read_input(conn, "language")
            duration = self.read_input(conn, "duration (seconds)")
            try:
                song_id = add_song(song_name, artist_name, language, duration)
                conn.send(f"New song added successfully with ID: {song_id}.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        elif option == "6":  # 刪除一首歌
            song_id = self.read_input(conn, "song ID to delete")
            try:
                delete_song(song_id)
                conn.send(f"Song ID {song_id} successfully deleted.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] {str(e)}\n".encode('utf-8'))

        else:
            conn.send("[ERROR] Invalid option. Please try again.\n".encode('utf-8'))
