import sqlite3
from package.function import current_time
import os


def connect():
    conn = sqlite3.connect('data.db')
    db = conn.cursor()
    db.execute(
        '''CREATE TABLE IF NOT EXISTS vc_channel(
        channel_id int, 
        msg_channel_id int, 
        response_msg_id int)''')
    db.execute(
        '''CREATE TABLE IF NOT EXISTS text_channel(
        voice_channel_id int, 
        channel_id int, 
        FOREIGN KEY (voice_channel_id) REFERENCES vc_channel(channel_id) ON DELETE CASCADE)''')
    db.execute(
        '''CREATE TABLE IF NOT EXISTS full_statistic(
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
         server_in_use int, 
         vc_created int, 
         vc_deleted int)''')
    db.execute(
        '''CREATE TABLE IF NOT EXISTS error(
        id INTEGER PRIMARY KEY AUTOINCREMENT , 
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        author String, 
        command String, 
        error_messages String,
        fixed int DEFAULT 0,
        dev String)''')
    conn.commit()
    return conn


def save_voice_channel(new_channel_id, msg_channel_id, response_msg_id):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute("INSERT INTO vc_channel(channel_id, msg_channel_id, response_msg_id) VALUES (?, ?, ?)",
                   (new_channel_id, msg_channel_id, response_msg_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')


def save_text_channel(voice_channel_id, text_channel_id):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute("INSERT INTO text_channel(voice_channel_id, channel_id) VALUES (?, ?)",
                   (voice_channel_id, text_channel_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')


def delete_channel(before_channel_id):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute("DELETE FROM vc_channel WHERE channel_id = (?)", [before_channel_id])
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')


def stats_save(server_count, created, deleted):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute('''INSERT INTO full_statistic(server_in_use, vc_created, vc_deleted) VALUES(?, ?, ?)''',
                   (server_count, created, deleted))
        conn.commit()
        conn.close()
        print(
            f'''{current_time()} DB: saved to data.db (server count:{server_count} created: {created}, deleted: {deleted})''')
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')


def get_channel(before_channel_id):
    try:
        conn = connect()
        db = conn.cursor()
        result = db.execute("""SELECT
                                tc.channel_id AS 'tx_channel_id',
                                vc.msg_channel_id,
                                vc.response_msg_id
                            FROM
                                 vc_channel vc
                            LEFT JOIN text_channel tc
                            ON vc.channel_id = tc.voice_channel_id
                            WHERE vc.channel_id = (?)""",
                            [before_channel_id]).fetchall()
        conn.close()
        data = dict(zip([c[0] for c in db.description], result[0]))
        return data
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


def reset_db(self):
    for file in os.listdir():
        if file == "data.db":
            if not os.path.exists('backup'):
                os.makedirs('backup')
            os.replace(file, f"""backup/{current_time()}.db""")
            stats_save(len(self.bot.guilds), 0, 0)
            return


def save_error(ctx, error):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute('''INSERT INTO error(author, command, error_messages) VALUES(?, ?, ?)''', (
            ctx.author.display_name + " #" + ctx.author.discriminator, ctx.message.clean_content, error.args[0]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')


def get_all_error():
    try:
        data = []
        conn = connect()
        db = conn.cursor()
        result = db.execute('''SELECT * FROM error WHERE fixed = 0''').fetchall()
        conn.commit()
        conn.close()
        for i in result:
            data.append(dict(zip([c[0] for c in db.description], i)))
        return data
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')


def check_error(ctx, id):
    try:
        conn = connect()
        db = conn.cursor()
        db.execute('''UPDATE error SET fixed = (1), dev = (?) WHERE id = (?)''', (str(ctx.author), id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'''{current_time()} Error: DB ({e})''')
