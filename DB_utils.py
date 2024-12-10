# 資料庫操作工具
import sys
import psycopg2
import psycopg2.extras
from tabulate import tabulate
from threading import Lock

DB_NAME = "QQbeat"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

cur = None
db = None
create_event_lock = Lock()

def db_connect():
    exit_code = 0
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='Ll125844688', 
                              host=DB_HOST, port=DB_PORT)
        print("Successfully connect to DBMS.")
        global cur
        cur = db.cursor()
        return db
        
    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    # finally:
    #     if db is not None:
    #         db.close()
    sys.exit(exit_code)

def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")   


# ============================= System function =============================
def db_register_user(username, pwd, email):
    cmd =   """
            insert into "users" (uname, password, email) values (%s, %s, %s)
            RETURNING uid;
            """
    cur.execute(cmd, [username, pwd, email])
    userid = cur.fetchone()[0]
    print(f"Register user {username} with userid {userid}")

    cmd =   """
            insert into "roles" (roles_uid, roles) VALUES (%s, 'User');
            """
    cur.execute(cmd, [userid])
    db.commit()

def fetch_user(userid): 
    cmd =   """
            select * 
            from "users" u
            join "roles" r on u.uid = r.roles_uid
            where u.uid = %s;
            """
    cur.execute(cmd, [userid])

    rows = cur.fetchall()
    if not rows:
        return None, None, None, None, None
    else:
        print(rows)
        isUser = False
        isAdmin = False
        for row in rows:
            userid, username, email, pwd, userid, role = row
            
            if role == 'User':
                isUser = True
            elif role == 'Admin':
                isAdmin = True

    return username, pwd, email, isUser, isAdmin

def username_exist(username):
    
    cmd =   """
            select count(*) from "users"
            where uname = %s;
            """
    # print(cur.mogrify(cmd, [username]))
    cur.execute(cmd, [username])


    count = cur.fetchone()[0]
    return count > 0

