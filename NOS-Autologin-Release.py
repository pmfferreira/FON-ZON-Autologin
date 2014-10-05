#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  Copyright 2014, Paulo Ferreira
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from urllib.parse import urlparse, parse_qs
from time import gmtime, strftime
import time
import requests
import subprocess
import platform

from os import *

sist = platform.system()
print("System Info: " + sist)
print("Time: "+ strftime("%H:%M:%S") + "\n")

global FON_USERNAME
global FON_PASSWORD

FON_USERNAME = getenv('FON_USERNAME')
FON_PASSWORD = getenv('FON_PASSWORD')

def fetchURL():
        try:
                global auth_url
                
                r = requests.get('http://www.google.pt/')
                ip = requests.get('http://myip.dnsdynamic.org/')
                
                auth_url = r.url

                if 'google' in auth_url:
                        print("Connected: "+ ip.text)
                        ret = 1

                elif 'FON':
                        ret = 2
                else:
                        ret = 3
                return ret

        
        except requests.ConnectionError:
                print("Check network connection")
           

def authenticateFON():

        url_data = parse_qs(urlparse(auth_url).query, keep_blank_values = True)
        fields = [ 'nasid', 'uamip', 'uamport', 'mac', 'challenge' ]
        
        str_data = 'res=login'
        for f in fields:
            str_data += '&%s=%s' % (f, url_data[f][0])
        str_data += '&tab=2'
        
        url = "%s://%s%s?%s" % (urlparse(auth_url).scheme,  urlparse(auth_url).netloc, urlparse(auth_url).path, str_data)
        credentials = {'USERNAME': FON_USERNAME, 'PASSWORD': FON_PASSWORD}
        ra = requests.post(url, data=credentials)


        # Check the result
        print("FON: Checking authentication...")
        if 'Login failed. Incorrect username or password. Please try again.' in ra.text:
            print ("FON: Login failed, check username/password!")
        elif "'You're connected!":
            print ("FON: Connected")
        else:
            print ("FON: Something failed")

                  
while True:
       ret = fetchURL()
       if ret == 1:
            time.sleep(10)
       elif ret == 2:
            print("FON: Authenticating " + " @ " + strftime("%Y-%m-%d %H:%M:%S"))
            authenticateFON()
       else:
            print("Try again in 3 seconds")
            time.sleep(3)
