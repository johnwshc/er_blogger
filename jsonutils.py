# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 09:56:44 2018

@author: johnc

This file contains utility methods to manage google api oauth 2
   authentication, json data manipulation, google ids and and
   bloggerAPI resources on EnlightenRadio.org
"""

import json
# from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
# from oauth2client import client
from googleapiclient import sample_tools
# import httplib2
import time
import os

class WPConfig:
    def __init__(self):
         self.ids = WPConfig.json_file_to_dic(WPConfig.CONF_JSON)
        
    
    # constants
    
    CLIENT_SECRETS_FILE = 'client_secrets.json'
    WP_BODY_FILE = 'wp_post_body.json'
    CONF_JSON = 'WPConfig.json'
    
    # oauth credentials storage tool
    CREDENTIALS_FILE = 'credentials-foobar.dat'
    storage = Storage(CREDENTIALS_FILE)
    WP_LOG_HEAD = "::::::: WhatsPlaying Event Log :::::::\nStart: " + str(time.time()) + '\n:::::::::::::::::::::::::::::::::::::::::::::::::::\n'
    
     # get_timestamp()  -- returns string
    def get_timestamp():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
    
    def storeOauthCredentials(credentials):
        WPConfig.storage.put(credentials)
        
       

        
 
   
    
    #default method to authenticate with Google BloggerAPI
    ###FIX: make workable for other services in addition to Blogger
    
    def get_authenticated_service(self):
        # Authenticate and construct service.
        
        service, flags = sample_tools.init(
          [], 'blogger', 'v3', __doc__, __file__,
          scope=self.ids['scope'])
        return (service,flags)
    
    
    
   
    
    
    
    #methods to store an retrieve json and rotate body file
    def saveWPBodyToJson(dic):
        fn = WPConfig.WP_BODY_FILE
        WPConfig.dic_to_json_file(dic,fn)
    
    def dic_to_json_file(dic, fn):
        js = json.dumps(dic,indent=4, sort_keys=True)
        fp = open(fn, 'w')
        # write to json file
        fp.write(js)
    
        # close the connection
        fp.close()
        
    
    def renameWPdata():
        stm = str(time.time())
        newFile = WPConfig.WP_BODY_FILE
        r_fname = str('credentials-foobar' + stm + '.dat')
        os.rename(newFile,r_fname)
        
    
    def readWPBodyFromJson(fn=WP_BODY_FILE):
        return WPConfig.json_file_to_dic(fn)
        
    def json_file_to_dic(fn):
        with open(fn) as js:
            dic = json.load(js)
            js.close()
            return dic
        
    
    def loadClientSecrets(fname=CLIENT_SECRETS_FILE):
        with open(fname) as auth_json:
            d = json.load(auth_json)
            auth_json.close()
            
            return d['installed']
    
    


