"""
Message class to handle storage of chat messages
"""
import sqlite3


class Messages():
    def __init__(self, save_type=None):
        self.message_history = {}
        self.save_type = save_type
        if save_type == "sqlite":
            self.conn = sqlite3.connect("src/res/messages.db")
            self.create_sqlite_database()

    def store_message(self, channel, username, message, time):
        self.message_history[time] = {"channel": channel, "username": username, "message": message, "time": time}
        if self.save_type == "sqlite":
            self.save_message_sqlite(channel, username, message, time)

    def create_sqlite_database(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS messages ( \
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                        channel TEXT NOT NULL, \
                        username TEXT NOT NULL, \
                        message TEXT NOT NULL, \
                        time TEXT NOT NULL);")
        self.conn.commit()
        cursor.close()

    def save_message_sqlite(self, channel, username, message, time):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO messages (channel, username, message, time) VALUES (?, ?, ?, ?)",
                      (channel, username, message, time))
        self.conn.commit()
        cursor.close()

    def clear_message_history(self):
        self.message_history = {}
