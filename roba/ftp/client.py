from ftplib import FTP

count = 0


def ftpSave1(data):
    global count
    # print "f1 secondo callBack", f1
    if (count < f1):
        f1salv.write(data)
        print "count" + str(count)
        count = count + 1
    else:
        ftp.abort()
        print "abortato"


def ftpSave2(data):
    global count
    # print "f2 secondo callBack", f2
    if (count < f2):
        f2salv.write(data)
        print "count" + str(count)
        count = count + 1
    else:
        ftp.abort()
        print "abortato"


def ftpSave3(data):
    global count
    f3salv.write(data)
    print "count" + str(count)
    count = count + 1


def ftpSave(file, fine, ftp):
    def real_ftpSave(data):
        global count
        print "count:", count, "fine", fine
        if (count < fine):
            file.write(data)
            print "count", count
            count = count + 1
        else:
            #ftp.abort()
            print "abortato"
    return real_ftpSave


if __name__ == '__main__':
    name = 'Tekken 3.7z'
    ftp = FTP('127.0.0.1')
    ftp.login('ftp', 'romanelli')
    size = ftp.size(name)
    print "size" + str(size)
    blocksize = 8192
    numBlock = size / blocksize
    part = numBlock / 3
    f1 = part
    f2 = part * 2
    print "numBlock", str(numBlock)
    print "f1", str(f1), "f2", str(f2)

    f1salv = open('a', 'wb')
    f2salv = open('b', 'wb')
    f3salv = open('c', 'wb')

    ftp.retrbinary('RETR /' + name, ftpSave(
        f1salv, f1, ftp), blocksize=blocksize, rest=str(0))

    print "scritto la prima parte"
    ftp.retrbinary('RETR /' + name, ftpSave(f2salv, f2, ftp),
                   blocksize=blocksize, rest=str(f1 * blocksize))

    print "scritto la seconda parte"
    ftp.retrbinary('RETR /' + name, ftpSave(f3salv, numBlock, ftp),
                   blocksize=blocksize, rest=str(f2 * blocksize))

    print "scritto la terza parte"
