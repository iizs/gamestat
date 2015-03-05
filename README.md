# gamestat

## Database Initialize
```
mysql> CREATE DATABASE gamestat CHARACTER SET utf8;
mysql> CREATE USER 'gamestat_admin'@'localhost' IDENTIFIED BY 'somepassword';
mysql> GRANT ALL ON gamestat.* TO 'gamestat_admin'@'localhost';
```

