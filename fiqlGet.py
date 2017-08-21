import configparser
import requests
from lxml import etree
from collections import defaultdict

fields = configparser.ConfigParser()
fields.read('fields.conf')

firm = configparser.ConfigParser()
firm.read('firm.conf')


def get_field(field, env="TRAIN", fiql=""):
    data = defaultdict(dict)

    headers = {'Authorization': firm["FIRM"]["Token"], 'Content-Type': 'application/xml'}
    params = {'fiql': fiql, 'fields': fields[field]["Fields"]}
    url = firm["FIRM"][env] + fields[field]["URLPart"]

    response = requests.get(url, params=params, headers=headers)

    root = etree.fromstring(response.content)

    for child in root:
        key = child.attrib.get('lxID')
        for grandchild in child:
            # if a tag ends in ID then it is a foreign key and might have an LxID
            # if it has an LxID then we want that instead of the text
            if grandchild.attrib.get('lxID') is not None:
                data[key][grandchild.tag] = grandchild.attrib.get('lxID')
            else:
                data[key][grandchild.tag] = grandchild.text

    return data

contract = get_field("Contract", "TRAIN")
print(contract)