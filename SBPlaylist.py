# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:06:20 2018

@author: johnc
"""

import os
import shutil
import time
from datetime import datetime
from WPEvent import WPEvent
from WPEvent import WPPollPub
from WPEvent import TraceEvent
import WPLogger as log
from jsonutils import WPConfig




# if os.path.exists("test.txt"):
#     print('Yep - found it')

# if os.path.isfile("test.txt"):
#     print('that\'s a file alright')


class SBPlaylistObserver(WPPollPub):
    
    

#     xstr = '\\\\EPIC1\\samHTMLweb\\'
#     source_path = r"\\EPIC1\playlists\now.playing.out.html"
#     dest_path = r"C:\python_apps\bloggerAPI\er.playing.out.html"
#     file_name = "\\er.playing.out.html"
    
#     self.file_to_listen = ''
#     self.dest_copy_file = ''
#     dest_p = ''
#     dest_n = ''
    
    def __init__(self):
        WPPollPub.__init__(self)
        self.conf = WPConfig()
        self.file_to_listen = self.conf.ids['src_file']
        self.dest_copy_file = self.conf.ids['dest_file']
        self.dest_p, self.dest_n = os.path.split(self.dest_copy_file)
        self.logger = log.WPLogger()
        self.DEBUG = self.conf.ids['DEBUG']
        self.logger.rotate_log()
        
        
        
        
#        self.blog_lstnr = WP_listen
    
        

    def sbFileCopy(self):
        isDestFile = os.path.isfile(self.dest_copy_file)
        if isDestFile:            
            stm = str(time.time())
            r_fname = str('t_' + stm + self.dest_n)
            os.rename(self.dest_copy_file, (self.conf.ids['wp_legacy_dir'] + r_fname))
            shutil.copy(self.file_to_listen,self.dest_copy_file)
        else:
            shutil.copy(self.file_to_listen,self.dest_copy_file)
        self.dispatch(TraceEvent('copying playfile to API dir (' + 
                        self.file_to_listen + '  =>  ' + self.dest_copy_file + ')'))
       


        
    def getLastMod(self):
        
        #print('getting mod date on: ', self.file_to_listen)
        moddate = os.stat(self.file_to_listen)[8] 
        # there are 10 attributes this call returns and you want the next to last

        return moddate

    def pollForChange(self):    

        prevModDate = None    
        stop = False

        while not stop:
            nowModDate = self.getLastMod() 
            if prevModDate == None:
                # first start up -- publish the playlist page to blogger
                #####################################################
                #   copy SB file, renaming current dest file, if exists, to name+timestamp,
                #          to bloggerAPI working directory
                self.sbFileCopy()
                
                dict = {'msg':self.NEWFILE,'timestamp':WPConfig.get_timestamp(), 'filename':self.dest_n}
                wp_ev = WPEvent(dict)
                self.dispatch(wp_ev)
                #self.logger.log(wp_ev)                  
                prevModDate = nowModDate
                
            elif prevModDate < nowModDate:
                # playlist has changed -- update/replace playlist blogger site
                self.sbFileCopy()
                dict = {'msg':self.FILE_CHANGE,'timestamp':WPConfig.get_timestamp(), 'filename':self.dest_n}
                wp_ev = WPEvent(dict)
                self.dispatch(wp_ev)
                #self.logger.log(wp_ev)                
                prevModDate = nowModDate
            elif prevModDate == nowModDate:
                dict = {'msg':self.NO_CHANGE,'timestamp':WPConfig.get_timestamp(), 'filename':self.dest_n}
                wp_ev = WPEvent(dict)
                self.dispatch(wp_ev)
                
                # no change in playist file: not update/replace

            else:
                msg = ('ERROR Invalid Mod Date: previous time cannot be greater than now time (' + 
                            prevModDate + ',' + nowModDate + ')')
                self.dispatch(TraceEvent(msg))
                stop=True
            start_time = datetime.now()
            if self.DEBUG:
                self.dispatch(TraceEvent('poll start time: ' + str(start_time)))
            wait = True
            if self.DEBUG:
                self.dispatch(TraceEvent("poll waiting..."))
            while wait:
                time_delta = datetime.now() - start_time
                if time_delta.seconds >=30:
                    wait = False
                    if self.DEBUG:
                        self.dispatch(TraceEvent("Poll Waiting is over: " + str(time_delta.seconds)))
                    
                    

#    print('got sbo:',sbo)
    #sbplay.pollForChange()
    
    
    #dict = {'msg':sbo.NEWFILE,'timestamp':str(time.time()), 'filename':sbplay.dest_n}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    