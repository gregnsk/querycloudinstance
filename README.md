NAME

    getCloudInstance.py  -- reports underlying cloud instance details

SYNOPSIS

		getCloudInstance.py

DESCRIPTION

        Current version supports AWS, Azure and GCP 

DEPENDENCIES

		psutil
		requests

EXAMPLES

$ ./getCloudInstance.py
userName:  ec2-user
hostName:  ip-10-20-16-141.ec2.internal
privateIPs:  127.0.0.1@lo; 10.20.16.141@eth0
provider:  AWS
AZ:  us-east-1a
instanceType:  t2.micro
OS:  Linux-3.10.0-862.el7.x86_64-x86_64-with-redhat-7.6-Maipo


AUTHOR

    Gregory Touretsky, gregory.touretsky@gmail.com   Aug, 23 2017

