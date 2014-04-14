#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import soaplib
import base64
import random
import string
import sys
import os
import uuid
from soaplib.core.service import soap
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from dbclass1 import DBQuery1 as DB
from collections import OrderedDict

from suds.client import Client

#from tempfile import mkstemp
from multiprocessing import Process, Queue

from ftplib import FTP

#argomenti = {'porta': 7791, 'io': 1, 'numServer': 3}
argomenti = OrderedDict(
    (('porta', 7791), ('io', 1), ('numServer', 3), ('database', 'server1')))

# url = ['http://127.0.0.1:7791/?wsdl',
#       'http://127.0.0.1:7792/?wsdl', 'http://127.0.0.1:7793/?wsdl']
url = []

#servers = ['server1', 'server2', 'server3']
count = 0
part = [None] * 3

client1 = None
client2 = None

# def ftpSave1(data):
#     global count
#     print "f1 secondo callBack", f1
#     if (count < f1):
#         f1salv.write(data)
#         print "count" + str(count)
#         count = count + 1
#     else:
#         ftp.abort()
#         print "abortato"


# def ftpSave2(data):
#     global count
#     print "f2 secondo callBack", f2
#     if (count < f2):
#         f2salv.write(data)
#         print "count" + str(count)
#         count = count + 1
#     else:
#         ftp.abort()
#         print "abortato"


# def ftpSave3(data):
#     global count
#     f3salv.write(data)
#     print "count" + str(count)
#     count = count + 1
#
#----METODO NON TESTATO!!!
#
# def che_parte_ho(id):
#    c = DB1('localhost', 'alexander', '0000')
#    return c.n_parte(id)
#"""
#

# def init_clients(urls):
def crea_clients():
    global client1
    global client2
    if client1 is None and client2 is None:
        urls = url[:]
        urls.pop(argomenti["io"] - 1)
        client1 = Client(urls[0])
        client2 = Client(urls[1])

    return [client1, client2]


def init_server_list():
    a = centrale.service.give_me_server_list()
    for r in a.string:
        url.append(r)
        print r
    print url


def ftpSave(file, fine, ftp):
    def real_ftpSave(data):
        global count
        print "count:", count, "fine", fine
        if (count < fine):
            file.write(data)
            print "count", count
            count = count + 1
        else:
            # ftp.abort()
            print "abortato"
    return real_ftpSave


def fappend(FTP_file_name, fid, offset):
    #ftp = FTP('127.0.0.1')
    #ftp.login('ftp', 'romanelli')
    #a = DB('localhost', 'mysql', 'romanelli', argomenti['database'])
    b = dbconnection.give_file_uid(fid)  # a.give_file_uid(fid)
    uid = "storage/" + b["uid"]
    file1 = open(uid, 'rb')
    ftp.storbinary("STOR " + FTP_file_name, file1,
                   blocksize=8192, callback=None, rest=offset)
    return ftp.size(FTP_file_name)


def chiamateSoap(cl, uuid, inizio, fine, blocksize, output, iid, n_parte):
    print "numero parte: " + str(n_parte)
    print"------------------------------------iid" + str(iid)
    print "parttito il process"
    cl.set_options(cache=None)
    output.put(cl.service.writePart(
        uuid, inizio, fine, blocksize, iid, n_parte))


def threaded_wich_slice(cl, iid, output):
    result1 = cl.service.wich_slice(iid)
    cl.set_options(cache=None)
    arr = []
    print result1
    for r in result1.integer:
        arr.append(r)
    output.put(arr)


