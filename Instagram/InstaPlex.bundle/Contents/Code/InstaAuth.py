'''
Implements authorisation and authentication using OAuth 2.0 protocol with Instagram.

Created on 29.11.2011

@author: Oliver Knoll
'''

import urllib2
import urllib
import cookielib
import WebKeys

COOKIE_FILE = 'InstaCookie.txt'

class InstaAuth:
    
    myRedirectHandler = None
     
    def __init__(self):
        self.myRedirectHandler = MyHTTPRedirectHandler()
        cj = cookielib.LWPCookieJar(COOKIE_FILE)        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), self.myRedirectHandler)
        urllib2.install_opener(opener)
    
    def authorize(self):
        
        token = None
     
        try:
            # Login
            Log.Debug('Login in...')
            param = urllib.urlencode({'password' : Prefs['password'], 'username': Prefs['username']})
            req = urllib2.Request(WebKeys.LOGIN_URL, data = param)
            response = urllib2.urlopen(req)
        except urllib2.HTTPError:
            Log.Debug('HTTP error happened')
        
        try:
            # Authorize
            Log.Debug('Authorise...')
            req = urllib2.Request(WebKeys.HTTPS_AUTH_URL)
            response = urllib2.urlopen(req)
        except urllib2.HTTPError:
            Log.Debug('HTTP error happened')
            
        token = self.myRedirectHandler.getToken()    
        if token == None:
            try:
                # Allow application
                param = urllib.urlencode({'allow' : 'Yes'})
                req = urllib2.Request(WebKeys.HTTP_AUTH_URL, data=param)
                response = urllib2.urlopen(req)
            except urllib2.HTTPError:
                Log.Debug('HTTP error happened')
        
        Log.Debug('Returning the Token:')
        Log.Debug(self.myRedirectHandler.getToken())
        return self.myRedirectHandler.getToken()
        
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    
    token = None    
    
    def http_error_302(self, req, fp, code, msg, headers):
        if 'location' in headers:
            newurl = headers.getheaders('location')[0]
        elif 'uri' in headers:
            newurl = headers.getheaders('uri')[0]
        
        if newurl.startswith(WebKeys.REDIRECT_URI):
            tokens = newurl.split('=')
            self.token = tokens[1]
        else:
            self.token = None
        
        return None
    
    def getToken(self):
        return self.token

    http_error_301 = http_error_303 = http_error_307 = http_error_302   