def userid_exist(userid):
    cmd =   """
            select count(*) 
            from "users"
            where uid = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    return count > 0


# ============================= function for User =============================

def search_songs(keyword):
    """
    搜尋歌曲，按照平均播放次數排序。
    :param keyword: 搜尋的關鍵字
    :return: 格式化的歌曲列表
    """
    query = """
        SELECT 
            m.mname, 
            m.artist, 
            m.language, 
            m.duration, 
            COALESCE(SUM(p.play_duration) / NULLIF(SUM(m.duration), 0), 0) AS avg_play_times,
            m.mid
        FROM 
            music m
        LEFT JOIN 
            play p ON m.mid = p.play_mid
        WHERE 
            LOWER(m.mname) LIKE LOWER(%s)
        GROUP BY 
            m.mid
        ORDER BY 
            avg_play_times DESC;
    """
    cur.execute(query, [f"{keyword}%"])
    return print_table(cur)

def search_albums(keyword):
    """
    搜尋專輯，按照平均播放次數排序。
    :param keyword: 搜尋的關鍵字
    :return: 格式化的專輯列表
    """
    query = """
        SELECT 
            a.aname, 
            COALESCE(SUM(play.play_duration) / NULLIF(SUM(m.duration), 0), 0) AS avg_play_count,
            a.aid
        FROM 
            album a
        JOIN 
            in_a ia ON a.aid = ia.a_aid
        JOIN 
            music m ON ia.a_mid = m.mid
        LEFT JOIN 
            play ON m.mid = play.play_mid
        WHERE 
            LOWER(a.aname) LIKE LOWER(%s)
        GROUP BY 
            a.aid
        ORDER BY 
            avg_play_count DESC;
    """
    cur.execute(query, [f"{keyword}%"])
    return print_table(cur)

def search_artists(keyword):
    """
    搜尋歌手，按照平均播放次數排序。
    :param keyword: 搜尋的關鍵字
    :return: 格式化的歌手列表
    """
    query = """
        SELECT 
            m.artist, 
            COALESCE(SUM(p.play_duration) / NULLIF(SUM(m.duration), 0), 0) AS avg_play_times
        FROM 
            music m
        LEFT JOIN 
            play p ON m.mid = p.play_mid
        WHERE 
            LOWER(m.artist) LIKE LOWER(%s)
        GROUP BY 
            m.artist
        ORDER BY 
            avg_play_times DESC;
    """
    cur.execute(query, [f"{keyword}%"])
    return print_table(cur)

def view_song_details(song_id):
    """
    查看指定歌曲的相關資訊。
    :param song_id: 歌曲 ID
    :return: 格式化的歌曲資訊
    """
    query = """
        SELECT 
            m.mname, 
            m.artist, 
            m.language, 
            m.duration, 
            a.aname AS album_name
        FROM 
            music m
        LEFT JOIN 
            in_a ia ON m.mid = ia.a_mid
        LEFT JOIN 
            album a ON ia.a_aid = a.aid
        WHERE 
            m.mid = %s;
    """
    cur.execute(query, [song_id])
    return print_table(cur)

def view_album_details(album_id):
    """
    查看指定專輯的相關資訊。
    :param album_id: 專輯 ID
    :return: 格式化的專輯資訊
    """
    query = """
        SELECT 
            a.aname AS album_name, 
            m.mname AS song_name, 
            m.artist, 
            m.language, 
            m.duration,
            m.mid
        FROM 
            album a
        LEFT JOIN 
            in_a ia ON a.aid = ia.a_aid
        LEFT JOIN 
            music m ON ia.a_mid = m.mid
        WHERE 
            a.aid = %s
        ORDER BY 
            m.mid ASC;
    """
    cur.execute(query, [album_id])
    return print_table(cur)


def create_playlist(user_id, playlist_name, permissions):
    """
    將新的播放清單插入資料庫。
    :param user_id: 使用者 ID
    :param playlist_name: 播放清單名稱
    :param permissions: 播放清單權限 ('Public' 或 'Private')
    :return: 新的播放清單 ID
    """
    create_event_lock.acquire()
    try:
        query = """
            DO $$
            BEGIN
                -- 檢查 PLAYLIST 表中的最大 pid 並同步序列值
                PERFORM setval('playlist_pid_seq', COALESCE((SELECT MAX(pid) FROM PLAYLIST), 0));
            END $$;

            INSERT INTO "playlist" (pname, created_by_uid, permissions)
            VALUES (%s, %s, %s)
            RETURNING pid;
        """
        cur.execute(query, [playlist_name, user_id, permissions])
        print("test")
        pid = cur.fetchone()[0]
        print(f"Playlist created successfully! New Playlist ID: {pid}")
        db.commit()
        return pid
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create playlist: {str(e)}")
    finally:
        create_event_lock.release()

def add_song_to_playlist(user_id, playlist_id, song_id):
    """
    將歌曲新增到播放清單。
    :param user_id: 使用者 ID
    :param playlist_id: 播放清單 ID
    :param song_id: 歌曲 ID
    :raises: Exception 如果新增失敗，回傳錯誤訊息。
    """
    create_event_lock.acquire()
    try:
        query = """
            INSERT INTO "in_p" (p_mid, p_pid, p_createdby_uid, index_in_playlist)
            VALUES (
                %s, 
                %s, 
                %s, 
                COALESCE(
                    (SELECT MAX(index_in_playlist) 
                     FROM "in_p" 
                     WHERE p_pid = %s), 
                    0
                ) + 1
            );
        """
        cur.execute(query, [song_id, playlist_id, user_id, playlist_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add song to playlist: {str(e)}")
    create_event_lock.release()



def remove_song_from_playlist(user_id, playlist_id, song_id):
    """
    從播放清單中移除指定歌曲。
    :param user_id: 使用者 ID
    :param playlist_id: 播放清單 ID
    :param song_id: 歌曲 ID
    :raises: Exception 如果刪除失敗，回傳錯誤訊息。
    """
    try:
        query = """
            DELETE FROM "in_p"
            WHERE p_mid = %s AND p_pid = %s AND p_createdby_uid = %s;
        """
        cur.execute(query, [song_id, playlist_id, user_id])
        db.commit()

        # 確認是否有影響到的記錄，若無，可能是無效的條件
        if cur.rowcount == 0:
            raise Exception("No matching song found in the playlist or insufficient permissions.")
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove song from playlist: {str(e)}")


def view_user_playlists(user_id):
    """
    查看用戶的所有播放清單。
    :param user_id: 用戶 ID
    :return: 格式化的用戶播放清單
    """
    query = """
        SELECT 
            pid, 
            pname, 
            permissions 
        FROM 
            playlist
        WHERE 
            created_by_uid = %s;
    """
    cur.execute(query, [user_id])
    return print_table(cur)

def view_playlist_details(playlist_id):
    """
    查看播放清單的歌曲資訊。
    :param playlist_id: 播放清單 ID
    :return: 格式化的播放清單內容
    """
    create_event_lock.acquire()
    query = """
        SELECT 
            p.pname AS playlist_name,
            m.mid,
            m.mname AS song_name,
            m.artist AS artist,
            m.duration AS duration,
            ip.index_in_playlist AS song_order
        FROM 
            playlist p
        JOIN 
            in_p ip ON p.pid = ip.p_pid
        JOIN 
            music m ON ip.p_mid = m.mid
        WHERE 
            p.pid = %s
        ORDER BY 
            ip.index_in_playlist;
    """
    cur.execute(query, [playlist_id])
    create_event_lock.release()
    return print_table(cur)
    

def search_public_playlists(keyword):
    """
    搜尋公開播放清單。
    :param keyword: 關鍵字（部分名稱匹配）
    :return: 格式化的公開播放清單資訊
    """
    query = """
        SELECT 
            p.pname, 
            COALESCE(SUM(play.play_duration) / NULLIF(SUM(m.duration), 0), 0) AS avg_play_count,
            p.pid
        FROM 
            playlist p
        JOIN 
            in_p ip ON p.pid = ip.p_pid
        JOIN 
            music m ON ip.p_mid = m.mid
        LEFT JOIN 
            play ON m.mid = play.play_mid
        WHERE 
            LOWER(p.pname) LIKE LOWER(%s) AND p.permissions = 'public'
        GROUP BY 
            p.pid
        ORDER BY 
            avg_play_count DESC;
    """
    cur.execute(query, [f"{keyword}%"])
    return print_table(cur)

def view_top_20_songs(current_date):
    """
    瀏覽 7 天內線上的 Top 20 歌曲。
    :param current_date: 當前日期（格式：'YYYY-MM-DD'）
    :return: 格式化的排行榜資訊
    """
    query = """
        SELECT 
            m.mname, 
            m.artist, 
            m.mid,
            COALESCE(SUM(play.play_duration) / NULLIF(SUM(m.duration), 0), 0) AS avg_play_count
        FROM 
            music m
        LEFT JOIN 
            play ON m.mid = play.play_mid
        WHERE 
            play.play_datetime >= (%s::DATE - INTERVAL '7 days')
            AND play.play_datetime <= %s::DATE
        GROUP BY 
            m.mid
        ORDER BY 
            avg_play_count DESC
        LIMIT 20;
    """
    cur.execute(query, [current_date, current_date])
    return print_table(cur)

def view_personalized_playlist(user_id, current_date):
    """
    瀏覽當日系統推薦的個人化歌單。
    :param user_id: 使用者 ID
    :param current_date: 當前日期（格式：'YYYY-MM-DD'）
    :return: 格式化的個人化歌單資訊
    """
    query = """
        SELECT 
            m.mname, 
            m.artist, 
            m.language, 
            m.duration,
            m.mid
        FROM 
            in_r ir
        JOIN 
            music m ON ir.r_mid = m.mid
        WHERE 
            ir.r_rcreated_for_uid = %s
            AND ir.r_date = %s::DATE;
    """
    cur.execute(query, [user_id, current_date])
    return print_table(cur)

def view_random_songs(song_ids):
    """
    按照隨機生成的歌曲 ID 列表顯示 20 首歌曲。
    :param song_ids: 隨機生成的歌曲 ID 列表（最多 20 個）
    :return: 格式化的歌曲資訊
    """
    query = """
        SELECT 
            m.mname, 
            m.artist, 
            m.language, 
            m.duration
        FROM 
            music m
        WHERE 
            m.mid = ANY(%s);
    """
    cur.execute(query, [song_ids])
    return print_table(cur)

def update_user_name(user_id, new_name):
    """
    更改用戶名稱。
    :param user_id: 用戶 ID
    :param new_name: 新的用戶名稱
    """
    query = """
        UPDATE users
        SET uname = %s
        WHERE uid = %s;
    """
    try:
        cur.execute(query, [new_name, user_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update user name: {str(e)}")

def verify_old_password(user_id, old_password):
    """
    驗證用戶的舊密碼是否正確（無加密版本）。
    :param user_id: 用戶 ID
    :param old_password: 用戶的舊密碼
    :return: 如果密碼正確，返回 True，否則返回 False。
    """
    query = """
        SELECT uid
        FROM users
        WHERE uid = %s AND password = %s;
    """
    cur.execute(query, [user_id, old_password])
    return cur.fetchone() is not None


def update_user_password(user_id, new_password):
    """
    更新用戶密碼（無加密版本）。
    :param user_id: 用戶 ID
    :param new_password: 新密碼
    """
    query = """
        UPDATE users
        SET password = %s
        WHERE uid = %s;
    """
    try:
        cur.execute(query, [new_password, user_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update user password: {str(e)}")


# ============================= function for Admin =============================
def list_all_users():
    """
    瀏覽所有用戶列表，包含名字、Email 和角色。
    :return: 格式化的用戶列表資訊。
    """
    query = """
        SELECT 
            u.uid, 
            u.uname, 
            u.email, 
            r.roles
        FROM 
            users u
        LEFT JOIN 
            roles r ON u.uid = r.roles_uid;
    """
    cur.execute(query)
    return print_table(cur)

def update_user_role(user_id, new_role):
    """
    更新用戶角色。
    :param user_id: 用戶 ID
    :param new_role: 新的角色名稱
    """
    query = """
        UPDATE roles
        SET roles = %s
        WHERE roles_uid = %s;
    """
    try:
        cur.execute(query, [new_role, user_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update user role: {str(e)}")

def update_song_name(song_id, new_name):
    """
    修改一首歌的名稱。
    :param song_id: 歌曲 ID
    :param new_name: 新的歌曲名稱
    """
    query = """
        UPDATE music
        SET mname = %s
        WHERE mid = %s;
    """
    try:
        cur.execute(query, [new_name, song_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update song name: {str(e)}")

def update_song_artist(song_id, new_artist):
    """
    修改一首歌的歌手。
    :param song_id: 歌曲 ID
    :param new_artist: 新的歌手名稱
    """
    query = """
        UPDATE music
        SET artist = %s
        WHERE mid = %s;
    """
    try:
        cur.execute(query, [new_artist, song_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update song artist: {str(e)}")

def update_song_language(song_id, new_language):
    """
    修改一首歌的語言資訊。
    :param song_id: 歌曲 ID
    :param new_language: 新的語言
    """
    query = """
        UPDATE music
        SET language = %s
        WHERE mid = %s;
    """
    try:
        cur.execute(query, [new_language, song_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update song language: {str(e)}")

def update_song_duration(song_id, new_duration):
    """
    修改一首歌的時長。
    :param song_id: 歌曲 ID
    :param new_duration: 新的時長（秒）
    """
    query = """
        UPDATE music
        SET duration = %s
        WHERE mid = %s;
    """
    try:
        cur.execute(query, [new_duration, song_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update song duration: {str(e)}")


def add_song(song_name, artist_name, language, duration):
    """
    新增一首歌到資料庫。
    :param song_name: 歌曲名稱
    :param artist_name: 歌手名稱
    :param language: 語言
    :param duration: 時長（秒）
    """
    query = """
        DO $$
        BEGIN
            -- 檢查 MUSIC 表中的最大 mid 並同步序列值
            PERFORM setval('music_mid_seq', COALESCE((SELECT MAX(mid) FROM music), 0) + 1, false);
        END $$;
        INSERT INTO music (mname, artist, language, duration)
        VALUES (%s, %s, %s, %s)
        RETURNING mid;
    """
    try:
        cur.execute(query, [song_name, artist_name, language, duration])
        song_id = cur.fetchone()[0]
        db.commit()
        return song_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add song: {str(e)}")

def delete_song(song_id):
    """
    刪除指定的歌曲。
    :param song_id: 要刪除的歌曲 ID
    """
    query = """
        DELETE FROM music
        WHERE mid = %s;
    """
    try:
        cur.execute(query, [song_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to delete song: {str(e)}")
    
def query_user_play_history(user_id):
    """
    查询特定用户的播放记录。
    :param user_id: 用户 ID
    :return: 格式化的播放记录表。
    """
    query = """
        SELECT 
            u.uid, 
            u.uname, 
            m.mname, 
            play.play_datetime, 
            play.play_duration
        FROM 
            play
        JOIN 
            users u ON play.play_uid = u.uid
        JOIN 
            music m ON play.play_mid = m.mid
        WHERE 
            u.uid = %s
        ORDER BY 
            play.play_datetime DESC;
    """
    try:
        cur.execute(query, [user_id])
        return print_table(cur)
    except Exception as e:
        raise Exception(f"Failed to query user play history: {str(e)}")

def view_all_albums():
    """
    查看所有专辑及其歌曲总数。
    :return: 格式化的专辑信息表。
    """
    query = """
        SELECT 
            a.aname AS album_name, 
            COUNT(ia.a_mid) AS total_songs
        FROM 
            album a
        LEFT JOIN 
            in_a ia ON a.aid = ia.a_aid
        GROUP BY 
            a.aid
        ORDER BY 
            total_songs DESC;
    """
    try:
        cur.execute(query)
        return print_table(cur)
    except Exception as e:
        raise Exception(f"Failed to view all albums: {str(e)}")

def add_album(album_name):
    """
    添加新专辑。
    :param album_name: 专辑名称
    :return: 新专辑 ID
    """
    query = """
        DO $$
        BEGIN
            -- 同步 album 表的 aid 序列值
            PERFORM setval('album_aid_seq', COALESCE((SELECT MAX(aid) FROM album), 0) + 1, false);
        END $$;

        INSERT INTO album (aname)
        VALUES (%s)
        RETURNING aid;
    """
    try:
        cur.execute(query, [album_name])
        album_id = cur.fetchone()[0]
        db.commit()
        return album_id
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add album: {str(e)}")


def delete_album(album_id):
    """
    删除专辑及其关联的歌曲。
    :param album_id: 专辑 ID
    """
    try:
        # 删除专辑与歌曲的关联
        query_delete_in_a = """
            DELETE FROM in_a
            WHERE a_aid = %s;
        """
        cur.execute(query_delete_in_a, [album_id])

        # 删除专辑
        query_delete_album = """
            DELETE FROM album
            WHERE aid = %s;
        """
        cur.execute(query_delete_album, [album_id])

        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to delete album: {str(e)}")
    
def add_songs_to_album(album_id, song_ids):
    """
    将一首或多首歌曲加入专辑。
    :param album_id: 专辑 ID
    :param song_ids: 歌曲 ID 列表
    """
    query = """
        INSERT INTO in_a (a_mid, a_aid)
        VALUES %s;
    """
    values = [(song_id, album_id) for song_id in song_ids]
    try:
        psycopg2.extras.execute_values(cur, query, values)  # 使用 extras.execute_values 高效插入
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to add songs to album: {str(e)}")


def remove_song_from_album(song_id, album_id):
    """
    从专辑中移除指定歌曲。
    :param song_id: 歌曲 ID
    :param album_id: 专辑 ID
    """
    query = """
        DELETE FROM in_a
        WHERE a_mid = %s AND a_aid = %s;
    """
    try:
        cur.execute(query, [song_id, album_id])
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to remove song from album: {str(e)}")


def create_personalized_playlist(user_id, admin_id, input_date, song_ids):
    """
    为特定用户创建当日个人化推荐歌单。
    :param user_id: 用户 ID
    :param admin_id: 系统管理员或生成歌单的 UID
    :param input_date: 推荐歌单日期
    :param song_ids: 推荐歌曲 ID 列表
    """
    try:
        # 插入或确保推荐歌单存在
        query_playlist = """
            INSERT INTO r_playlist (rcreated_for_uid, rcreated_by_uid, date)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        cur.execute(query_playlist, [user_id, admin_id, input_date])

        # 插入推荐歌曲
        query_songs = """
            INSERT INTO in_r (r_mid, r_rcreated_for_uid, r_date)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """
        # 构建 VALUES 子句的参数
        song_values = [(song_id, user_id, input_date) for song_id in song_ids]

        # 使用 execute_values 插入数据
        psycopg2.extras.execute_values(cur, query_songs, song_values)

        db.commit()
        return f"Personalized playlist for user {user_id} created successfully."
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create personalized playlist: {str(e)}")

