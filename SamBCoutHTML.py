# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 13:02:30 2018

@author: johnc
"""



import pandas as pd
import bloggerAPItemplates as temps
import GoogleOauthExample as blog_api
from bs4 import BeautifulSoup
from WPEvent import WP_listener
from WPEvent import WPLogPublisher
from WPEvent import BAPIEvent
from WPEvent import TraceEvent
from WPEvent import WPEvent
from jsonutils import WPConfig
import WPLogger as logger

from jinja2 import Template, Environment, PackageLoader, select_autoescape



class SamBCoutHTML(WP_listener,WPLogPublisher):    
    """A class for extracting and reforming Sam Broadcasting General HTML Playlst Outputs, and 
    republishing them to www.enlightenradio.org"""
    def __init__(self,pub):
        super(SamBCoutHTML, self).__init__()
        self.conf = WPConfig()
        self.wp_publisher = pub
        self.wp_publisher.register(self)
        self.gapis = blog_api.google_api_services()
        self.elog = logger.WPLogger()
        self.elog.set_publisher(self)
        # get bloggerAPI authenticated service
        self.service,self.flags = WPConfig.get_authenticated_service(self.conf)
        #wplog.rotate_log()        
        
    
#   Constants for 3 tables on the output html
    CP = 'currently_playing'
    CO = "coming_up"
    PP = "previously_played"
    
    
    # grab data from file or URL and initialize class
    def initialize(self,fname):
        
        self.sb_soup = self.getSoup(fname)
        self.tables = self.getTables(self.sb_soup)
        self.sb_headers = self.getTableHeaders(self.tables)
        self.sb_data = self.process_SB_soup()
        # select_autoescape syntax
        # autoescape=select_autoescape(['html', 'xml'])
        j_env = Environment(
    loader=PackageLoader('whatsplaying', 'templates'),
    autoescape=False)
        self.template = j_env.get_template('wpout.template.html')
        
        self.content = self.template.render(data=self.sb_data)
        
        self.body = temps.get_simp_post_template(self.conf)
        self.body['content']= self.content
        
     # get the headers for each table (th -- tags, except for Previously Played)   
    def getTableHeaders(self,tbls):
        #should be 3 (Beautiful Soup) tables in sam broadcasting heml output, header first row of each table
        headers = {}
        count = 0

        for table in tbls:
            rows = table.find_all('tr')
            header_row = rows[0]
            header = header_row.text
            header = self.process_header(header,count)
            if count == 0:
                headers[self.CP] = header
            elif count == 1:
                headers[self.CO] = header
    
            elif count == 2:
                headers[self.PP] = header
            else: 
                #do nothing
                print('bad count: ', count)

            count += 1

        return headers
    
    def process_header(self,hdr,cnt):
        h = hdr.strip()
        if cnt == 0:
            sh = h.split()
            return [' '.join([sh[0].strip(),sh[1].strip()]),sh[2].strip()]
        elif cnt == 2:
            sh = h.split()
            return [' '.join([sh[0].strip(),sh[1].strip()]),sh[4].strip()]
        else:
            return ['Index', 'Title', 'Artist']

   
    #  methods for extracting each HTML table into python data strucctures
    # Currently Playing Table

    def getTable0Data(self,table):
       
        table0data = []
        table0dic = {}
        table0dic['header'] = self.sb_headers[self.CP]
        
       
        rows = table.find_all('tr')
        data_row = rows[1]
        data_elements = data_row.find_all('td')
        table0data.append(data_elements[1].text.strip())
        table0data.append(data_elements[2].text.strip())
        table0dic['data'] = table0data

    #     print('length of data_elements for table 0, single row: ', len(data_elements))
    #     tdc = 0
    #     for td in data_elements:
    #         print('data for td: ' + str(tdc), td.text)
    #         tdc += 1
        return table0dic
###
##    Coming up Table
    def getTable1Data(self,table):
        table1dic = {}
        table1data= []
        #add header as first row
        table1dic['header']= self.sb_headers[self.CO]
        rows = table.find_all('tr')
        data_row = rows[1]
        tds  = data_row.find_all('td')
        td = tds[0]
        divs = td.find_all('div')
        numdiv = 0
        for div in divs:        
            strings = div.stripped_strings        
            data = []
            for string in strings:           
                data.append(string)           
            table1data.append(data)
            numdiv += 1
        table1dic['data'] =  table1data
        #         table1data['names'] =
        return table1dic

#    Previously Played Table
    def getTable2Data(self,table):
#         PP = "previously_played"
        table2dic = {}
        table2dic['header'] = self.sb_headers[self.PP]
        table2data=[]
    
        rows = table.find_all('tr')
        data_rows = rows[1:]
        row_num = 0

        for row in data_rows:
            row_data = []
            tds = row.find_all('td')
            td_num = 0
            for td in tds:
    #             print('row ' + str(row_num) + ', td '+str(td_num) +': ',td.text)
                if td_num == 1 or td_num == 4:
                    row_data.append(td.text.strip())                
                td_num += 1
            table2data.append(row_data)
            row_num += 1
        table2dic['data'] = table2data
        return table2dic



#  Using Beautiful Soup to parse HTML
    def getSoup(self,fname) :
        txtdata = ''
        with open(fname,'r') as myfile:
            txtdata = myfile.read()
            myfile.close()
        return BeautifulSoup(txtdata,'lxml')

    def getTables(self,soup):
        return soup.find_all('table')  


    def process_SB_soup(self):        
        
        CPdata = self.getTable0Data(self.tables[0])
        COdata = self.getTable1Data(self.tables[1])
        PPdata = self.getTable2Data(self.tables[2])
        return {'headers':self.sb_headers,self.CP:CPdata,self.CO:COdata,self.PP:PPdata}

    def CPdataToHTML(self):
        cp_in = [self.sb_data[self.CP]['data']]
        pd.options.display.max_colwidth = 100
        self.CPdf = pd.DataFrame(data=cp_in,columns=self.sb_headers[self.CP])
        print(self.CPdf)
        return self.CPdf.to_html(border=1)
        
    def PPdataToHTML(self):
        pp_in = self.sb_data[self.PP]['data']
        pd.options.display.max_colwidth = 100
        self.PPdf = pd.DataFrame(data=pp_in,columns=self.sb_headers[self.PP])
        return self.PPdf.to_html(border=1)
    
    def COdataToHTML(self):
        co_in = self.sb_data[self.CO]['data']
        pd.options.display.max_colwidth = 100
        self.COdf = pd.DataFrame(data=co_in,columns=self.sb_headers[self.CO])
        return self.COdf.to_html(border=1)
    
    def getTablesTitle(self):
        return "What's Playing on Enlighten Radio"
    
    def joinTablesHTML(self):
                
        tbl1str = ''.join(['<h2><center>Currently Playing</center></h2><br/>',self.CPdataToHTML(),'<br/><hr/><br/>'])
        tbl2str = ''.join(['<h2><center>Coming Up</center></h2><br/>',self.COdataToHTML(),'<br/><hr/><br/>'])
        tbl3str = ''.join(['<h2><center>Previously Playing</center></h2><br/>',self.PPdataToHTML(),'<br/><br/>'])
        return ''.join([tbl1str,tbl2str,tbl3str])
    
    def getERPlayerCode(self):
        return ("<br />" + "<script src=\"http://player.radiocdn.com/iframe.js?hash=1b9f17aacc6739610d310410c5f0b5091047abfa-450-135\"></script>" +  "<br/>")
    
    def getWPContent(self):
        wp_post_dic = temps.wp_simple_body
        
        con_title = self.getTablesTitle()
        con_body = ''.join([self.getERPlayerCode(),self.joinTablesHTML()])
        wp_post_dic['title'] = con_title
        wp_post_dic['content'] = con_body
        return wp_post_dic
    
    def update (self,wp_event):          
            
            
        if wp_event.msg == WP_listener.NEWFILE:
            self.initialize(wp_event.fname)
            self.dispatch(wp_event)
            re = self.do_new_file(wp_event)
            print('Event: do_new_file(wp_event):  response:')
            print(re)
        elif wp_event.msg == WP_listener.FILE_CHANGE:
            self.initialize(wp_event.fname)
            self.dispatch(wp_event)
            print('Event: do_file_change(wp_event)')
            self.do_file_change(wp_event)
        elif type(wp_event) == TraceEvent:
            self.dispatch(wp_event)
        else:
            print('Event: do_no_change(wp_event)')
            self.dispatch(wp_event)
            print('file polled, but no change')
            
    
    def buildBAPIdic(self,msg,method='None',blogid='None',itemid='None',response = 'None'):
        d = {}
        d['msg'] = msg
        d['timestamp'] = WPConfig.get_timestamp()
        d['service'] = self.conf.ids['service']
        d['method'] = method
        d['content'] = self.body
        d['blogid'] = blogid
        d['itemid'] = itemid
        d['response'] = response
        return d
    
            
        
#        self.ts = adic['timestamp']
#        self.msg = adic.get('msg')
#        self.service = adic.get('service')
#        self.method = adic.get('method')
#        self.content = adic.get('content','no content')
#        self.blogid = adic.get('blogid', 'no blog id')
#        self.itemid = adic.get('itemid', 'no item id')
#        self.response = adic.get('response', 'no response')
#        self.json = json.dumps(adic,indent=4)
    
    def do_new_file(self,wp_event):
        """ This is a post of content extracted from a new or starter(changed format) 
        Sam Broadcasting HTMLOutput file of its playing list, to http://whatsplaying.enlightenradio.org """
        #get WP post content)
        
        # get bloggerAPI authenticated service
        #service,flags = conf.get_authenticated_service()
        #wplog = logger.WPLogger()
        #wplog.rotate_log()
        
        # get a list of posts from the WP blog
        #gapis = blog_api.get_api()
        bdic = self.buildBAPIdic(msg='authenticated blogger api reference.', method='get_api()')
        self.dispatch(BAPIEvent(bdic))
        if self.gapis.IS_DRAFT:
            dft = 'draft'
            isDraft = self.gapis.IS_DRAFT
        else:
            dft = 'live'
            isDraft = False
        resp = self.gapis.list_blog_posts(self.service, self.conf.ids['wp_id'],dft)
        bdic = self.buildBAPIdic(msg='list blog posts',method='list',blogid=self.conf.ids['wp_id'],response=resp)
        self.dispatch(BAPIEvent(bdic))
        
        if resp.get('items') == None:
            #no posts of this type on this blog
            post_res = self.gapis.post_to_wp_blogs(self.service,self.body,draft=isDraft)
            bdic = self.buildBAPIdic(msg='post wp update to Blogger',method='post',blogid=self.conf.ids['wp_id'],response=post_res)
            self.dispatch(BAPIEvent(bdic))
        else:
            # delete existing posts
            for post in resp['items']:
                pid = post['id']
                bid = self.conf.ids['wp_id']
                res = self.gapis.delete_post(self.service,bid,pid)
                bdic = self.buildBAPIdic(msg='delete existing post',method='delete',blogid=bid,itemid=pid,response=res)
                self.dispatch(BAPIEvent(bdic))
            #insert new post
            post_res = self.gapis.post_to_wp_blogs(self.service,self.body,draft=isDraft)
            bdic = self.buildBAPIdic(msg='post wp update to Blogger',method='post',blogid=self.conf.ids['wp_id'],response=post_res)
            self.dispatch(BAPIEvent(bdic))
        print('list of posts for wp blog: \n', post_res)
        return post_res
    
    def do_file_change(self,wp_event):
        """ This is a post of content extracted from a new or starter(changed format) 
        Sam Broadcasting HTMLOutput file of its playing list, to http://whatsplaying.enlightenradio.org """
        #get WP post content
