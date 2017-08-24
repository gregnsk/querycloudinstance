#!/usr/bin/python
#Detect current provider and instance type
#Support GCP, Azure, AWS

import getpass
import socket
import requests
from requests.exceptions import ConnectionError
import fcntl
import struct
import json
import ntpath
from termcolor import cprint



def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


AWS_URL = "http://169.254.169.254/latest/dynamic/instance-identity/document"
GCP_URL = "http://metadata.google.internal/computeMetadata/v1/instance/"
AZURE_URL = "http://169.254.169.254/metadata/instance?api-version=2017-03-01"

provider = "UNKNOWN"
myzone = "UNKNOWN"
myinstancetype = "UNKNOWN"

try:
    AWS_R = requests.get(AWS_URL)
    if AWS_R.status_code == 200:
        provider = "AWS"
        as_json = json.loads(AWS_R.content)
        myzone = as_json['availabilityZone']
        myinstancetype = as_json['instanceType']
except ConnectionError:
    pass

try:
    GCP_R = requests.get(GCP_URL+'zone', headers={'Metadata-Flavor': 'Google'})
    if GCP_R.status_code == 200:
        provider = "GCP"
        myzone = ntpath.basename(GCP_R.text)
        GCP_R1 = requests.get(GCP_URL+'machine-type', headers={'Metadata-Flavor': 'Google'})
        myinstancetype = ntpath.basename(GCP_R1.text)
except ConnectionError:
    pass

try:
    AZURE_R = requests.get(AZURE_URL, headers={'Metadata': 'true'})
    if AZURE_R.status_code == 200:
        provider = "AZURE"
        as_json = json.loads(AZURE_R.content)
        myzone = as_json['compute']['location']
        myinstancetype = as_json['compute']['vmSize']
except ConnectionError:
    pass

myusername = getpass.getuser()
myhostname = socket.gethostname()
myip = get_ip_address('eth0')

data = [['userName','hostName','privateIP','provider','AZ','instanceType'],[myusername,myhostname,myip,provider,myzone,myinstancetype]]
col_width = max(len(word) for row in data for word in row) + 2
for row in data:
    cprint ("".join(word.ljust(col_width) for word in row), attrs=['bold','reverse'])
