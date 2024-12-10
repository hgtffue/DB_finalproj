import pandas as pd
import psycopg2

# PostgreSQL 資料庫連線參數
db_config = {
    "host": "127.0.0.1",      
    "database": "QQbeat", 
    "user": "postgres",     
    "password": "your_password", 
    "port": "5432"            
}

# 連接到 PostgreSQL 資料庫
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("連接到 PostgreSQL 成功")
except Exception as e:
    print(f"連接失敗：{e}")
    exit()

# 上傳檔案路徑
rplaylist_file = r"C:\Users\User\Downloads\rplaylist_1211.csv"
in_r_file = r"C:\Users\User\Downloads\in_r_1211.csv"

# 匯入資料到 R_PLAYLIST 表
try:
    df_rplaylist = pd.read_csv(rplaylist_file)
    for i, row in df_rplaylist.iterrows():
        sql = """
        INSERT INTO R_PLAYLIST (rcreated_for_uid, rcreated_by_uid, date)
        VALUES (%s, %s, %s)
        ON CONFLICT (rcreated_for_uid, rcreated_by_uid, date) DO NOTHING;
        """
        cursor.execute(sql, (row['rcreated_for_uid'], row['rcreated_by_uid'], row['date']))
    conn.commit()
    print("資料匯入到 R_PLAYLIST 成功")
except Exception as e:
    conn.rollback() 
    print(f"匯入資料到 R_PLAYLIST 失敗：{e}")

# 匯入資料到 IN_R 表
try:
    df_in_r = pd.read_csv(in_r_file)
    for i, row in df_in_r.iterrows():
        sql = """
        INSERT INTO IN_R (R_mid, R_rcreated_for_uid, R_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (R_mid, R_rcreated_for_uid, R_date) DO NOTHING;
        """
        cursor.execute(sql, (row['R_mid'], row['R_rcreated_for_uid'], row['R_date']))
    conn.commit()
    print("資料匯入到 IN_R 成功")
except Exception as e:
    conn.rollback() 
    print(f"匯入資料到 IN_R 失敗：{e}")

# 關閉連線
cursor.close()
conn.close()
print("匯入完成，連線已關閉")