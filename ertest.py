# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import os
#import shutil
#import time
#from datetime import datetime
from SamBCoutHTML import SamBCoutHTML as sboh
#from WPEvent import WPEvent
#from WPEvent import WPPollPub
#from WPEvent import TraceEvent
#import WPLogger as log
from jsonutils import WPConfig
from SBPlaylist import SBPlaylistObserver

def main():
    sbplay = SBPlaylistObserver()
    sbo = sboh(sbplay)
    conf = WPConfig()
   
    return (sbplay,sbo,conf)

sbp,sbh,config = main()
