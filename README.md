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

## Requires 

* Django==1.7.5
* django-pipeline==1.5.1
* django-twitter-bootstrap==3.3.0
* futures==3.0.3
* mysqlclient==1.3.6
* https://github.com/eternicode/bootstrap-datepicker
