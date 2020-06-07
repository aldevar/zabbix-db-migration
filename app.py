from flask import Flask, render_template, request
import zabbix_db_migration as zabbix

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/migrate", methods=["POST"])
def migrate():
    r = request.form
    zabbix.srczapi = zabbix.ZabbixAPI(r["srcurl"])
    zabbix.srczapi.login(r["srcuser"], r["srcpass"])

    zabbix.dstzapi = zabbix.ZabbixAPI(r["dsturl"])
    zabbix.dstzapi.login(r["dstuser"], r["dstpass"])

    zabbix.clean_destination()
    zabbix.hostgroups_export()
    zabbix.hostgroups_import()
    zabbix.proxies_export_import()
    zabbix.configuration_export()
    zabbix.configuration_import()
    zabbix.usergroups_export()
    zabbix.usergroups_import()


    return "DONE"

if __name__ == "__main__":
    app.run(debug=True)

