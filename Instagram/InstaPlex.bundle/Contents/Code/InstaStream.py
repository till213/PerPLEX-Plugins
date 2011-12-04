'''
Created on 04.12.2011

@author: Oliver Knoll
'''

import WebKeys

class InstaStream:
    def getStream(self, name, tag):
        dir = MediaContainer(title2 = 'Test', viewGroup = 'Pictures')
        photoItem = None
        request = HTTP.Request(WebKeys.TAG_STREAM_URL % tag, cacheTime=0)
        request.load()
        Log.Debug('- Received object: ')
        #Log.Debug(request.content)
        stream = simplejson.loads(request.content)
        #Log.Debug(stream)
        Log.Debug('Got Stream, iterating now...')
        try:
            for data in stream['data']:
                #Log.Debug('Data: ')
                #Log.Debug(data['images']['standard_resolution']['url'])     
                photoItem = self.getPhotoItem(data)
                
                if (photoItem != None):
                    Log.Debug("PhotoItem: ")
                    #Log.Debug('Appending photo item...')
                    dir.Append(photoItem)
        except Exception, e:
            Log.Debug('An exception happened.')
            Log.Debug(str(e))
        Log.Debug('---Returning dir...')
        return dir
    
    def getPhotoItem(self, data):
        url = data['images']['standard_resolution']['url']
        thumbUrl = data['images']['thumbnail']['url']
        comment = None
        caption = None
        #Log.Debug('Comment:')
        if len(data['comments']['data']) > 0:
            comment = data['comments']['data'][0]['text']
            Log.Debug(comment)
        #Log.Debug('Caption: ')
        #Log.Debug(data['caption'])
        if data['caption'] != None:
            caption = data['caption']['text']
        #Log.Debug('url: ' + url + ' title: ' + caption + ' Summary: ' + comment + ' thumb: ' + thumbUrl)
        return PhotoItem(url, title=caption, summary=comment, thumb=thumbUrl)
        
    
