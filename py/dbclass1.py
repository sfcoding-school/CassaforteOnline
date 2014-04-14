import MySQLdb


class DBQuery1:

    def __init__(self, server_addr, suser, spwd, nome_database='server2'):
        self.server_addr = server_addr
        self.suser = suser
        self.spwd = spwd
        self.dbname = nome_database
        self.db = MySQLdb.connect(
            host=server_addr,
            user=suser,
            passwd=spwd,
            db=nome_database)
        print self.server_addr
        print self.suser
        print self.spwd
        print self.dbname

    def insert_slice(self, fid, slice_n, uid):
        cur = self.db.cursor()
        try:
            cur.execute(
                """INSERT INTO slice VALUES(%s,%s,%s)""",
                (fid, slice_n, uid))
            self.db.commit()
            return 1
        except MySQLdb.Error, e:
            print e[0], e[1]
            cur.close()
            print "\n\n Errore \n\n"
            raise e
        return 0

    def remove_slice(self, fid):
        cur = self.db.cursor()
        try:
            cur.execute("""DELETE FROM slice WHERE slice.id=(%s)""", (fid,))
            self.db.commit()
            return 1
        except Exception, e:
            raise e

    def n_parte(self, fid):
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute("""SELECT slice_n FROM slice WHERE slice.id=(%s)""", (fid,))
            ris = cur.fetchone()
            if (ris is None):
                return -1
            else:
                return ris
        except Exception, e:
            raise e

    def give_file_uid(self, fid):
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute("SELECT uid FROM slice WHERE slice.id=(%s)", (fid,))
            ris = cur.fetchone()
            if (ris is None):
                return -1
            else:
                return ris
        except Exception, e:
            raise e
