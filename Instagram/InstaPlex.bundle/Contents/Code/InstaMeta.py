'''
Created on 17.12.2011

@author: Oliver Knoll
'''

from Constants import *

def getPhotoTitle(data):
    title = ''
    if data['caption'] != None:
        caption = data['caption']['text'].strip()
        if len(caption) > 0 and caption[0] != '#':
            title = caption 
        
    return title

def getPhotoSummary(data):
    summary = ''
    
    user = data[IG_USER][IG_USER_USERNAME]
    summary = summary + 'Author: ' + user
    username =  data[IG_USER][IG_USER_FULL_NAME]
    if username != None:
        summary = summary + ' (' + username + ')'
        
    nofLikes = data[IG_LIKES][IG_LIKES_COUNT]
    summary = summary + '   Likes: ' + str(nofLikes)
    
    filter = data[Constants.IG_FILTER]
    summary = summary + '   Filter: ' + filter + '\n'
    
    for comment in data['comments']['data']:
        theComment = comment['text'].strip()
        if len(theComment) > 0 and theComment[0] != '#':
            summary = summary + theComment
            break
    
    return summary
    
def getTags(data):
    tags = data[IG_TAGS]
    for tag in tags:
        Log.Debug('---------- TAGS: ' + tag)
    return tags
    
def getDate(data):
    timestamp = data[IG_CREATED_TIME]
    datetime = Datetime.FromTimestamp(float(timestamp))
    Log.Debug('getDate: ' + str(datetime))
    return datetime
    