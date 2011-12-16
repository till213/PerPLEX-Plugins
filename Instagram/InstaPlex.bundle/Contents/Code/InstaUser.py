'''
Created on 16.12.2011

@author: Oliver Knoll
'''

import WebKeys

def search(name):
    '''Searches the user given by it's name and returns its ID; None if not found'''
    id = None
    token = Data.Load('oauthtoken')
    url = WebKeys.SEARCH_USER_URL % name + token
    stream = JSON.ObjectFromURL(url)
    #Log.Debug('\n'.join([l.rstrip() for l in  str(stream).splitlines()]))
    if stream != None:
        data = stream['data']
        if len(data) > 0:
            Log.Debug('Data: ' + str(data[0]))
            id = data[0]['id']
    return id
    
    
   
