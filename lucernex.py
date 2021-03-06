import configparser
import requests
from lxml import etree
from collections import defaultdict

fields = configparser.ConfigParser()
fields.read('fields.conf')

firm = configparser.ConfigParser()
firm.read('firm.conf')


def fiql_get(table, firm_name="Default", environment="TRAIN", fiql=""):
    data = defaultdict(dict)

    headers = {'Authorization': firm[firm_name]["Token"], 'Content-Type': 'application/xml'}
    params = {'fiql': fiql, 'fields': fields[table]["Fields"]}
    url = "{}/rest/businessObject/{}/details".format(firm[firm_name][environment], table)

    response = requests.get(url, params=params, headers=headers)

    print(response.status_code)

    root = etree.fromstring(response.content)

    for child in root:
        key = child.attrib.get('lxID')
        for grandchild in child:
            # if a tag ends in ID then it is a foreign key and might have an LxID
            # if it has an LxID then we want both items stored in a dict
            if grandchild.attrib.get('lxID') is not None:
                data[key][grandchild.tag] = {'RecID': grandchild.attrib.get('lxID'), 'Name': grandchild.text}
            else:
                data[key][grandchild.tag] = grandchild.text

    return data


def lxid_get(table, lxid, firm_name="Default", environment="TRAIN"):
    data = defaultdict(dict)

    headers = {'Authorization': firm[firm_name]["Token"], 'Content-Type': 'application/xml'}
    params = {'deep': 'true', 'wantClientID': 'true', 'wantLxID': 'true'}
    url = "{}/rest/businessObject/{}/lxid/{}".format(firm[firm_name][environment], table, lxid)

    response = requests.get(url, params=params, headers=headers)

    root = etree.fromstring(response.content)

    for child in root:
        # if a tag ends in ID then it is a foreign key and might have an LxID
        # if it has an LxID then we want both items stored in a dict
        if child.attrib.get('lxID') is not None:
            data[lxid][child.tag] = {'RecID': child.attrib.get('lxID'), 'Name': child.text}
        else:
            data[lxid][child.tag] = child.text

    return data