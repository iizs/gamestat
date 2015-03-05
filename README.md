# gamestat

## Database Initialize
execute mysql as root 
```
mysql> CREATE DATABASE gamestat CHARACTER SET utf8;
mysql> CREATE USER 'gamestat_admin'@'localhost' IDENTIFIED BY 'somepassword';
mysql> GRANT ALL ON gamestat.* TO 'gamestat_admin'@'localhost';
```

add my.cnf
```
# my.cnf
[client]
database = gamestat
user = gamestat_admin
password = PASSWORD
default-character-set = utf8
```
