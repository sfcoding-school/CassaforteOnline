from suds.client import Client

if __name__ == '__main__':
    print "FUNZINE: uploadFile"
    url1 = "http://127.0.0.1:7791/?wsdl"
    url2 = 'http://127.0.0.1:7792/?wsdl'
    url3 = 'http://127.0.0.1:7793/?wsdl'

    print "contatto server1 creao Client"
    client1 = Client(url1)
    print "contatto server1 invoco la funzione"
    result = client1.service.give_me_file('199')
    #centrale = Client('http://127.0.0.1:7790/?wsdl')
    #result = centrale.service.give_me_server_list()
    #result = client1.service.dividiFile('file1', '199')
    #result = client1.service.wich_slice('199')

    print result
