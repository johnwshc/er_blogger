# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:23:21 2018

@author: johnc
"""
import json

from abc import ABC,abstractmethod

class EREvent(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def toString():
        pass
    
    


class WPEvent(EREvent):
    def __init__(self,edic):
        super().__init__()
        self.msg = edic['msg']
        self.ts = edic['timestamp']
        self.fname = edic['filename']
        self.json = json.dumps(edic, indent=4)
        self.content = edic.get('content','no_content')
    def toString(self):
        return self.json
        
        
        
class BAPIEvent(EREvent):
    def __init__(self, adic):
        super().__init__()
        self.timestamp = adic['timestamp']
        self.msg = adic.get('msg')
        self.service = adic.get('service')
        self.method = adic.get('method','None')
        self.content = adic.get('content','no content')
        self.blogid = adic.get('blogid', 'no blog id')
        self.itemid = adic.get('itemid', 'no item id')
        self.response = adic.get('response', 'no response')
        self.json = json.dumps(adic,indent=4)
    def toString(self):
        return self.json
    
class TraceEvent(EREvent):
    def __init__(self,msg):
        super().__init__()
        self.msg = msg
        
    def toString(self):
        return self.msg

class Subscriber(ABC):
    def __init__(self):
       super().__init__()
        
    @abstractmethod
    def update(self, message):
        pass
#        print('{} got message "{}"'.format(self.name, message))
    
    
        
class WP_listener(Subscriber):
    NEWFILE = "new_html_file"
    NO_CHANGE = "no_html_update"
    FILE_CHANGE = "html_updated"
    def __init__(self):
        super().__init__()
        self.name = "wp_listener"
    def update(self,wpevent):
        self.msg = wpevent['msg']
        self.timestamp = wpevent['timestamp']
        self.fname = wpevent['filename']
        
        
class WP_log_listener(Subscriber):
    def __init__(self):
         super().__init__()
         
    @abstractmethod    
    def update(self,bapi_event):
        pass
        
           
        
class Publisher:
    
    def __init__(self):
        self.subscribers = set()
    def register(self, who):
        self.subscribers.add(who)
    def unregister(self, who):
        self.subscribers.discard(who)
    def dispatch(self, event):
        for subscriber in self.subscribers:
            subscriber.update(event)
            
class WPPollPub(Publisher):
    NEWFILE = "new_html_file"
    NO_CHANGE = "no_html_update"
    FILE_CHANGE = "html_updated"
    
class WPLogPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self.name = 'wp_log_publisher'
    
    