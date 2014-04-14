sudo yum install screen httpd php python python-devel python-pip mysql mysql-server mysql-devel php-soap vsftpd

echo 'prova'

sudo pip install mysql-python soaplib suds-jurko

echo 'set password ftp user(romanelli)'

sudo passwd ftp --stdin

echo 'password mysql root, press only ENTER in fedora'

#sudo mysql -u root -p < initSQLuser.sql
sudo mysql -u root -p < SQL/InitializeDB.sql
sudo mysql -u root -p < SQL/InitializeDB1.sql