#!/usr/bin/env python

import soaplib, base64, random, string, sys, os
from soaplib.core.service import soap
from soaplib.core.service import rpc, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from soaplib.core.model.binary import Attachment

from suds.client import Client

from tempfile import mkstemp
from multiprocessing import Process, Queue


argomenti={'porta':7791,'io':1,'numServer':3}
url = ['http://127.0.0.1:7791/?wsdl','http://127.0.0.1:7792/?wsdl','http://127.0.0.1:7793/?wsdl']

def chiamateSoap(url, parte, nome, output):
    print "parttito il process"
    client = Client(url)
    output.put(client.service.writePart(parte,nome))

class Servizi(DefinitionBase):
    @soap(String,String,_returns=String)
    def dividiFile(self,content,name):
        #fd,fname = mkstemp()
        #os.close(fd)
        #print content
        #
        print "FUNZIONE: dividiFile"
        size = len(content)/3
        part = [content[:size], content[size:size*2], content[size*2:]]
        
        print "ho diviso il file"
        #scrivo il primo pezzo su di me
        fh = open(name+str(0), "wb")
        fh.write(part[0])
        fh.close()
        
        print "ho salvato la mia parte"
        #invio dei file agli altri server
        #con il metodo writePart(content,name)
        
        output = Queue()
        process=[]
        url.pop(argomenti["io"]-1)
        i=1
        for u in url:
            p = Process(target=chiamateSoap, args=((u),(part[i]),(name+str(i)),(output),))
            p.start()
            process.append(p)
            i=i+1
            
        for p in process:
            p.join()
            print output.get()
            
        print "ho contattato i due tizzi"
        #content.fileName = fname
        #content.save_to_file()
        return "server.py"
    
    @soap(String,String,_returns=String)
    def writePart(self,content,name):
        print "FUNZIONE writePart"
        fh = open(name, "wb")
        fh.write(content)
        print "ho scritto la mia parte"
        fh.close()        
        return "fatto, server"+str(argomenti['io'])
    
    #@soap(String,Integer,_returns=Array(String))
    #def say_hello(self,name,times):
    #    results = []
    #    for i in range(0,times):
    #        results.append('dio nn esiste, %s'%name)
    #    return results
    #
    #@soap(String,String,_returns=Integer)
    #def uploadFile(self,content,name):
    #    
    #    
    #    return 1
    #

if __name__=='__main__':
    #arg {porta,server,numeroServer}
    
    try:
        i=2
        key=argomenti.keys()
        print key
        for arg in sys.argv[1:4]:
            argomenti[key[i]] = int(arg)
            i=i-1
    except:
        print "parametri sbagliati uso quelli di default"
    
    print "porta:",argomenti['porta'],"server:",argomenti['io'],"numServer:",argomenti['numServer']
    
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([Servizi], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', argomenti['porta'], wsgi_application)
        print "startato"
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"