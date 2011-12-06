import InstaAuth
#import InstaStream
import WebKeys
import Resources

PHOTOS_PREFIX = '/photos/instaplex'

NAME = L('Instagram Title')

token = None

####################################################################################################

def Start():

    ## make this plugin show up in the 'Photos' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(PHOTOS_PREFIX, PhotosMainMenu, NAME, Resources.ICON, Resources.ART)

    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('Details', viewMode='InfoList', mediaType='items')
    Plugin.AddViewGroup('Pictures', viewMode='Pictures', mediaType='photos')

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = 'List'
    MediaContainer.art = R(Resources.ART)
    DirectoryItem.thumb = R(Resources.ICON)
    VideoItem.thumb = R(Resources.ICON)
    
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
        

def PhotosMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # 'sub-folders', videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup='Details')


    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                PopularStream,
                'Popular',
                subtitle='Instagram',
                summary='The recent popular photos',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                MyPhotoStream,
                'My Photos',
                subtitle='Instagram',
                summary='Your own photos',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                ZurichStream,
                'Zurich',
                subtitle='Instagram',
                summary='Tag: #zurich',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                NewYorkStream,
                'New York',
                subtitle='Instagram',
                summary='Tag: #newyork',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                ParisStream,
                'Paris',
                subtitle='Instagram',
                summary='Tag: #paris',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                LoginItem,
                'Login',
                subtitle='Login',
                summary='Login to Instagram New',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
  
    # Part of the 'search' example 
    # see also:
    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
    dir.Append(
        Function(
            InputDirectoryItem(
                SearchResults,
                'Search title',
                'Search subtitle',
                summary='This lets you search stuff',
                thumb=R(Resources.ICON),
                art=R(Resources.ART)
            )
        )
    )
  
    # Part of the 'preferences' example 
    # see also:
    #  http://dev.plexapp.com/docs/Objects.html#PrefsItem
    #  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
    #  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs 
    dir.Append(
        PrefsItem(
            title='Your preferences',
            subtile='So you can set preferences',
            summary='lets you set preferences',
            thumb=R(Resources.ICON)
        )
    )

    # ... and then return the container
    return dir

def PopularStream(sender):
    
#    instaStream = InstaStream.InstaStream();
    dir = getPopularStream()
    return dir

def MyPhotoStream(sender):
    
#    instaStream = InstaStream.InstaStream();
    dir = getOwnPhotosStream()
    return dir
    
def ZurichStream(sender):
    
#    instaStream = InstaStream.InstaStream();
    dir = getTagStream(tag = 'zurich')
    return dir

def NewYorkStream(sender):
    
#    instaStream = InstaStream.InstaStream();
    dir = getTagStream(tag = 'newyork')
    return dir

def ParisStream(sender):
    
#    instaStream = InstaStream.InstaStream();
    dir = getTagStream(tag = 'paris')
    return dir

def LoginItem(sender):
    
    global token   
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
def SearchResults(sender,query=None):
    return MessageContainer(
        'Not implemented',
        'In real life, you would probably perform some search using python\nand then build a MediaContainer with items\nfor the results'
    )
    
def getPopularStream():
    '''Retrieves the Popular photo stream'''
    token = Data.Load('oauthtoken')
    
    title = "Popular"
    request = HTTP.Request(WebKeys.POPULAR_URL + token)
    return readStream(title, WebKeys.POPULAR_URL + token)
 
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
    #s = simplejson.dumps(stream, sort_keys=True, indent=4 * ' ')
    stream = JSON.ObjectFromURL(url)
    #Log.Debug('\n'.join([l.rstrip() for l in  s.splitlines()]))
    for data in stream['data']:
        photoItem = getPhotoItem(data)
        
        if (photoItem != None):
            dir.Append(photoItem)
            
    pagination = stream['pagination']
    if pagination != None:
        nextUrl = pagination['next_url']
        Log.Debug('Next URL: ' + str(nextUrl))            
        dir.Append(Function(DirectoryItem(morePhotos, "Next"), url = nextUrl, title = title))
        
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

def morePhotos(sender, title,  url):
    Log.Debug('Next URL called: ' + url)
    request = HTTP.Request(url)
    return readStream(title, request)
    
    
  
