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

    oc = ObjectContainer(view_group='Details')

    oc.add(DirectoryObject(key = Callback(PopularStream), title = 'Popular', tagline='The most popular', summary='The recent popular photos.'))
    oc.add(DirectoryObject(key = Callback(MyPhotoStream), title = 'My Photos', summary='Photos I have done.'))
    
    oc.add(DirectoryObject(key = Callback(ZurichStream), title = 'Zurich', tagline='Photos from Zurich', summary='These are photos from Zurich'))
    oc.add(DirectoryObject(key = Callback(NewYorkStream), title = 'New York', tagline='Photos from New York', summary='These are photos from New York'))
    oc.add(DirectoryObject(key = Callback(ParisStream), title = 'Paris', tagline='Photos from Paris', summary='These are photos from Paris')) 
  
    oc.add(DirectoryObject(key = Callback(LoginItem), title = 'Login', tagline='Login', summary='Login to Instagram'))  
    oc.add(PrefsObject(title='Your preferences', tagline='So you can set preferences', summary='lets you set preferences'))
    return oc

def PopularStream():
    oc = InstaStream.getPopularStream()
    return oc

def MyPhotoStream():
    oc = InstaStream.getOwnPhotosStream()
    return oc
    
def ZurichStream():
    oc = InstaStream.getTagStream(tag = 'zurich')
    return oc

def NewYorkStream():
    oc = InstaStream.getTagStream(tag = 'newyork')
    return oc

def ParisStream():
    oc = InstaStream.getTagStream(tag = 'paris')
    return oc

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
    
    
  
