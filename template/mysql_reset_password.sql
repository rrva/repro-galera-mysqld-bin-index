update mysql.user set password=PASSWORD('%(password)s') where User='root';
delete from mysql.user where User='';
flush privileges;