#        # get bloggerAPI authenticated service
#        service,flags = conf.get_authenticated_service()
#        
#        # get a list of posts from the WP blog
#        #gapis = blog_api.get_api()
        bdic = self.buildBAPIdic(msg='authenticated blogger api reference.', method='get_api()')
        self.dispatch(BAPIEvent(bdic))
        if self.gapis.IS_DRAFT:
            dft = 'draft'
            isDraft = self.gapis.IS_DRAFT
        else:
            dft = 'live'
            isDraft = False
        resp = self.gapis.list_blog_posts(self.service, self.conf.ids['wp_id'],dft)
        bdic = self.buildBAPIdic(msg='list blog posts',method='list',blogid=self.conf.ids['wp_id'],response=resp)
        self.dispatch(BAPIEvent(bdic))
        
        if resp.get('items') == None:
            #no posts of this type on this blog
            post_res = self.gapis.post_to_wp_blogs(self.service,self.body,draft=isDraft)
            bdic = self.buildBAPIdic(msg='post wp update to Blogger',method='post',blogid=self.conf.ids['wp_id'],response=post_res)
            self.dispatch(BAPIEvent(bdic))
        else:
            # delete existing posts
            for post in resp['items']:
                pid = post['id']
                bid = self.conf.ids['wp_id']
                res = self.gapis.delete_post(self.service,bid,pid)
                bdic = self.buildBAPIdic(msg='delete existing post',method='delete',blogid=bid,itemid=pid,response=res)
                self.dispatch(BAPIEvent(bdic))
            #insert new post
            post_res = self.gapis.post_to_wp_blogs(self.service,self.body,draft=isDraft)
            bdic = self.buildBAPIdic(msg='post wp update to Blogger',method='post',blogid=self.conf.ids['wp_id'],response=post_res)
            self.dispatch(BAPIEvent(bdic))
        print('list of posts for wp blog: \n', post_res)
        return post_res
        
        
    def do_no_change(self,ev):
        self.dispatch(WPEvent())            
        
        
        
        
        
    
        
        
        
        