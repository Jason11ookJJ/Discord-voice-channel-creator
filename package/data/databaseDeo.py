import sqlite3
from ..function import current_time


def connect():
    conn = sqlite3.connect('data.db')
    db = conn.cursor()
    db.execute('''CREATE TABLE IF NOT EXISTS vc_channel(channel_id int, msg_channel int, respone_msg_id int)''')
    db.execute('''CREATE TABLE IF NOT EXISTS full_statistic(Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, server_in_use int, vc_created int, vc_deleted int)''')
    conn.commit()
    return conn

def savechannel(new_channel_id, msg_channel_id, respone_msg_id):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute("INSERT INTO vc_channel(channel_id, msg_channel, respone_msg_id) VALUES (?, ?, ?)", (new_channel_id, msg_channel_id, respone_msg_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')

def deleteChannel(before_channel_id):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute("DELETE FROM vc_channel WHERE channel_id = (?)", [before_channel_id])
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')

def statsSave(server_count, created, deleted):
    try: 
        conn = connect()
        db = conn.cursor()
        db.execute('''INSERT INTO full_statistic(server_in_use, vc_created, vc_deleted) VALUES(?, ?, ?)''', (server_count, created, deleted))
        conn.commit()
        conn.close()
        print(f'''{current_time()} DB: saved to data.db (server count:{server_count} created: {created}, deleted: {deleted})''')
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')

def get_all_channel(before_channel_id):
    try:
        conn = connect()
        db = conn.cursor()
        result = db.execute("SELECT * FROM vc_channel WHERE channel_id = (?)", [before_channel_id]).fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')

def get_all_stats():
    try:
        conn = connect()
        db = conn.cursor()
        result = db.execute('''SELECT SUM(vc_created), SUM(vc_deleted) FROM full_statistic''').fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')

def delete_all():
    try:
        conn = sqlite3.connect('data.db')
        db = conn.cursor()
        db.execute('''DELETE FROM vc_channel''')
        db.execute('''DELETE FROM full_statistic''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')
    