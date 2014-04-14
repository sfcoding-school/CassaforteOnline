import soaplib
from soaplib.core.service import soap
from soaplib.core.service import rpc, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array

from soaplib.core.model.binary import Attachment
from tempfile import mkstemp
import base64, random, string

from suds.client import Client

class Servizi(DefinitionBase):
    @soap(String,String,String,_returns=String)
    def uploadFile(self,content,name,email):
        print "FUNZINE: uploadFile"
        print "name",name
        length = 10
        chars = string.ascii_lowercase + string.digits
        #random.seed = (os.urandom(1024))
        codice = ''.join(random.choice(chars) for i in range(length))
        
        url1 = 'http://127.0.0.1:7791/?wsdl'
        url2 = 'http://127.0.0.1:7792/?wsdl'
        url3 = 'http://127.0.0.1:7793/?wsdl'
        
        print "contatto server1 atraverso soap"
        
        client1 = Client(url2)
        client1.options.cache.clear()
        
        print "contatto server1 atraverso soap"
        result1 = client1.service.dividiFile(content,name)
        #scegliiere tra ii tre server quale usare per
        #far dividere il file
        #e usare la funzione diividiFile(content,name)
        return result1
    
if __name__=='__main__':
    print "porta:","7790","serverCentrale"
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([Servizi], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('localhost', 7790, wsgi_application)
        print "startato"
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"