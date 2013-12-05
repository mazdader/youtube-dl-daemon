import MySQLdb
from yt_tools import yt_logger

class yt_DB_my:

    (STATUS_NEW, STATUS_DOWNLOADING, STATUS_DONE, STATUS_FAILED) = (0,1,2,9)

    def __init__(self, mysql_passwd='samplepassword', mysql_user='ytdldaemon', mysql_db_name='ytdldaemon', mysql_host='localhost'):

        self.connection_ok = False
        self.mysql_passwd = mysql_passwd
        self.mysql_user = mysql_user
        self.mysql_db_name = mysql_db_name
        self.mysql_host = mysql_host

        if self.connection_test():
            self.disconnect()

        self.logger = yt_logger.yt_Logger()

    def connection_test(self):
        try:
            self.con = MySQLdb.connect(host=self.mysql_host, user=self.mysql_user, passwd=self.mysql_passwd, db=self.mysql_db_name)
            self.cursor = self.con.cursor()
            self.cursor.execute('SET NAMES "utf8"')
            self.cursor.execute('SELECT id FROM yt_videos LIMIT 1')
            self.cursor.execute('SELECT id FROM yt_log LIMIT 1')
            self.connection_ok = True
            return True
        except MySQLdb.Error as e:
            self.connection_ok = False
            print(repr(e))
            print("""You have to create database and user:
            mysql -uroot -p "CREATE DATABASE ytdldaemon; CREATE USER 'ytdldaemon'@'localhost' identified by 'samplepassword'; GRANT ALL PRIVILEGES on ytdldaemon.* to 'ytdldaemon'@'localhost'; FLUSH PRIVILEGES;"
            mysql -uytdldaemon -psamplepassword -e "CREATE TABLE yt_videos ( \
                id VARCHAR(15) NOT NULL PRIMARY KEY, \
                status INT NOT NULL DEFAULT 0);
                CREATE TABLE yt_log ( \
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                    receivedat TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    log_text VARCHAR(100) );" ytdldaemon
            """)
            return False

    def connect(self):
        try:
            self.con = MySQLdb.connect(host=self.mysql_host, user=self.mysql_user, passwd=self.mysql_passwd, db=self.mysql_db_name)
            self.cursor = self.con.cursor()
            self.cursor.execute('SET NAMES "utf8"')
            self.connection_ok = True
            return True
        except MySQLdb.Error as e:
            self.connection_ok = False
            print(repr(e))
            return False

    def disconnect(self):
        self.con.commit()
        self.cursor.close()
        self.con.close()

    def is_connected(self):
        return self.connection_ok

    def add_videos(self, ids_video):
            self.connect()
            self.cursor.executemany("""INSERT INTO yt_videos (id) VALUES (%s)""", ids_video)
            self.disconnect()
            self.log('Added videos with ids: ' + ' '.join(ids_video))

    def get_all_videos(self, status=-1):
        self.connect()
        if status != -1:
            self.cursor.execute("""SELECT id, status FROM yt_videos where status = %s""", status)
        else:
            self.cursor.execute("""SELECT id, status FROM yt_videos""")
        data = self.cursor.fetchall()
        self.disconnect()
        return tuple(data)

    def change_video_status(self, id_video, status):
        self.connect()
        self.cursor.execute("""UPDATE yt_videos SET status='%s' where id=%s""", (status, id_video))
        self.disconnect()

    def video_exists(self,id_video):
        self.connect()
        self.cursor.execute("""SELECT id FROM yt_videos where id = %s""", id_video)
        data = self.cursor.fetchall()
        self.disconnect()

        if len(data):
            return True
        else:
            return False


