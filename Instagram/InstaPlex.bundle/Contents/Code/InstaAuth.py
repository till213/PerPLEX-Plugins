'''
Created on 29.11.2011

@author: tknoll
'''

import urllib2
import urllib
import cookielib
import WebKeys

COOKIE_FILE = "InstaCookie.txt"

class InstaAuth:
    
    clientId = None
    redirectUri = None
    myRedirectHandler = None
     
    def __init__(self, clientId, redirectUri):
        self.clientId = clientId
        self.redirectUri = redirectUri
        self.myRedirectHandler = MyHTTPRedirectHandler()
        cj = cookielib.LWPCookieJar(COOKIE_FILE)        
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), self.myRedirectHandler)
        urllib2.install_opener(opener)
        
    def getClientId(self):
        return self.clienId
    
    def getRedirectUri(self):
        return self.redirectUri
    
    def authorize(self):
        
        token = None
     
        try:
            # Login
            Log.Debug('Login in: ' + WebKeys.LOGIN_URL % (self.clientId, self.redirectUri))
            param = urllib.urlencode({"password" : Prefs['password'], "username": Prefs['username']})
            req = urllib2.Request(WebKeys.LOGIN_URL % (self.clientId, self.redirectUri), data = param)
            response = urllib2.urlopen(req)
        except urllib2.HTTPError:
            Log.Debug("HTTP error happened")
        
        try:
            # Authorize
            Log.Debug('Authorise: ' + WebKeys.HTTPS_AUTH_URL % (self.clientId, self.redirectUri))
            req = urllib2.Request(WebKeys.HTTPS_AUTH_URL % (self.clientId, self.redirectUri))
            response = urllib2.urlopen(req)
        except urllib2.HTTPError:
            Log.Debug("HTTP error happened")
            
        token = self.myRedirectHandler.getToken()    
        if token == None:
            try:
                # Allow application
                param = urllib.urlencode({"allow" : "Yes"})
                Log.Debug('Allow: ' + WebKeys.HTTP_AUTH_URL % (self.clientId, self.redirectUri))
                req = urllib2.Request(WebKeys.HTTP_AUTH_URL % (self.clientId, self.redirectUri), data=param)
                response = urllib2.urlopen(req)
            except urllib2.HTTPError:
                Log.Debug("HTTP error happened")
        
        Log.Debug("Returning the Token:")
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
            tokens = newurl.split("=")
            self.token = tokens[1]
            Log.Debug("Token: " + tokens[1])
        else:
            self.token = None
        
        return None
    
    def getToken(self):
        return self.token

    http_error_301 = http_error_303 = http_error_307 = http_error_302   
