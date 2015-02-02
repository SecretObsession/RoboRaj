"""
Points class to award points to users
"""
import sqlite3


class Points():
    def __init__(self, config, users):
        self.config = config
        self.users = users
        self.conn = sqlite3.connect("src/res/points.db")
        self.create_sqlite_database()

    def get_points(self, username, channel):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT `points` FROM `points_data` \
                            WHERE `username`=? AND `channel`=? \
                            ORDER BY `timestamp` DESC LIMIT 1",
                           (username, channel,))
            try:
                points = cursor.fetchall()[0]
            except IndexError:
                return 0
            finally:
                cursor.close()

            return int(points[0])

        except sqlite3.OperationalError:
            self.set_points(username=username, channel=channel, points=0)
            return 0

    def set_points(self, username, channel, points):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO `points_data` (`username`, `channel`, `points`) VALUES (?, ?, ?)",
                       (username, channel, points))
        self.conn.commit()
        cursor.close()

    def create_sqlite_database(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS points_data ( \
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                        channel TEXT NOT NULL, \
                        username TEXT NOT NULL, \
                        points INT NOT NULL, \
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);")
        self.conn.commit()
        cursor.close()