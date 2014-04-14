from ftplib import FTP


def connect():
    ftp = FTP('127.0.0.1')
    ftp.login('ftp', 'romanelli')
    file1 = open("localFile1", 'rb')
    ftp.storbinary("STOR file1", file1, blocksize=8192, callback=None, rest=None)
    file2 = open("localFile2", 'rb')
    rest1 = ftp.size('file1')
    ftp.storbinary("STOR file1", file2, blocksize=8192, callback=None, rest=rest1)

    return 0


def write_part(id, offset):
	ftp = FTP('127.0.0.1');
	ftp.login('ftp', 'romanelli')
	uid
    return 0

if __name__ == '__main__':
    connect()
