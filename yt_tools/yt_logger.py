import MySQLdb

class yt_Logger:

    def __init__(self, mysql_passwd='samplepassword', mysql_user='ytdldaemon', mysql_db_name='ytdldaemon', mysql_host='localhost'):

        self.connection_ok = False
        self.mysql_passwd = mysql_passwd
        self.mysql_user = mysql_user
        self.mysql_db_name = mysql_db_name
        self.mysql_host = mysql_host

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

    def log(self, log_text):
        self.connect()
        self.cursor.execute("""INSERT INTO yt_log (log_text) VALUES (%s)""", log_text)
        self.disconnect()
