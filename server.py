# 伺服器主程式
import socket
from threading import Thread

from action.LogIn import LogIn
from action.SignUp import SignUp
from action.Exit import Exit

from DB_utils import *
from utils import *

welcome_action = [LogIn("Log-in"), SignUp("Sign-up"), Exit("Leave System")]

def handle_connection(conn, client_addr):
    try:
        while True:  # Welcome Page
            conn.send("Welcome to QQbeat Music Platform!\n".encode('utf-8'))
            conn.send(f'[INPUT]Please select your option:\n{list_option(welcome_action)}---> '.encode('utf-8'))
                
            action = get_selection(conn, welcome_action)
            
            user = action.exec(conn)
            if user == -1:
                raise Exception("End connection")
            
            conn.send(f'Hi {user.get_username()}! Welcome back!\n'.encode('utf-8'))

            while True:  # Function Page
                conn.send(f'\n[INPUT]Select your action:\n{list_option(user.get_available_action())}---> '.encode('utf-8'))
                action = get_selection(conn, user.get_available_action())
                ret = action.exec(conn, user)
                if ret == -1:
                    break
    except Exception as e:
        print(f"Connection with {client_addr} ended: {e}")
        conn.close()
    finally:
        print(f"Connection with {client_addr} closed.")
        conn.close()


if __name__ == '__main__':

    db = db_connect() 
    # need to modify the sql connection
    cur = db.cursor()

    bind_ip = "127.0.0.1"
    bind_port = 8800

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)

    print(f'Server listening on {bind_ip}:{bind_port} ...')


    try:
        while True:
            (conn, client_addr) = server_socket.accept()
            print("Connect to client:", client_addr)

            thread = Thread(target=handle_connection, args=(conn, client_addr,))
            thread.start()
    finally:
        db.close()
        server_socket.close()