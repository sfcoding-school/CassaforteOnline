import soaplib
from soaplib.core.service import soap
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import String, Integer, Boolean
from soaplib.core.model.clazz import Array
from soaplib.core.model.clazz import ClassModel
from soaplib.core.server import wsgi

from suds.client import Client
#from tempfile import mkstemp
from dbclass import DBQuery

import random

ready = 0

def scegliServer():
    url = ['http://127.0.0.1:7791/?wsdl',
           'http://127.0.0.1:7792/?wsdl', 'http://127.0.0.1:7793/?wsdl']
    return url[random.randint(0, 2)]


class File(ClassModel):
    # print row['codest']
    # print row['nome']
    # print row['dim']
    __namespace__ = "File"
    codest = String
    nome = String
    dim = Integer


class FileDownload(ClassModel):
    __namespace__ = "FileDownload"
    tmpName = String
    name = String


class Servizi(DefinitionBase):

    @soap(_returns=Array(String))
    def give_me_server_list(self):
        a = db.get_server_list()
        return a

    @soap(String, String, _returns=FileDownload)
    def downloadFile(self, code, email):
        print 'download file', code, email
        try:
            dbFile = db.get_file(email, code)
            File = FileDownload()
            print 'idfile', dbFile['id'], dbFile['nome']
            if (dbFile is not None):
                client = Client(scegliServer())
                tmpName = client.service.give_me_file(dbFile['id'])
                File.tmpName = tmpName
                File.name = dbFile['nome']
                print 'File.tmpName', File.tmpName
                print 'File.name', File.name
            else:
                File.tmpName = '-1'
                File.name = '-1'
            return File
        except Exception:
            File.tmpName = '-1'
            File.name = '-1'
            return File

    @soap(String, _returns=Array(File))
    def listFile(self, email):
        print 'get list file', email
        try:
            risDB = db.getfilelist(email)
            return risDB
            #ris = File()
            # for f in risDB:
            #    ris.codest = f['codest']
            #    ris.nome = f['nome']
            #    ris.dim = f['dim']

        except Exception, e:
            print 'errore:', e

    @soap(String, String, _returns=Boolean)
    def login(self, email, passwd):
        print 'login', email
        try:
            return db.user_login(email, passwd)
        except Exception, e:
            print 'errore:', e
            return False

    @soap(String, String, _returns=Boolean)
    def registraUtente(self, email, passwd):
        print 'registro utente', email, passwd
        try:
            return db.registrazione_user(email, passwd)
        except Exception, e:
            print 'errore:', e
            return False

    @soap(String, Integer, _returns=Boolean)
    def checkFileSpace(self, email, dim):
        if (db.check_space(email=email, space_of_new_file=dim) is True):
            return True
        else:
            return False

    @soap(String, String, String, Integer, String, _returns=String)
    def uploadFile(self, uuid, name, codest, dim, email):
        print "FUNZINE: uploadFile"
        print "name", name

        url1 = 'http://127.0.0.1:7791/?wsdl'
        url2 = 'http://127.0.0.1:7792/?wsdl'
        url3 = 'http://127.0.0.1:7793/?wsdl'
        try:
            idFile = db.insert_file(
                email=email, codest=codest, dim=dim, nome=name)
            if (idFile > -1):
                print "contatto server1 creao Client"
                client1 = Client(url1)
                print "contatto server1 invoco la funzione"
                result = client1.service.dividiFile(uuid, idFile)
            else:
                result = 'databaseFail'
        except Exception:
            result = Exception

        return "risp: " + result

if __name__ == '__main__':
    print "porta:", "7790", "serverCentrale"
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([Servizi], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', 7790, wsgi_application)
        db = DBQuery(server_addr='localhost', suser='mysql', spwd='romanelli')
        print "startato"
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"
