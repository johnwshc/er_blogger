# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:47:15 2018

@author: johnc
"""

from jsonutils import WPConfig
from oauth2client.client import AccessTokenRefreshError


class google_api_services:    
    
    IS_DRAFT=False
   
    
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret.
    CLIENT_SECRETS_FILE = 'client_secrets.json'
    
    # This access scope grants read-only access to the authenticated user's blogger
    # account.
#    SCOPES = ['https://www.googleapis.com/auth/blogger']
#    API_SERVICE_NAME = 'blogger'
#    API_VERSION = 'v3'
    def __init__(self,sn='blogger',sv='v3'):
        self.conf = WPConfig()
        self.SCOPES = self.conf.ids['scope']
        self.API_SERVICE_NAME = self.conf.ids['service']
        self.API_VERSION = self.conf.ids['version']
        self.posts = None
        self.request = None
        self.response = None
       
        
    
#    def get_authenticated_service(self):
#        
#        #flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#        # credentials = flow.run_console()
#        credentials = conf.credentials
#        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)
    
    def get_user_blogs(self,service, **kwargs):    
    
        # Retrieve the list of Blogs this user has write privileges on
        thisusersblogs = service.blogs().listByUser(userId='self').execute()
        bloglist = []
        for blog in thisusersblogs['items']:
            blogline = str('The blog named \'%s\' is at: %s' % (blog['name'], blog['url']))
            print(blogline)
            bloglist.append(blogline)
              
        return bloglist
    def post_to_wp_blogs(self,service,bdy,draft=True):
        try:
            self.posts = service.posts()
            b_id = self.conf.ids['wp_id']
            
            #print('blog id: ', b_id)
            b_body = bdy #temps.wp_simple_body #json.dumps(jsonutils.simplest_dict)
#            print('body: ')
#            print(b_body)
            
            is_draft = draft
            self.request = self.posts.insert(blogId=b_id,body=b_body,isDraft=is_draft)
            self.response = self.request.execute()
            print('response ')
            print(self.response)
            return self.response
        #
        
        except AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-runthe application to re-authorize')
    
    def list_blog_posts(self,service, b_Id, stat, fBodies=False, fImages=False, v='ADMIN'):
        
        try:
#            
#            self.wpposts = service.posts()
            self.request = service.posts().list(blogId=b_Id,status=stat,fetchBodies=fBodies,fetchImages=fImages,view=v )
            self.response = self.request.execute()            
            return self.response                
            
        except AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run the application to re-authorize')
            
    def getFirstPostId(self,service,b_Id,stat):
        try:
            
            posts_list = self.list_blog_posts(service,b_Id,stat)['items']
            firstPost = posts_list[0]
            return firstPost['id']
        except AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run the application to re-authorize')
    
    def delete_post(self,service,b_id,p_id):
        try:
            
                posts = service.posts()
                request = posts.delete(blogId=b_id, postId=p_id)
                response = request.execute()
                return response
                
            
        except AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')
        
        
        
def get_api():
    gapis = google_api_services()
    print('got gapis')
    return gapis
    
