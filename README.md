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
userName        hostName        privateIP       provider        AZ              instanceType    
ubuntu          ip-10-11-0-146  10.11.0.146     AWS             us-west-1c      t2.micro        


AUTHOR

    Gregory Touretsky, gregory.touretsky@gmail.com   Aug, 23 2017

