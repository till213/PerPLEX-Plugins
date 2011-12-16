'''
Created on 04.12.2011

@author: Oliver Knoll
'''

import urlparse

import WebKeys
import Resources
    
def getPopularStream():
    '''Retrieves the Popular photo stream'''
    
    token = Data.Load('oauthtoken')
    Data.Remove('navig')
    return readStream(url = WebKeys.POPULAR_URL, title = 'Popular')
 
def getOwnPhotosStream():
    '''Retrieves the user photos; user needs to be logged in, that is a valid OAuth 2 token is necessary.'''
    
    token = Data.Load('oauthtoken')
    Data.Remove('navig')
    return readStream(url = WebKeys.MY_PHOTOS_URL + token, title = 'My Photos')

def getTagStream(tag, name = None):
    '''Retrieves the Instagram photo stream, given by its tag and returns a ObjectContainer containing the photo URLs
    named name'''
    
    title = None
    if (name != None):
        title = name
    else:
        title = tag
    Data.Remove('navig')
    return readStream(url = WebKeys.TAG_STREAM_URL % tag, title = title)

def getUserStream(id, name):
    '''Retrieves the Instagram user's stream, given by ID and returns a ObjectContainer containing the photo URLs
    named name'''
    
    token = Data.Load('oauthtoken')
    Data.Remove('navig')
    Log.Debug('+++++++++++Users stream: requesting: ' +  WebKeys.USER_URL % id + token)
    return readStream(url = WebKeys.USER_URL % id + token, title = name)

def readStream(url, title, forward = True):
    oc = ObjectContainer(title2 = title, view_group = 'Pictures', no_history=True)
    photoObject = None
    stream = JSON.ObjectFromURL(url)
    #Log.Debug('\n'.join([l.rstrip() for l in  str(stream).splitlines()]))
    for data in stream['data']:
        photoObject = getPhotoObject(data)        
        if (photoObject != None):
            oc.add(photoObject)
     
    addNavigation(url = url, title = title, stream = stream, forward = forward, objectContainer = oc)    
    return oc

def getPhotoObject(data):
    url = data['images']['standard_resolution']['url']
    thumbUrl = data['images']['thumbnail']['url']
    comment = None
    caption = None
    if len(data['comments']['data']) > 0:
        comment = data['comments']['data'][0]['text']
    if data['caption'] != None:
        caption = data['caption']['text']
    photoObject = PhotoObject(title=caption, summary=comment, key=url, rating_key=url, thumb=Callback(getThumb, url=thumbUrl))
    return photoObject

def addNavigation(url, title, stream, forward, objectContainer):
    previousUrl = None
    nav = []
    
    if forward:
        if Data.Exists('navig'):  
            nav = Data.LoadObject('navig')
            if len(nav) > 0:                
                previousUrl = nav[-1]
        nav.append(url)
    else:
        if Data.Exists('navig'):    
            nav = Data.LoadObject('navig')
            nav.pop()
            if len(nav) > 1:
                # the last element points to the page we're currently on; so take the second-last element     
                previousUrl = nav[-2]
    
    if previousUrl != None:
        objectContainer.add(DirectoryObject(key = Callback(morePhotos, url=previousUrl, title=title, forward=False), title = 'Previous...', thumb = R(Resources.PREVIOUS_ICON)))  
    Data.SaveObject('navig', nav)

    if 'pagination' in stream:        
        pagination = stream['pagination']
        if pagination != None:
            nextUrl = pagination['next_url']
            objectContainer.add(DirectoryObject(key = Callback(morePhotos, url=nextUrl, title=title, forward=True), title = 'Next...', thumb = R(Resources.NEXT_ICON)))  

def getThumb(url):
    return None
  
def morePhotos(url, title, forward):
    return None
    
   
