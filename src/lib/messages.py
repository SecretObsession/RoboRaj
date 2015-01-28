"""
Message class to handle storage of chat messages
"""
import sqlite3
import time


class Messages():
    def __init__(self, save_type=None):
        self.message_history = {}
        self.save_type = save_type
        if save_type == "sqlite":
            self.conn = sqlite3.connect("src/res/messages.db")
            self.create_sqlite_database()
        elif save_type == "html":
            self.html = ""
            self.html_page = "log/messages.html"
            self.build_html_header()

    def store_message(self, channel, username, message, timestamp):
        self.message_history[time] = {"channel": channel, "username": username, "message": message, "time": timestamp}
        if self.save_type == "sqlite":
            self.save_message_sqlite(channel, username, message.encode('utf-8'), timestamp)
        if self.save_type == "html":
            self.save_message_html(channel, username, message.encode('utf-8'), timestamp)

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

    def build_html_header(self):
        html = "<html><head><title>Chat Messages</title></head><body><table>"
        html += "<tr><th>Channel</th><th>Time</th><th>User</th><th>Message</th></tr>"
        self.html = html

    def save_message_html(self, channel, username, message, timestamp):
        html = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" \
               % (channel, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(timestamp)), username, message)
        self.html += html
        temp_html = self.html
        temp_html += "</table></body></html>"
        file_log = open(self.html_page, "w+")
        file_log.write(temp_html)
        file_log.close()

    def save_message_sqlite(self, channel, username, message, timestamp):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO messages (channel, username, message, time) VALUES (?, ?, ?, ?)",
                      (channel, username, message, timestamp))
        self.conn.commit()
        cursor.close()

    def clear_message_history(self):
        self.message_history = {}
