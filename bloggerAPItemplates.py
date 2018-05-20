# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 17:32:37 2018

@author: johnc
"""

from jsonutils import WPConfig


WPpageUpdateFormat = {
    "status": "DRAFT", 
    "content": "A String", 
    "kind": "blogger#page",  
    "author": {
      "url": "https://www.blogger.com/profile/01595792808567356923", 
      "image": { 
        "url": "//lh3.googleusercontent.com/-Djh2iZUQ4ec/AAAAAAAAAAI/AAAAAAAAAAA/odrltTauZxQ/s35-c/photo.jpg", 
      },
      "displayName": "John Case", 
      "id": "g112419394476427752442", 
    },
    "url": "http://www.enlightenradio.org/p/whats-playing.html", 
    "title": "What's Playing on Enlighten Radio", 
    "updated": "", 
    "blog": { 
      "id": "1966293608187192453", 
    },
    "etag": "A String", 
    "published": "A String", 
    "id": "A String", 
    "selfLink": "https://www.googleapis.com/blogger/v3/blogs/1966293608187192453/pages/8970717140175834303", 
  }

  #revert: boolean, Whether a revert action should be performed when the page is updated (default: false).
  #publish: boolean, Whether a publish action should be performed when the page is updated (default: false).

#def getWPContent():
    
    
    
    
##############################################################################################################
#                                      Pages List JSON format

# list(blogId=*, status=None, pageToken=None, maxResults=None, fetchBodies=None, view=None)
# Retrieves the pages for a blog, optionally including non-LIVE statuses.

# Args:
#   blogId: string, ID of the blog to fetch Pages from. (required)
#   status: string, A parameter (repeated)
#     Allowed values
#       draft - Draft (unpublished) Pages
#       live - Pages that are publicly visible
#   pageToken: string, Continuation token if the request is paged.
#   maxResults: integer, Maximum number of Pages to fetch.
#   fetchBodies: boolean, Whether to retrieve the Page bodies.
#   view: string, Access level with which to view the returned result. Note that some fields require elevated access.
#     Allowed values
#       ADMIN - Admin level detail
#       AUTHOR - Author level detail
#       READER - Reader level detail


  

# ###################################################################       
#list(blogId=*, orderBy=None, startDate=None, endDate=None, labels=None, pageToken=None, 
            #status=None, maxResults=None, fetchBodies=None, fetchImages=None, view=None)
#Retrieves a list of posts, possibly filtered.
#
#Args:
#  blogId: string, ID of the blog to fetch posts from. (required)
#  orderBy: string, Sort search results
#    Allowed values
#      published - Order by the date the post was published
#      updated - Order by the date the post was last updated
#  startDate: string, Earliest post date to fetch, a date-time with RFC 3339 formatting.
#  endDate: string, Latest post date to fetch, a date-time with RFC 3339 formatting.
#  labels: string, Comma-separated list of labels to search for.
#  pageToken: string, Continuation token if the request is paged.
#  status: string, Statuses to include in the results. (repeated)
#    Allowed values
#      draft - Draft (non-published) posts.
#      live - Published posts
#      scheduled - Posts that are scheduled to publish in the future.
#  maxResults: integer, Maximum number of posts to fetch.
#  fetchBodies: boolean, Whether the body content of posts is included (default: true). This should be set to false when the post bodies are not required, to help minimize traffic.
#  fetchImages: boolean, Whether image URL metadata for each post is included.
#  view: string, Access level with which to view the returned result. Note that some fields require escalated access.
#    Allowed values
#      ADMIN - Admin level detail
#      AUTHOR - Author level detail
#      READER - Reader level detail
#
#Returns:
#  An object of the form:

list_posts_response_temp = {
    "nextPageToken": "A String", # Pagination token to fetch the next page, if one exists.
    "items": [ # The list of Posts for this Blog.
      {
        "status": "A String", # Status of the post. Only set for admin-level requests
        "content": "A String", # The content of the Post. May contain HTML markup.
        "kind": "blogger#post", # The kind of this entity. Always blogger#post
        "titleLink": "A String", # The title link URL, similar to atom's related link.
        "author": { # The author of this Post.
          "url": "A String", # The URL of the Post creator's Profile page.
          "image": { # The Post author's avatar.
            "url": "A String", # The Post author's avatar URL.
          },
          "displayName": "A String", # The display name.
          "id": "A String", # The identifier of the Post creator.
        },
        "replies": { # The container of comments on this Post.
          "totalItems": "A String", # The count of comments on this post.
          "items": [ # The List of Comments for this Post.
            {
              "status": "A String", # The status of the comment (only populated for admin users)
              "content": "A String", # The actual content of the comment. May include HTML markup.
              "kind": "blogger#comment", # The kind of this entry. Always blogger#comment
              "inReplyTo": { # Data about the comment this is in reply to.
                "id": "A String", # The identified of the parent of this comment.
              },
              "author": { # The author of this Comment.
                "url": "A String", # The URL of the Comment creator's Profile page.
                "image": { # The comment creator's avatar.
                  "url": "A String", # The comment creator's avatar URL.
                },
                "displayName": "A String", # The display name.
                "id": "A String", # The identifier of the Comment creator.
              },
              "updated": "A String", # RFC 3339 date-time when this comment was last updated.
              "blog": { # Data about the blog containing this comment.
                "id": "A String", # The identifier of the blog containing this comment.
              },
              "published": "A String", # RFC 3339 date-time when this comment was published.
              "post": { # Data about the post containing this comment.
                "id": "A String", # The identifier of the post containing this comment.
              },
              "id": "A String", # The identifier for this resource.
              "selfLink": "A String", # The API REST URL to fetch this resource from.
            },
          ],
          "selfLink": "A String", # The URL of the comments on this post.
        },
        "readerComments": "A String", # Comment control and display setting for readers of this post.
        "labels": [ # The list of labels this Post was tagged with.
          "A String",
        ],
        "customMetaData": "A String", # The JSON meta-data for the Post.
        "updated": "A String", # RFC 3339 date-time when this Post was last updated.
        "blog": { # Data about the blog containing this Post.
          "id": "A String", # The identifier of the Blog that contains this Post.
        },
        "url": "A String", # The URL where this Post is displayed.
        "etag": "A String", # Etag of the resource.
        "location": { # The location for geotagged posts.
          "lat": 3.14, # Location's latitude.
          "lng": 3.14, # Location's longitude.
          "span": "A String", # Location's viewport span. Can be used when rendering a map preview.
          "name": "A String", # Location name.
        },
        "published": "A String", # RFC 3339 date-time when this Post was published.
        "images": [ # Display image for the Post.
          {
            "url": "A String",
          },
        ],
        "title": "A String", # The title of the Post.
        "id": "A String", # The identifier of this Post.
        "selfLink": "A String", # The API REST URL to fetch this resource from.
      },
    ],
    "kind": "blogger#postList", # The kind of this entity. Always blogger#postList
    "etag": "A String", # Etag of the response.
  }
        
        
        
        
        

samplePagesList = {
    
    "nextPageToken": "A String", # Pagination token to fetch the next page, if one exists.
    "items": [ # The list of Pages for a Blog.
        
        
        {
            "status": "A String", # The status of the page for admin resources (either LIVE or DRAFT).
            "content": "A String", # The body content of this Page, in HTML.
            "kind": "blogger#page", # The kind of this entity. Always blogger#page
            "author": { # The author of this Page.
                "url": "A String", # The URL of the Page creator's Profile page.
                "image": { # The page author's avatar.
                    "url": "A String", # The page author's avatar URL.
                },
                "displayName": "A String", # The display name.
                "id": "A String", # The identifier of the Page creator.
            },
            "url": "A String", # The URL that this Page is displayed at.
            "title": "A String", # The title of this entity. This is the name displayed in the Admin user interface.
            "updated": "A String", # RFC 3339 date-time when this Page was last updated.
            "blog": { # Data about the blog containing this Page.
                "id": "A String", # The identifier of the blog containing this page.
            },
            "etag": "A String", # Etag of the resource.
            "published": "A String", # RFC 3339 date-time when this Page was published.
            "id": "A String", # The identifier for this resource.
            "selfLink": "A String", # The API REST URL to fetch this resource from.
        },
        ],
    "kind": "blogger#pageList", # The kind of this entity. Always blogger#pageList
    "etag": "A String", # Etag of the response.
  }

wp_simple_body = {
  "kind": "blogger#post",
  "blog": {
    "id": 'wp_id'
  },
  "title": "what's Playing on Enlighten Radio",
  "content": "With <b>exciting</b> content..."
}  

def get_simp_post_template(conf):
    wp_simple_body['blog']['id'] = conf.ids['wp_id']
    return wp_simple_body


dictPostTemplate  = {
  "status": "DRAFT", # Status of the post. Only set for admin-level requests
  "content": "This is a test Post", # The content of the Post. May contain HTML markup.
  "kind": "blogger#post", # The kind of this entity. Always blogger#post
  "titleLink": "Hello Blogger API Calling...", # The title link URL, similar to atom's related link.
  "author": { # The author of this Post.
    "url": "https://plus.google.com/112419394476427752442", # The URL of the Post creator's Profile page.
    "image": { # The Post author's avatar.
      "url": "https://drive.google.com/open?id=1EPzOqv-nK_1IavjBOfzyXYvc8LHgFUTCPA", # The Post author's avatar URL.
    },
    "displayName": "John Case", # The display name.
    "id": 'client_id' # The identifier of the Post creator.
  },
  "replies": { # The container of comments on this Post.
    "totalItems": "A String", # The count of comments on this post.
    "items": [ # The List of Comments for this Post.
      {
        "status": "A String", # The status of the comment (only populated for admin users)
        "content": "A String", # The actual content of the comment. May include HTML markup.
        "kind": "blogger#comment", # The kind of this entry. Always blogger#comment
        "inReplyTo": { # Data about the comment this is in reply to.
          "id": "A String", # The identified of the parent of this comment.
        },
        "author": { # The author of this Comment.
          "url": "A String", # The URL of the Comment creator's Profile page.
          "image": { # The comment creator's avatar.
            "url": "A String", # The comment creator's avatar URL.
          },
          "displayName": "A String", # The display name.
          "id": "A String", # The identifier of the Comment creator.
        },
        "updated": "A String", # RFC 3339 date-time when this comment was last updated.
        "blog": { # Data about the blog containing this comment.
          "id": "A String", # The identifier of the blog containing this comment.
        },
        "published": "A String", # RFC 3339 date-time when this comment was published.
        "post": { # Data about the post containing this comment.
          "id": "A String", # The identifier of the post containing this comment.
        },
        "id": "A String", # The identifier for this resource.
        "selfLink": "A String", # The API REST URL to fetch this resource from.
      },
    ],
    "selfLink": "A String", # The URL of the comments on this post.
  },
  "readerComments": "A String", # Comment control and display setting for readers of this post.
  "labels": [ # The list of labels this Post was tagged with.
    "A String",
  ],
  "customMetaData": "A String", # The JSON meta-data for the Post.
  "updated": "A String", # RFC 3339 date-time when this Post was last updated.
  "blog": { # Data about the blog containing this Post.
    "id": "A String", # The identifier of the Blog that contains this Post.
  },
  "url": "A String", # The URL where this Post is displayed.
  "etag": "A String", # Etag of the resource.
  "location": { # The location for geotagged posts.
    "lat": 3.14, # Location's latitude.
    "lng": 3.14, # Location's longitude.
    "span": "A String", # Location's viewport span. Can be used when rendering a map preview.
    "name": "A String", # Location name.
  },
  "published": "A String", # RFC 3339 date-time when this Post was published.
  "images": [ # Display image for the Post.
    {
      "url": "A String",
    },
  ],
  "title": "A String", # The title of the Post.
  "id": "A String", # The identifier of this Post.
  "selfLink": "A String", # The API REST URL to fetch this resource from.
}
  
#with open('post_data.json', 'w') as outfile:
#    json.dump(pp.pprint(dictPostTemplate), outfile)
#  
#outfile.close()  