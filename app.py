from flask import Flask, render_template, request
import zabbix_db_migration as zabbix
import socket

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/migrate", methods=["POST"])
def migrate():
    try:
        r = request.form
        zabbix.srczapi = zabbix.ZabbixAPI(r["srcurl"])
        zabbix.srczapi.login(r["srcuser"], r["srcpass"])

        zabbix.dstzapi = zabbix.ZabbixAPI(r["dsturl"])
        zabbix.dstzapi.login(r["dstuser"], r["dstpass"])

        zabbix.clean_destination()
        zabbix.hostgroups_export()
        zabbix.hostgroups_import()
        zabbix.proxies_export_import()
        zabbix.configuration_import(zabbix.configuration_export())
        zabbix.usergroups_export()
        zabbix.usergroups_import()
        return render_template("done.html")

    except:
        return render_template("error.html")

    

def _getIpAddress():
    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    app.run(debug=True, host=_getIpAddress())

