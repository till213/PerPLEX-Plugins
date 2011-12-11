import InstaAuth
import InstaStream
import WebKeys
import Resources

PHOTOS_PREFIX = '/photos/instaplex'

TITLE = L('Instagram Photos')

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
    
    HTTP.CacheTime = 0 #CACHE_1HOUR
    
    Log.Debug('**** Cities: ' + str(Prefs['cities']));
    

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
    
    subMenu = None

    Log.Debug('Instagram: Creating menu...')

    oc = ObjectContainer(view_group='Details')

    oc.add(DirectoryObject(key = Callback(PopularStream), title = 'Popular', summary='The recent popular photos'))
    oc.add(DirectoryObject(key = Callback(MyPhotoStream), title = 'My Photos', summary='Photos I have done'))
    
    cities = Prefs['cities']
    if cities != '':
        oc.add(DirectoryObject(key = Callback(TagsMenu, category =  'cities', summary = "Cities around the world"), title = 'Cities', summary='Cities around the world'))

    cities = Prefs['nature']
    if cities != '':
        oc.add(DirectoryObject(key = Callback(TagsMenu, category =  'nature', summary = "Nature"), title = 'Nature', summary='Nature'))

    oc.add(DirectoryObject(key = Callback(LoginItem), title = 'Login', tagline='Login', summary='Login to Instagram'))  
    oc.add(PrefsObject(title='Your preferences', tagline='So you can set preferences', summary='lets you set preferences'))
    return oc

def TagsMenu(category, summary):

    oc = ObjectContainer(view_group='Details')
   
    tags = Prefs[category]
    for tag in tags.split(' '):
        oc.add(DirectoryObject(key = Callback(TagStream, tag = tag), title = tag, summary = summary))
    return oc    

def PopularStream():
    oc = InstaStream.getPopularStream()
    return oc

def MyPhotoStream():
    oc = InstaStream.getOwnPhotosStream()
    return oc

@indirect
def TagStream(tag):
    oc = InstaStream.getTagStream(tag = tag)
    return oc

@indirect
def LoginItem():  
    Log.Debug('LoginItem CALLED. InstaAuth Inst')
    instaAuth = InstaAuth.InstaAuth()

    token = instaAuth.authorize()
    Data.Save('oauthtoken', data = token)
    return None

def getThumb(url):
  try:
    data = HTTP.Request(url, cacheTime = CACHE_1MONTH).content
    return DataObject(data, 'image/jpeg')
  except:
    Log.Debug('getThumb: no thumb data, redirecting to default ICON resource.')
    return Redirect(R(Resources.ICON))

def morePhotos(url, title, forward):
    return InstaStream.readStream(url = url, title = title, forward = forward)
    
    
  
