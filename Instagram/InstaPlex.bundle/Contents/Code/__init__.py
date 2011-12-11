import InstaAuth
#import InstaStream
import WebKeys
import Resources

PHOTOS_PREFIX = '/photos/instaplex'

TITLE = L('Instagram Photos')
####################################################################################################

def Start():

    Plugin.AddPrefixHandler(PHOTOS_PREFIX, PhotosMainMenu, TITLE, Resources.ICON, Resources.ART)

    Log.Debug('Start: Adding View Groups...')
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('Details', viewMode='InfoList', mediaType='items')
    Plugin.AddViewGroup('Pictures', viewMode='Pictures', mediaType='photos')

    ObjectContainer.title1 = TITLE
    ObjectContainer.view_group = 'List'
    ObjectContainer.art = R(Resources.ART)
    
    DirectoryObject.thumb = R(Resources.ICON)
    DirectoryObject.art = R(Resources.ART)
    
    HTTP.CacheTime = CACHE_1HOUR
    
# see:
#  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs
def ValidatePrefs():
    u = Prefs['username']
    p = Prefs['password']
    ## do some checks and return a
    ## message container
    if( u and p ):
        return MessageContainer(
            'Success',
            'User and password provided ok'
        )
    else:
        return MessageContainer(
            'Error',
            'You need to provide both a user and password'
        )
        
@handler('/photos/instaplex', TITLE)
def PhotosMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # 'sub-folders', videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    oc = ObjectContainer(view_group='Details')

    oc.add(DirectoryObject(key = Callback(PopularStream), title = 'Popular', tagline='The most popular', summary='The recent popular photos.'))
    
    
#    oc.add(
#        Function(
#            DirectoryItem(
#                MyPhotoStream,
#                'My Photos',
#                subtitle='Instagram',
#                summary='Your own photos',
#                thumb=R(Resources.ICON),
#                art=R(Resources.ART)
#            )
#        )
#    )
#    
#    oc.add(
#        Function(
#            DirectoryItem(
#                ZurichStream,
#                'Zurich',
#                subtitle='Instagram',
#                summary='Tag: #zurich',
#                thumb=R(Resources.ICON),
#                art=R(Resources.ART)
#            )
#        )
#    )
#    
#    oc.Append(
#        Function(
#            DirectoryItem(
#                NewYorkStream,
#                'New York',
#                subtitle='Instagram',
#                summary='Tag: #newyork',
#                thumb=R(Resources.ICON),
#                art=R(Resources.ART)
#            )
#        )
#    )
#    
#    oc.Append(
#        Function(
#            DirectoryItem(
#                ParisStream,
#                'Paris',
#                subtitle='Instagram',
#                summary='Tag: #paris',
#                thumb=R(Resources.ICON),
#                art=R(Resources.ART)
#            )
#        )
#    )
#    

    #oc.add(DirectoryObject(key = Callback(LoginItem), title = 'Login', tagline='Login', summary='Login to Instagram'))
  
#    # Part of the 'search' example 
#    # see also:
#    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
#    oc.Append(
#        Function(
#            InputDirectoryItem(
#                SearchResults,
#                'Search title',
#                'Search subtitle',
#                summary='This lets you search stuff',
#                thumb=R(Resources.ICON),
#                art=R(Resources.ART)
#            )
#        )
#    )
  
    oc.add(PrefsObject(title='Your preferences', tagline='So you can set preferences', summary='lets you set preferences'))
    # ... and then return the container
    return oc

def PopularStream():
    
#    instaStream = InstaStream.InstaStream();
    oc = getPopularStream()
    return oc

def MyPhotoStream():
    
#    instaStream = InstaStream.InstaStream();
    oc = getOwnPhotosStream()
    return oc
    
def ZurichStream():
    
#    instaStream = InstaStream.InstaStream();
    oc = getTagStream(tag = 'zurich')
    return oc

def NewYorkStream():
    
#    instaStream = InstaStream.InstaStream();
    oc = getTagStream(tag = 'newyork')
    return oc

def ParisStream():
    
#    instaStream = InstaStream.InstaStream();
    oc = getTagStream(tag = 'paris')
    return oc

def LoginItem():
    
    # TODO: BAD! Don't use globals - store it in the context! (Per user, threading!)
    
    Log.Debug('InstaAuth Inst')
    instaAuth = InstaAuth.InstaAuth()

    token = instaAuth.authorize()
    Log.Debug('LoginItem: token: ' + str(token))
    Data.Save('oauthtoken', data = token)
    
    return


# Part of the 'search' example 
# query will contain the string that the user entered
# see also:
#   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
def SearchResults(query=None):
    return PopupDirectoryObject(
        title='Not implemented',
        summary='In real life, you would probably perform some search using python\nand then build a MediaContainer with items\nfor the results'
    )
    
def getPopularStream():
    '''Retrieves the Popular photo stream'''
    token = Data.Load('oauthtoken')
    
    title = "Popular"
    #request = HTTP.Request(WebKeys.POPULAR_URL + token)
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
            Log.Debug('Next URL: ' + str(nextUrl))            
            dir.Append(Function(DirectoryItem(morePhotos, "Next"), url = nextUrl, title = title))
        
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
    #request = HTTP.Request(url)
    return readStream(title = title, url = url)

def getThumb(url):
  try:
    Log.Debug('Calling thumb for url: ' + url)
    data = HTTP.Request(url, cacheTime = CACHE_1MONTH).content
    return DataObject(data, 'image/jpeg')
  except:
    Log.Debug('getThumb. exception happened!')
    return Redirect(R(Resources.ICON))
    
    
  
