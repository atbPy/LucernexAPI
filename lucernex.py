import configparser
import requests
from lxml import etree
from collections import defaultdict

fields = configparser.ConfigParser()
fields.read('fields.conf')

firm = configparser.ConfigParser()
firm.read('firm.conf')


def fiql_get(field, env="TRAIN", fiql=""):
    data = defaultdict(dict)

    headers = {'Authorization': firm["FIRM"]["Token"], 'Content-Type': 'application/xml'}
    params = {'fiql': fiql, 'fields': fields[field]["Fields"]}
    url = "{}/rest/businessObject/{}/details".format(firm["FIRM"][env], field)

    response = requests.get(url, params=params, headers=headers)

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


def lxid_get(field, env="TRAIN", lxid):
    data = defaultdict(dict)

    headers = {'Authorization': firm["FIRM"]["Token"], 'Content-Type': 'application/xml'}
    params = {'deep': 'true', 'wantClientID': 'true', 'wantLxID': 'true'}
    url = "{}/rest/businessObject/{}/lxid/{}".format(firm["FIRM"][env], field, lxid)

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
