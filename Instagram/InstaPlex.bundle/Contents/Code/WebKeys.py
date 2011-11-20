'''
Created on 29.11.2011

@author: tknoll
'''

CLIENT_ID    = 'c5142704e6104afe89552d7d170e6915'
REDIRECT_URI = 'http://www.till-art.net/instaplex'

'''First arg (str): client ID Second arg (str): Redirect-URI'''
HTTPS_AUTH_URL = 'https://instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=token'
HTTP_AUTH_URL  = 'http://instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=token'
LOGIN_URL      = 'https://instagram.com/accounts/login/?next=/oauth/authorize/&client_id=%s&redirect_uri=%s&response_type=token'

# End points

POPULAR_URL = 'https://api.instagram.com/v1/media/popular?client_id='
MY_PHOTOS_URL = 'https://api.instagram.com/v1/users/self/media/recent?access_token='
ZURICH_URL = 'https://api.instagram.com/v1/tags/zurich/media/recent?client_id='
NEWYORK_URL = 'https://api.instagram.com/v1/tags/newyork/media/recent?client_id='
PARIS_URL = 'https://api.instagram.com/v1/tags/paris/media/recent?client_id='
