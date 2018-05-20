# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 15:07:11 2018

@author: johnc
"""

import WPEvent as wpe

import time
import os
from jsonutils import WPConfig



class singleton(object):
    instances = {}
    def __new__(cls, clz = None):
        if clz is None:
            # print ("Creating object for", cls)
            if not cls.__name__ in singleton.instances:
                singleton.instances[cls.__name__] = \
                    object.__new__(cls)
            return singleton.instances[cls.__name__]
        # print (cls.__name__, "creating", clz.__name__)
        singleton.instances[clz.__name__] = clz()
        singleton.first = clz
        return type(clz.__name__, (singleton,), dict(clz.__dict__))




#Singleton Logger
    
@singleton
class WPLogger:
    
    
    
    class log_listener(wpe.WP_log_listener):
#        def __init__(self):
#            super.__init__(self)
        
        
        def e_log(self,event):
            with open(self.logname,"a+") as lf:
                
                if type(event) == wpe.WPEvent:
                    lf.write('Poll Event: ')
                    lf.write(event.toString())
                    lf.close()
                elif type(event) == wpe.BAPIEvent:
                    lf.write('Blogger API Event: ')
                    lf.write(event.toString())
                    lf.close()
                elif type(event) == wpe.TraceEvent:
                    lf.write('Trace Debug: ' + event.toString())
                else:
                    lf.write(str(type(event)) + ': ')
                    lf.write(event.toString())
                    lf.close()
        def update(self,event):
            self.e_log(event)
        def set_publisher(self,pub):
            self.pub = pub
            pub.register(self)
            
            
            
    def __init__(self):
        self.conf = WPConfig()      
        self.logname = self.conf.ids.get('logname')
        self.listener = self.log_listener()
        self.listener.logname = self.logname
        
    def set_publisher(self, pub):
        self.listener.set_publisher(pub)
        
    def get_publisher(self):
        return self.listener.pub
    
        
#    def setPublisher(self,pub):
#        sekf,pub = pub
#        pub.register(self)
#        
#    def log(self,event,content=None):
#        with open(self.logname,"a+") as lf:
#            lf.write('Poll Event: ', time.ctime(event['timestamp']), ': ', event['msg'])
#            if not content == None:
#                lf.write('response: \n',content)
#            lf.close()
#    def m_log(self,msg):
#        with open(self.logname, "a+") as lf:
#            lf.write('trace: ', msg)
#        lf.close()
#            
            
    def rotate_log(self):
        tm_s = str(time.time())
        with open(self.logname,"a+") as lf:
            lf.write('\n\nRotating Log file at: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())) + '\n\n' )
            lf.close()
        r_fname = 'WPLogger.' + tm_s + '.log'
        new_log_header = self.conf.ids['wp_log_head']
        os.rename(self.logname,self.conf.ids['event_log_dir'] + r_fname)
        with open(self.logname,"a+") as lf:
            lf.write(new_log_header)
            lf.close()
            
        
    
