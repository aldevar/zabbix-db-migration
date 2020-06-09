## How to use the dev tools ?

Use docker-compose to create 6 containers.
3 containers for zabbix-mysql (zabbix-server, mysql-database, zabbix-frontend)
3 containers for zabbix-postgresql (zabbix-server, postgresql-database, zabbix-frontend)

If you encounter a permission issue with the percona container, pass the following command : 
  chown -R 999:999 percona
Then restart docker-compose.

You can then use the SQL file to populate the mysql-database. It provides some basics configurations (hosts, templates, hostgroups, users, usergroups...). 
  mysql -u zabbix -p -h IP.OF.MYSQL zabbix < 

