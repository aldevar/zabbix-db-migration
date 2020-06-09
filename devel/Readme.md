## How to use set up dev env

### Create environment
Use docker-compose to create 6 containers.
- 3 containers for zabbix-mysql (zabbix-server-mysql, mysql-database, zabbix-frontend-mysql)
- 3 containers for zabbix-postgresql (zabbix-server-postgresql, postgresql-database, zabbix-frontend-postgresql)  

If you encounter a permission issue with the percona container, pass the following command :   
```
chown -R 999:999 percona
```
Then restart docker-compose.

### Populate Zabbix database
Use the SQL file to populate the mysql database. It provides some basics configurations (hosts, templates, hostgroups, users, usergroups, items, triggers, medias...). 
```
mysql -u zabbix -pzabbix_pwd -h IP.OF.MY.SQL zabbix < populate-zabbix-mysql.sql
```

### Access Zabbix Frontends
Zabbix-MySQL instance is at http://localhost:8080 
Zabbix-PostgreSQL instance is at http://localhost:9080
