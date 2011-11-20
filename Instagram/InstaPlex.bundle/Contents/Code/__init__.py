import simplejson
import InstaAuth
import WebKeys

PHOTOS_PREFIX = "/photos/instaplex"

NAME = L('Instagram Title')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART  = 'art-default.jpg'
ICON = 'icon-default.png'

token = None

####################################################################################################

def Start():

    ## make this plugin show up in the 'Photos' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(PHOTOS_PREFIX, PhotosMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("Pictures", viewMode="Pictures", mediaType="photos")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
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
            "Success",
            "User and password provided ok"
        )
    else:
        return MessageContainer(
            "Error",
            "You need to provide both a user and password"
        )
        

#### the rest of these are user created functions and
#### are not reserved by the plugin framework.
#### see: http://dev.plexapp.com/docs/Functions.html for
#### a list of reserved functions above



#
# Example main menu referenced in the Start() method
# for the 'Photos' prefix handler
#

def PhotosMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")


    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                PopularStream,
                "Popular",
                subtitle="Instagram",
                summary="The recent popular photos",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                MyPhotoStream,
                "My Photos",
                subtitle="Instagram",
                summary="Your own photos",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                ZurichStream,
                "Zurich",
                subtitle="Instagram",
                summary="Tag: #zurich",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                NewYorkStream,
                "New York",
                subtitle="Instagram",
                summary="Tag: #newyork",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                ParisStream,
                "Paris",
                subtitle="Instagram",
                summary="Tag: #paris",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    
    dir.Append(
        Function(
            DirectoryItem(
                LoginItem,
                "Login",
                subtitle="Login",
                summary="Login to Instagram New",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
  
    # Part of the "search" example 
    # see also:
    #   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
    dir.Append(
        Function(
            InputDirectoryItem(
                SearchResults,
                "Search title",
                "Search subtitle",
                summary="This lets you search stuff",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )

  
    # Part of the "preferences" example 
    # see also:
    #  http://dev.plexapp.com/docs/Objects.html#PrefsItem
    #  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
    #  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs 
    dir.Append(
        PrefsItem(
            title="Your preferences",
            subtile="So you can set preferences",
            summary="lets you set preferences",
            thumb=R(ICON)
        )
    )

    # ... and then return the container
    return dir

def PopularStream(sender):
    
    caption = ""
    comment = ""

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
    
    dir = MediaContainer(title2 = 'Popular', viewGroup = 'Pictures')
    
    request = HTTP.Request(WebKeys.POPULAR_URL + WebKeys.CLIENT_ID, cacheTime=0)
    request.load()
    Log.Debug("---- Received object: ")
    # Log.Debug(request.content)
    popular = simplejson.loads(request.content)
    #Log.Debug(popular)
    for data in popular['data']:
        #Log.Debug("Data: ")
        #Log.Debug(data['images']['standard_resolution']['url'])     
        url = data['images']['standard_resolution']['url']
        thumbUrl = data['images']['thumbnail']['url']
        Log.Debug('Comment:')
        if len(data['comments']['data']) > 0:
            comment = data['comments']['data'][0]['text']
            Log.Debug(comment)
        else:
            comment = ""
        Log.Debug('Caption: ')
        Log.Debug(data['caption'])
        if data['caption'] != None:
            caption = data['caption']['text']
        else:
            caption = ""
        dir.Append(PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl))
    
    return dir

def MyPhotoStream(sender):
    
    caption = ""
    comment = ""

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
    
    dir = MediaContainer(title2 = 'Popular', viewGroup = 'Pictures')
    token = Data.Load("oauthtoken")
    Log.Debug("MyPhotoStream: oauthtoken: " + token)
    request = HTTP.Request(WebKeys.MY_PHOTOS_URL + token)
    request.load()
    Log.Debug("---- Received object: ")
    # Log.Debug(request.content)
    popular = simplejson.loads(request.content)
    #Log.Debug(popular)
    for data in popular['data']:
        #Log.Debug("Data: ")
        #Log.Debug(data['images']['standard_resolution']['url'])     
        url = data['images']['standard_resolution']['url']
        thumbUrl = data['images']['thumbnail']['url']
        Log.Debug('Comment:')
        if len(data['comments']['data']) > 0:
            comment = data['comments']['data'][0]['text']
            Log.Debug(comment)
        else:
            comment = ""
        Log.Debug('Caption: ')
        Log.Debug(data['caption'])
        if data['caption'] != None:
            caption = data['caption']['text']
        else:
            caption = ""
        dir.Append(PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl))
    
    return dir
    
def ZurichStream(sender):
    
    caption = ""
    comment = ""

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
    
    dir = MediaContainer(title2 = 'Zurich', viewGroup = 'Pictures')
    
    request = HTTP.Request(WebKeys.ZURICH_URL + WebKeys.CLIENT_ID, cacheTime=0)
    request.load()
    Log.Debug("---- Received object: ")
    Log.Debug(request.content)
    popular = simplejson.loads(request.content)
    #Log.Debug(popular)
    for data in popular['data']:
        #Log.Debug("Data: ")
        #Log.Debug(data['images']['standard_resolution']['url'])     
        url = data['images']['standard_resolution']['url']
        thumbUrl = data['images']['thumbnail']['url']
        Log.Debug('Comment:')
        if len(data['comments']['data']) > 0:
            comment = data['comments']['data'][0]['text']
            Log.Debug(comment)
        else:
            comment = ""
        Log.Debug('Caption: ')
        Log.Debug(data['caption'])
        if data['caption'] != None:
            caption = data['caption']['text']
        else:
            caption = ""
        dir.Append(PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl))
    
    return dir

def NewYorkStream(sender):
    
    caption = ""
    comment = ""

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
    
    dir = MediaContainer(title2 = 'New York', viewGroup = 'Pictures')
    
    request = HTTP.Request(WebKeys.NEWYORK_URL + WebKeys.CLIENT_ID, cacheTime=0)
    request.load()
    Log.Debug("---- Received object: ")
    Log.Debug(request.content)
    popular = simplejson.loads(request.content)
    #Log.Debug(popular)
    for data in popular['data']:
        #Log.Debug("Data: ")
        #Log.Debug(data['images']['standard_resolution']['url'])     
        url = data['images']['standard_resolution']['url']
        thumbUrl = data['images']['thumbnail']['url']
        Log.Debug('Comment:')
        if len(data['comments']['data']) > 0:
            comment = data['comments']['data'][0]['text']
            Log.Debug(comment)
        else:
            comment = ""
        Log.Debug('Caption: ')
        Log.Debug(data['caption'])
        if data['caption'] != None:
            caption = data['caption']['text']
        else:
            caption = ""
        dir.Append(PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl))
    
    return dir

def ParisStream(sender):
    
    caption = ""
    comment = ""

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)
    
    dir = MediaContainer(title2 = 'Paris', viewGroup = 'Pictures')
    
    request = HTTP.Request(WebKeys.PARIS_URL + WebKeys.CLIENT_ID, cacheTime=0)
    request.load()
    Log.Debug("---- Received object: ")
    Log.Debug(request.content)
    popular = simplejson.loads(request.content)
    #Log.Debug(popular)
    for data in popular['data']:
        #Log.Debug("Data: ")
        #Log.Debug(data['images']['standard_resolution']['url'])     
        url = data['images']['standard_resolution']['url']
        thumbUrl = data['images']['thumbnail']['url']
        Log.Debug('Comment:')
        if len(data['comments']['data']) > 0:
            comment = data['comments']['data'][0]['text']
            Log.Debug(comment)
        else:
            comment = ""
        Log.Debug('Caption: ')
        Log.Debug(data['caption'])
        if data['caption'] != None:
            caption = data['caption']['text']
        else:
            caption = ""
        dir.Append(PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl))
    
    return dir

def LoginItem(sender):
    
    global token   
    Log.Debug("InstaAuth Inst")
    instaAuth = InstaAuth.InstaAuth(clientId = WebKeys.CLIENT_ID, redirectUri = WebKeys.REDIRECT_URI)

    token = instaAuth.authorize()
    Log.Debug("LoginItem: token: " + str(token))
    Data.Save("oauthtoken", data = token)
    
    return


# Part of the "search" example 
# query will contain the string that the user entered
# see also:
#   http://dev.plexapp.com/docs/Objects.html#InputDirectoryItem
def SearchResults(sender,query=None):
    return MessageContainer(
        "Not implemented",
        "In real life, you would probably perform some search using python\nand then build a MediaContainer with items\nfor the results"
    )
    
  
