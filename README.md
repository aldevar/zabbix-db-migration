# zabbix-db-migration
This project aims to provide a Zabbix migration tool from MySQL to PostresQL mainly using the Zabbix API.

| Zabbix Page                                     | Export methode       | Import Method         |
|-------------------------------------------------|----------------------|-----------------------|
| Administration -> General -> Images             | configuration.export | configuration.import  |
| Administration -> General -> Regular Expression |  DB request?         |  DB request ?         |
| Administration -> General -> Value Mapping      | configuration.export | configuration.import  |
| Administration -> Proxies                       | proxy.get            | proxy.create          |
| Administration -> User Groups                   | usergroup.get        | usergroup.create      |
| Administration -> Users                         | user.get             | user.create           |
| Administration -> Media Type                    | configuration.export | configuration.import  |
| Configuration -> Host Groups                    | configuration.export | configuration.import  |
| Configuration -> Templates                      | configuration.export | configuration.import  |
| Configuration -> Hosts                          | configuration.export | configuration.import  |
| Configuration -> Maintenance                    | maintenance.get      | maintenance.create    |
| Configuration -> Actions                        | action.get           | action.create         |
| Configuration -> Service                        | service.get          | service.create        |
| Monitoring -> Dashboards                        | dashboard.get        | dashboard.create      |
| Monitoring -> Screens                           | configuration.export | configuration.import  |
| Monitoring -> Maps                              | configuration.export | configuration.import  |

## Use

```
pip install -r requirement.txt
python app.py
Go to http://localhost:5000/
```

![flask](/static/img/flask.png "bootstrap flask")



