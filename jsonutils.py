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
        
       
#{'recovery_id' : '3260392681602305539',
#        'radio_id' : '1966293608187192453',
#        'radio_url' : 'http://www.enlightenradio.org',
#        'radio_pod_id' : '7279974555523146286',
#        'tales_id' : '238171273635559327',
#        'soc_econ_id' : '5307075296669483402',
#        'resistance_id' : '4625929664919937419',
#        'poetry_id' : '8986792789719838466',
#        'pnm_id' : '894702519709902274',
#        'wp_page_id' : '8970717140175834303',
#        'api_key': 'AIzaSyDW6XtkmrkjoKCEOTS5urpPIciJjV9hdJo',
#        'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
#        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
#        'client_id': '946832198726-eub0q1jk1b46emlsqdrbsj3aupsij1ue.apps.googleusercontent.com',
#        'client_secret': 'kDiIp5JzdDVOeQrhdfGveiZ1',
#        'project_id': 'bloggertools-170622',
#        'redirect_uri': 'https://localhost:8080',
#        'token_uri': 'https://accounts.google.com/o/oauth2/token',
#        'scope' : 'https://www.googleapis.com/auth/blogger',
#        'service':'blogger',
#        'grant_type': 'client_credentials',
#        'version':'v3',
#        'DRAFT' : True,
#        'userId':'112419394476427752442', #jcase
#        'wp_id':'7576689809423182356',
#        'DEBUG': True,
#        'wp_log_head': WP_LOG_HEAD,
#        'logname': r'..\blogger_logs\WPLogger.log',
#        'src_file':r'\\EPIC1\playlists\now.playing.out.html',     
#        'dest_file': "er.playing.out.html",
#        'HTML_body_config':'body_config.json',
#               
#        }
        
 
   
    
    #default method to authenticate with Google BloggerAPI
    ###FIX: make workable for other services in addition to Blogger
    
    def get_authenticated_service(self):
        # Authenticate and construct service.
        
        service, flags = sample_tools.init(
          [], 'blogger', 'v3', __doc__, __file__,
          scope=self.ids['scope'])
        return (service,flags)
    
    #how to authorize and http instance:
    #   http = httplib2.Http()
    #   http = credentials.authorize(http)
        
    #dictionary object conatining client secrets data: don't use
    
    csdict ={"client_id":"946832198726-eub0q1jk1b46emlsqdrbsj3aupsij1ue.apps.googleusercontent.com",
    "project_id":"bloggertools-170622",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":"kDiIp5JzdDVOeQrhdfGveiZ1",
    "rediret_uri":"https://localhost:8080"}
    
    #alternative method of getting google api credentials/token
    
    #def get_credentials():
    #    
    #    credentials = get_flow().run_local_server(host='localhost',
    #        port=8080, 
    #        authorization_prompt_message='Please visit this URL: {url}', 
    #        success_message='The auth flow is complete; you may close this window.',
    #        open_browser=True)
    #    return credentials
    
    #def get_flow():
    #    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    #                               scope='https://www.googleapis.com/auth/blogger',
    #                               redirect_uri=ids['rediret_uri'])
    #    return flow
    
    
    ## Methods to load and manipulate an alt json cred file
    #def loadOauthCreds(fname=CREDENTIALS_FILE):
    #    with open(fname) as oauth_json:
    #        d = json.load(oauth_json)
    #        oauth_json.close()
    #        return d
    
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
    
    


