import configparser
import requests
from lxml import etree
from collections import defaultdict

fields = configparser.ConfigParser()
fields.read('fields.conf')

firm = configparser.ConfigParser()
firm.read('firm.conf')

def get_field(field, env):
    data = defaultdict(dict)

    headers = {'Authorization': firm["FIRM"]["Token"], 'Content-Type': 'application/xml'}
    params = {'fiql': fields[field]["FIQL"], 'fields': fields[field]["Fields"]}
    url = firm["FIRM"][env] + fields[field]["URLPart"]

    response = requests.get(url, params=params, headers=headers)

    root = etree.fromstring(response.content)
    print(root.tag)

    for child in root:
        print(child.tag)
        for grandchild in child:
            print(grandchild.tag)

get_field("Contract", "TRAIN")