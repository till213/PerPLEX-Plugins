import InstaAuth
import InstaStream
import InstaUser
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
    
    names = Prefs['users']
    users = Data.LoadObject('users')
    if users != None:
        for name in users.keys():
            if name not in names.split(' '):
                del users[name]
    else:
        users = {}
    
    for name in names.split(' '):
        
        if name in users.keys():
            id = users[name]
            if id == None:
                id = InstaUser.search(name = name)
                users[name] = id
        else:
            id = InstaUser.search(name = name)
            users[name] = id
            
    Data.SaveObject('users', users)
    
    Log.Debug('Users validated, count: ' + str(len(users)))    
    for user in users.keys():
        Log.Debug('User:' + user + ' ID: ' + users[user])
        
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
    
    category = Prefs['cities']
    if category != '':
        oc.add(DirectoryObject(key = Callback(TagsMenu, category =  'cities', summary = "Cities around the world"), title = 'Cities', summary='Cities around the world'))

    category = Prefs['nature']
    if category != '':
        oc.add(DirectoryObject(key = Callback(TagsMenu, category =  'nature', summary = "Nature"), title = 'Nature', summary='Nature'))
        
    category = Prefs['users']
    if category != '':
        oc.add(DirectoryObject(key = Callback(UsersMenu, category =  'users', summary = "Users"), title = 'Users', summary='Users'))

    oc.add(DirectoryObject(key = Callback(LoginItem), title = 'Login', tagline='Login', summary='Login to Instagram'))  
    oc.add(PrefsObject(title='Your preferences', tagline='So you can set preferences', summary='lets you set preferences'))
    return oc

def TagsMenu(category, summary):

    oc = ObjectContainer(view_group='Details')
   
    tags = Prefs[category]
    for tag in tags.split(' '):
        oc.add(DirectoryObject(key = Callback(TagStream, tag = tag), title = tag, summary = summary))
    return oc    

def UsersMenu(category, summary):

    users = {}
    oc = ObjectContainer(view_group='Details')
   
    users = Data.LoadObject('users')
    for user in sorted(users.iterkeys()):
        oc.add(DirectoryObject(key = Callback(UserStream, id = users[user], name = user), title = user, summary = summary))
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
def UserStream(id, name):
    oc = InstaStream.getUserStream(id = id, name = name)
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
    
    
  
