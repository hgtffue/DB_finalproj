# 資料庫操作工具
import sys
import psycopg2
from tabulate import tabulate
from threading import Lock

DB_NAME = "QQbeat"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

cur = None
db = None

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
            insert into "USER" (User_name, Password, Email) values (%s, %s, %s)
            RETURNING User_id;
            """
    cur.execute(cmd, [username, pwd, email])
    userid = cur.fetchone()[0]

    cmd =   """
            insert into "USER_ROLE" (User_id, Role) VALUES (%s, 'User');
            """
    cur.execute(cmd, [userid])
    db.commit()