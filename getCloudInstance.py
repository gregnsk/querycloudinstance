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
import psutil
import platform



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
    AWS_R = requests.get(AWS_URL, timeout=0.001)
    if AWS_R.status_code == 200:
        provider = "AWS"
        as_json = json.loads(AWS_R.content)
        myzone = as_json['availabilityZone']
        myinstancetype = as_json['instanceType']
except ConnectionError:
    pass

try:
    GCP_R = requests.get(GCP_URL+'zone', headers={'Metadata-Flavor': 'Google'}, timeout=0.001)
    if GCP_R.status_code == 200:
        provider = "GCP"
        myzone = ntpath.basename(GCP_R.text)
        GCP_R1 = requests.get(GCP_URL+'machine-type', headers={'Metadata-Flavor': 'Google'})
        myinstancetype = ntpath.basename(GCP_R1.text)
except ConnectionError:
    pass

try:
    AZURE_R = requests.get(AZURE_URL, headers={'Metadata': 'true'}, timeout=0.001)
    if AZURE_R.status_code == 200:
        provider = "AZURE"
        as_json = json.loads(AZURE_R.content)
        myzone = as_json['compute']['location']
        myinstancetype = as_json['compute']['vmSize']
except ConnectionError:
    pass

myusername = getpass.getuser()
myhostname = socket.gethostname()

addrs = psutil.net_if_addrs()
myip = ""
for addr in addrs.keys():
    for interface in addrs[addr]:
        if(interface.family == 2):
            if (myip != ""):
                myip = myip + "; "
            myip = myip + interface.address + "@" + addr


print "userName: ",myusername
print "hostName: ",myhostname
print "privateIPs: ",myip
print "provider: ",provider
print "AZ: ",myzone
print "instanceType: ",myinstancetype
print "OS: ",platform.system(),platform.release()