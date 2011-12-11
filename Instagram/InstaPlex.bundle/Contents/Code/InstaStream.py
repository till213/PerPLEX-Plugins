'''
Created on 04.12.2011

@author: Oliver Knoll
'''

import WebKeys
import Resources
    
def getPopularStream():
    '''Retrieves the Popular photo stream'''
    token = Data.Load('oauthtoken')
    
    Log.Debug('Called InstaStream functions...')
    title = "Popular"
    return readStream(title, WebKeys.POPULAR_URL)
 
def getOwnPhotosStream():
    '''Retrieves the user photos; user needs to be logged in, that is a valid OAuth 2 token is necessary.'''
    token = Data.Load('oauthtoken')
    
    title = "My Photos"
    return readStream(title, WebKeys.MY_PHOTOS_URL + token)

def getTagStream(tag, name = None):
    '''Retrieves the Instagram photo stream, given by its tag and returns a MediaContainer containing the photo URLs
    named name'''
    title = None
    if (name != None):
        title = name
    else:
        title = tag
    return readStream(title, WebKeys.TAG_STREAM_URL % tag)

def readStream(title, url):
    oc = ObjectContainer(title2 = title, view_group = 'Pictures')
    photoObject = None
    #request.load()
    #stream = simplejson.loads(request.content)
    #s = simplejson.dumps(stream, sort_keys=True, indent=4 * ' ')
    Log.Debug('Getting JSON from url:' + url)
    stream = JSON.ObjectFromURL(url)
    Log.Debug('Got JSON from url:' + url)
    #Log.Debug('\n'.join([l.rstrip() for l in  s.splitlines()]))
    for data in stream['data']:
        photoObject = getPhotoObject(data)
        
        if (photoObject != None):
            oc.add(photoObject)
    
    if 'pagination' in stream:        
        pagination = stream['pagination']
        if pagination != None:
            nextUrl = pagination['next_url']      
            oc.add(DirectoryObject(key = Callback(morePhotos, url=nextUrl, title=title), title = 'Next...'))
        
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

def morePhotos(title,  url):
    Log.Debug('Next URL called: ' + url)
    return readStream(title = title, url = url)

def getThumb(url):
  try:
    Log.Debug('Calling thumb for url: ' + url)
    data = HTTP.Request(url, cacheTime = CACHE_1MONTH).content
    return DataObject(data, 'image/jpeg')
  except:
    Log.Debug('getThumb. exception happened!')
    return Redirect(R(Resources.ICON))
    
   
