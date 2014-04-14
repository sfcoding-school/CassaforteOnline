import MySQLdb


class DBQuery:

    def __init__(self, server_addr, suser, spwd, nome_database='server'):
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

    def registrazione_user(self, mail, password):
        try:
            if (self.check_if_user_mail_exists(mail)):
                return self.make_user_pro(mail, password)
            else:
                self.create_user(mail, password, 1)
                return True
        except Exception, e:
            raise e

    def create_user(self, mail, password='', pro=0):
        """Se Il parametro pro e' omesso nella chiamata esso prende falso di default"""
        cur = self.db.cursor()
        try:
            cur.execute(
                """INSERT INTO user VALUES(%s,%s,%s,%s)""",
                (mail, 0, pro, password))
            self.db.commit()
        except MySQLdb.Error, e:
            print e[0], e[1]
            cur.close()
            print "\n\n Errore create_user(...) at line 30 file: dbclass.py \n\n"
            raise e

    def check_if_user_mail_exists(self, email):
        cur = self.db.cursor()
        try:
            cur.execute(
                """SELECT mail FROM user WHERE user.mail=(%s)""",
                (email,))
            ris = cur.fetchone()
            if (ris is None):
                return False
            else:
                return True
        except Exception, e:
            print "Errore"
            raise e
            return -1

    def check_space(self, email, space_of_new_file):
        cur = self.db.cursor()
        MaxMemory = 1073741824
        try:
            if(not self.check_if_user_mail_exists(email)):
                print "UserMAil passed as arg not exist"
                if (space_of_new_file <= MaxMemory):
                    return True
                else:
                    return False
            else:
                cur.execute(
                    """SELECT used_space FROM user WHERE user.mail=(%s)""", (email,))
                ris = cur.fetchone()
                spaceleft = ris[0] + space_of_new_file
                if(spaceleft <= MaxMemory):
                    return True
                else:
                    return False
        except Exception, e:
            print "ERRORE at function check_space in file dbclass.py"
            raise e

    def user_login(self, mail, pwd):
        cur = self.db.cursor()
        try:
            cur.execute(
                """SELECT password FROM user WHERE user.mail=(%s)""",
                (mail,))
            ris = cur.fetchone()
            if (ris is None):
                print "UserMAil passed as arg not exists"
                return False
            else:
                if (ris[0] == pwd):
                    return True
                else:
                    print "Wrong Password"
                    return False
        except Exception, e:
            print("ERRORE at function user_login in file dbclass.py")
            raise e

    def make_user_pro(self, email, password):
        cur = self.db.cursor()
        try:
            cur.execute(
                """SELECT pro FROM user WHERE user.mail=(%s)""", (mail,))
            ris = cur.fetchall()
            if (ris == 0):
                cur.execute(
                    """UPDATE user SET pro=1, password=(%s) WHERE user.mail=(%s)""", (password, email))
                self.db.commit()
                return True
            else:
                return False
        except Exception, e:
            raise e

   # def inserisci_file(email, dim, nomefile, codest, array):
       # cur = self.db.cursor()
      #  try:
     #       if(check_if_user_mail_exists(email)):
    #            if(check_space(email, dim)):
   #                 cur.execute('INSERT INTO FILE VALUES(%%%%)',())

    # Ritorna None se l'utente non ha file!!!
    # Altrimenti ritorna un dizionario con le chiavi del db
    def getfilelist(self, mail):
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute(
                """SELECT codest, nome, dim FROM file WHERE file.owner=(%s)""",
                (mail,))
            ris = cur.fetchall()
            if ris:
                return ris
            # for row in ris:
                # print row['codest']
                # print row['nome']
                # print row['dim']
            else:
                print 'None'
                return None

        except Exception, e:
            raise e

    def get_file(self, mail, codest):
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute(
                """SELECT id, nome FROM file WHERE file.owner=(%s) AND file.codest=(%s)""", (mail, codest))
            ris = cur.fetchone()
            if ris:
                return ris
            else:
                print "None"
                return None
        except Exception, e:
            raise e

    def set_file_available(self, email, codest):
        cur = self.db.cursor()
        try:
            cur.execute(
                """UPDATE file SET lavorazione=1 WHERE file.owner=(%s) AND file.codest=(%s) """, (email, codest))
            self.db.commit()
            return 1
        except Exception, e:
            raise e

    def insert_file(self, email, codest, dim, nome):
        if not self.check_if_user_mail_exists(email):
            self.create_user(email)
        if self.check_space(email, dim):
            cur = self.db.cursor()
            try:
                cur.execute(
                    """INSERT file (codest,dim,nome,owner ) VALUES (%s,%s,%s,%s)""", (codest, dim, nome, email))
                self.db.commit()
                return cur.lastrowid
            except Exception, e:
                raise e
        else:
            return -1

    def delete_file(self, mail, codest):
        cur = self.db.cursor()
        try:
            cur.execute(
                """DELETE FROM file WHERE file.owner=(%s) AND file.codest=(%s) """, (mail, codest))
            self.db.commit()
            return 1
        except Exception, e:
            raise e

    def get_server_list(self):
        cur = self.db.cursor()
        try:
            cur.execute(
                """SELECT address FROM server ORDER BY id asc""")
            ris = cur.fetchall()
            array = []
            for row in ris:
                array.append(row[0])
            return array
        except Exception, e:
            raise e
