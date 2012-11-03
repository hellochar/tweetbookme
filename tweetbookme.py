import bottle
from bottle import route, run
from facebook import *

APP_KEY = ""
APP_SECRET = ""

HOST = ""
TOKEN_STORE = {}
cookies = {}

@route('/')
def index_page():
    sess = get_session()
    request_token = sess.obtain_request_token()
    TOKEN_STORE[request_token.key] = request_token
    
    callback = "http://%s/callback/" % (bottle.request.headers['host'])
    url = sess.build_authorize_url(request_token, oauth_callback=callback)
    prompt = """Click <a href="%s">here</a> to link with Dropbox."""
    return prompt % url 

def get_session():
    return session.FacebookSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
  
def get_client(access_token):
    sess = get_session()
    sess.set_token(access_token.key, access_token.secret)
    return client.DropboxClient(sess)