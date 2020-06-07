from pyzabbix import ZabbixAPI, ZabbixAPIException
import json

srczaburl = "http://localhost"
srczabuser = 'Admin'
srczabpass = 'zabbix'

dstzaburl = "http://localhost:9080"
dstzabuser = 'Admin'
dstzabpass = 'zabbix'


srczapi = ZabbixAPI(srczaburl)
srczapi.login(srczabuser, srczabpass)
dstzapi = ZabbixAPI(dstzaburl)
dstzapi.login(dstzabuser, dstzabpass)



def usergroups_import():
    with open('usergroups.json', 'r') as f:
        usergroups = json.loads(f.read())
    for usergroup in usergroups:
        usergroup.pop('usrgrpid')
        try:
            res = dstzapi.usergroup.create(usergroup)
        except ZabbixAPIException as e:
            print(str(e))
        else:
            print('Group {0} created with group id {1}'.format(usergroup['name'], res['usrgrpids'][0]))


def usergroups_export():
    usergroups = srczapi.usergroup.get()
    with open('usergroups.json', 'w') as f:
        json.dump(usergroups, f, indent=4)


def hostgroups_export():
    with open('hostgroups.json', 'w') as f:
        hostgroups = srczapi.hostgroup.get()
        json.dump(hostgroups, f, indent=4)


def hostgroups_import():
    with open('hostgroups.json', 'r') as f:
        hostgroups = json.loads(f.read())
    for hostgroup in hostgroups:
        if hostgroup['flags'] == '0':
            groupname = hostgroup['name']
            try:
              res = dstzapi.hostgroup.create(name=groupname)
            except ZabbixAPIException as e:
                print(str(e))
            else:
                print('Host Group {0} created with group id {1}'.format(hostgroup['name'], res['groupids'][0]))


def proxies_export_import():
    proxies = srczapi.proxy.get(output='extend', selectInterface='extend')
    for proxy in proxies:
        if proxy['status'] == '6':
            del proxy['interface']['interfaceid']
            del proxy['interface']['hostid']
        try:
            res = dstzapi.proxy.create(host=proxy['host'],
                                    status=proxy['status'],
                                    tls_connect=proxy['tls_connect'],
                                    description=proxy['description'],
                                    tls_accept= proxy['tls_accept'],
                                    tls_issuer= proxy['tls_issuer'],
                                    tls_subject=proxy['tls_subject'],
                                    tls_psk_identity=proxy['tls_psk_identity'],
                                    tls_psk=proxy['tls_psk'],
                                    proxy_address=proxy['proxy_address'],
                                    interface=proxy['interface'])
        except ZabbixAPIException as e:
            print(str(e))
        else:                
            print('Proxy {0} created with id {1}'.format(proxy['host'], res['proxyids'][0]))


def clean_destination():
    '''
    Drop all hosts and templates
    on target zabbix installation
    '''
    templates = dstzapi.template.get(output='templateid')
    print(templates)
    templatesids = [templ['templateid'] for templ in templates]
    print(templatesids)
    hosts = dstzapi.host.get(output='hostid')
    print(hosts)
    hostsids = [h['hostid'] for h in hosts]
    print(hostsids)
    for templateid in templatesids:
        res1 = dstzapi.template.delete(templateid)
        print(res1)
    for hostid in hostsids:
        res2 = dstzapi.host.delete(hostid)
        print(res2)
    

def configuration_export():
    hostgroups = srczapi.hostgroup.get(output='groupid')
    groupsids = [hg['groupid'] for hg in hostgroups]
    templates = srczapi.template.get(output='templateid')
    templatesids = [templ['templateid'] for templ in templates]
    mediatypes = srczapi.mediatype.get(output='mediatypeid')
    mediatypesids = [media['mediatypeid'] for media in mediatypes]
    hosts = srczapi.host.get(output='hostid')
    hostsids = [h['hostid'] for h in hosts]
    images = srczapi.image.get(output='imageid')
    imagesids = [i['imageid'] for i in images]
    maps = srczapi.map.get(output='selementid')
    mapsids = [m['sysmapid'] for m in maps]
    screens = srczapi.screen.get(output='screenid')
    screensids = [screen['screenid'] for screen in screens]
    valuemaps = srczapi.valuemap.get()
    valuemapsids = [val['valuemapid'] for val in valuemaps]

    ## TODO : Add a condition on API versions (option mediatypes not available before 4.4)    
    config = srczapi.configuration.export(format='json',
                                          options={'groups': groupsids,
                                                   'hosts': hostsids,
                                                   'images': imagesids,
                                                   'maps': mapsids,
                                                   'mediaTypes': mediatypesids,
                                                   'screens': screensids,
                                                   'templates': templatesids,
                                                   'valueMaps': valuemapsids
                                                   }
                                         )
 

    with open('config-export.json', 'w') as f:
        json.dump(config, f, indent=4)



def configuration_import():
    ## TODO : Proxies must be imported first
    res = dstzapi.confimport(confformat='json', source=config,
                             rules={'hosts':{'createMissing': True, 'updateExisting': True},
                                    'templates':{'createMissing': True, 'updateExisting': True},
                                    'groups':{'createMissing': True},
                                    'images':{'createMissing': True, 'updateExisting': True},
                                    'maps':{'createMissing': True, 'updateExisting': True},
                                    'mediaTypes':{'createMissing': True, 'updateExisting': True},
                                    'screens':{'createMissing': True, 'updateExisting': True},
                                    'valueMaps':{'createMissing': True, 'updateExisting': True},
                                    'applications': {'createMissing': True},
                                    'discoveryRules':{'createMissing': True, 'updateExisting': True},
                                    'graphs': {'createMissing': True, 'updateExisting': True},
                                    'httptests': {'createMissing': True, 'updateExisting': True},
                                    'items': {'createMissing': True, 'updateExisting': True},
                                    'templateLinkage': {'createMissing': True},
                                    'templateScreens': {'createMissing': True, 'updateExisting': True},
                                    'triggers': {'createMissing': True, 'updateExisting': True}})
    print(res)


def users_export():
    pass


def users_import():
    pass


def maintenances_export():
    pass


def maintenances_import():
    pass


if __name__ == '__main__':
    clean_destination()
    hostgroups_export()
    hostgroups_import()
    proxies_export_import()
    configuration_export()
    configuration_import()
    usergroups_export()
    usergroups_import()