class Servizi(DefinitionBase):

    @soap(String, Integer, _returns=String)  # aggiunto id..
    def dividiFile(self, uuidF, iid):
        clients = crea_clients()
        client1 = clients[0]
        print client1
        client2 = clients[1]
        print client2
        global count
        count = 0
        print "FUNZIONE: dividiFile"
        print uuidF
        f = [0, 0]
        #ftp = FTP('127.0.0.1')
        #ftp.login('ftp', 'romanelli')
        size = ftp.size(uuidF)
        print "size: " + str(size)
        print str(count)

        # se il file e' più grande di 3Kb
        if (size > 24576):
            blocksize = 8192
            numBlock = size / blocksize
            part = numBlock / 3
            f[0] = part
            f[1] = part * 2
            print "numBlock", str(numBlock)
            print "f1", str(f[0]), "f2", str(f[1])
        else:
            #size = size * 8
            print "size in bit:", size
            blocksize = size / 3
            print "blocksize", blocksize
            numBlock = 3
            f[0] = 1
            f[1] = 2

        # chiamate soap
        output = Queue()
        urlMod = url[:]
        urlMod.pop(argomenti["io"] - 1)
        print"------------------------------------iid" + str(iid)

        print "faccio partire i process"
        p1 = Process(target=chiamateSoap, args=(
            (client1), (uuidF), (f[0]), (f[1]), (blocksize), (output), (iid), (2),))
        p2 = Process(target=chiamateSoap, args=(
            (client2), (uuidF), (f[1]), (numBlock + 1), (blocksize), (output), (iid), (3),))
        print"2------------------------------------iid" + str(iid)

        p1.start()
        p2.start()
        print"3------------------------------------iid" + str(iid)
        name = str(uuid.uuid4())
        print "name", name

        dbconnection.insert_slice(iid, 1, name)

        name = 'storage/' + name

        # scrivo la mia parte
        fsalv = open(name, 'wb')
        print "apro il file"
        count = 0
        fine = f[0]
        ftp.retrbinary('RETR /' + uuidF, ftpSave(
            fsalv, fine, ftp), blocksize=blocksize, rest=str(0))
        fsalv.close()
        print "ho salvato la mia parte"

        p1.join()
        p2.join()
        print output.get()
        print "ho contattato i due tizzi"
        return "fatto"

    @soap(String, Integer, Integer, Integer, Integer, Integer, _returns=String)
    # aggiungere n_parte e id
    def writePart(self, uuidF, inizio, fine, blocksize, fid, slice_n):
        print "---------------------------------writePart" + str(fid)
        global count
        count = 0
        print "FUNZIONE writePart"
        #ftp = FTP('127.0.0.1')
        #ftp.login('ftp', 'romanelli')

        name = str(uuid.uuid4())

        dbconnection.insert_slice(fid, slice_n, name)

        name = 'storage/' + name

        # inizializzo le variabili
        fsalv = open(name, "wb")
        count = inizio
        ftp.retrbinary('RETR /' + uuidF, ftpSave(fsalv, fine, ftp),
                       blocksize=blocksize, rest=str(count * blocksize))

        print "ho scritto la mia parte"
        fsalv.close()

        return "fatto, server" + str(argomenti['io'])

    @soap(String, Integer, Integer, _returns=Integer)
    def append_slice(self, FTP_file_name, fid, offset):
        print " append slice", offset
        return fappend(FTP_file_name, fid, offset)

    @soap(Integer, _returns=String)
    def give_me_file(self, iid):
        urls = url[:]
        urls.pop(argomenti["io"] - 1)
        output = Queue()
        #client1 = Client(urls[0])
        clients = crea_clients()
        client1 = clients[0]
        client2 = clients[1]
        p1 = Process(target=threaded_wich_slice, args=((client1), (iid), (output),))
        p2 = Process(target=threaded_wich_slice, args=((client2), (iid), (output),))
        p1.start()
        p2.start()
        try:
            myslice_is = dbconnection
            mine = myslice_is.n_parte(iid)
            part[mine['slice_n'] - 1] = url[argomenti["io"] - 1]
        except Exception, e:
            raise e
        p1.join()
        p2.join()
        a = output.get()
        part[a[0]-1] = url[a[1]-1]
        a = output.get()
        part[a[0]-1] = url[a[1]-1]
        print a
        print part

        #result1 = client1.service.wich_slice(iid)
        #part[result1 - 1] = urls[0]
        #client2 = Client(urls[1])
        #result2 = client2.service.wich_slice(iid)
        #part[result2 - 1] = urls[1]

        FTP_file_name = str(uuid.uuid4())
        offset = 0
        for i in range(0, 3):
            print 'i', i
            if (i == argomenti["io"] - 1):
                offset = fappend(FTP_file_name, iid, offset)
            else:
                cl0 = Client(part[i])
                print 'parte', part[i]
                cl0.options.cache.clear()
                offset = cl0.service.append_slice(
                    FTP_file_name, iid, offset)
                print 'parte', part[i]
            i = i + 1
        return FTP_file_name

    @soap(Integer, _returns=Array(Integer))
    def wich_slice(self, iid):
        try:
            myslice_is = dbconnection
            mine = myslice_is.n_parte(iid)
            ris = [mine['slice_n'], argomenti['io']]
            return ris
        except Exception, e:
            raise e

    # def getFile():
    #@soap(String,Integer,_returns=Array(String))
    # def say_hello(self,name,times):
    #    results = []
    #    for i in range(0,times):
    #        results.append('dio nn esiste, %s'%name)
    #    return results
    #
    #@soap(String,String,_returns=Integer)
    # def uploadFile(self,content,name):
    #
    #
    #    return 1
    #

if __name__ == '__main__':
    # arg {porta,server,numeroServer}
    #global client1
    #global client2
    try:
        i = 0
        key = argomenti.keys()
        print key
        for arg in sys.argv[1:4]:
            argomenti[key[i]] = int(arg)
            i = i + 1
        argomenti[key[i]] = sys.argv[4]
    except:
        print "parametri sbagliati uso quelli di default"

    print "porta:", argomenti['porta'], "server:", argomenti['io'], "numServer:", argomenti['numServer'], "Database:", argomenti['database']

    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([Servizi], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', argomenti['porta'], wsgi_application)
        print "startato"
        dbconnection = DB(
            'localhost', 'mysql', 'romanelli', argomenti['database'])
        ftp = FTP('127.0.0.1')
        ftp.login('ftp', 'romanelli')
        centrale = Client('http://127.0.0.1:7790/?wsdl')
        init_server_list()
        #crea_clients()
        server.serve_forever()

    except ImportError:
        print "Error: example server code requires Python >= 2.5"
