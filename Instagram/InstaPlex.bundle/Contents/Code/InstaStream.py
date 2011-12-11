'''
Created on 04.12.2011

@author: Oliver Knoll
'''

import WebKeys
import Resources
    
def getPopularStream():
    '''Retrieves the Popular photo stream'''
    token = Data.Load('oauthtoken')
    
    title = "Popular"
    request = HTTP.Request(WebKeys.POPULAR_URL)
    return readStream(title, WebKeys.POPULAR_URL)
 
def getOwnPhotosStream():
    '''Retrieves the user photos; user needs to be logged in, that is a valid OAuth 2 token is necessary.'''
    token = Data.Load('oauthtoken')
    
    title = "My Photos"
    request = HTTP.Request(WebKeys.MY_PHOTOS_URL + token)
    return readStream(title, WebKeys.MY_PHOTOS_URL + token)

def getTagStream(tag, name = None):
    '''Retrieves the Instagram photo stream, given by its tag and returns a MediaContainer containing the photo URLs
    named name'''
    title = None
    if (name != None):
        title = name
    else:
        title = tag
    request = HTTP.Request(WebKeys.TAG_STREAM_URL % tag) 
    return readStream(title, WebKeys.TAG_STREAM_URL % tag)

def readStream(title, url):
    dir = MediaContainer(title2 = title, viewGroup = 'Pictures')
    photoItem = None
    #request.load()
    #stream = simplejson.loads(request.content)
    stream = JSON.ObjectFromURL(url)
    #s = simplejson.dumps(stream, sort_keys=True, indent=4 * ' ')
    #Log.Debug('\n'.join([l.rstrip() for l in  s.splitlines()]))
    for data in stream['data']:
        photoItem = getPhotoItem(data)
        
        if (photoItem != None):
            dir.Append(photoItem)
            
    pagination = stream['pagination']
    if pagination != None:
        nextUrl = pagination['next_url']
        Log.Debug('Next URL: ' + str(nextUrl))            
        #dir.Append(PhotoItem(Function(nextUrlF), title="title", summary="summary", thumb=None))
        dir.Append(
            Function(
                DirectoryItem(
                    nextUrlF3,
                    'Next',
                    subtitle='Instagram',
                    summary='Tag: #newyork',
                    thumb=R(Resources.ICON),
                    art=R(Resources.ART)
                )
            )
        )
        
        
    return dir

def getPhotoItem(data):
    url = data['images']['standard_resolution']['url']
    thumbUrl = data['images']['thumbnail']['url']
    comment = None
    caption = None
    if len(data['comments']['data']) > 0:
        comment = data['comments']['data'][0]['text']
    if data['caption'] != None:
        caption = data['caption']['text']
    return PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl)

def nextUrlF3(sender):
    Log.Debug('Next URL called.')
    return MessageContainer(
        'Not implemented',
        'In real life, you would probably perform some search using python\nand then build a MediaContainer with items\nfor the results'
    )


       
   
