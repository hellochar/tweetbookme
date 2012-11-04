from bottle import route, run
import facebook
import pprint
from time import gmtime, strftime
import urllib2
import json
import urllib
import itertools

APP_ID = "125942107559245"
APP_SECRET = "b662899fe149bd0e552fd9a1f12b157f"

HOST = ""
TOKEN_STORE = {}
cookies = {}
ACCESS_TOKEN = "AAACEdEose0cBAONOmWh7pSwGUQXA05GwABy4nlhiwJi6XSG9YOFr7L9xaJUVZCmZBMB0Ou5kWVB4kfJcRW0jNaEA74bn2YuZAhegF2s5gZDZD"


def flatten(l):
    return list(itertools.chain(*l))

def grab_popular_tweet(names_array):
    def try_encode(name):
        try:
            return ["http://search.twitter.com/search.json?" + urllib.urlencode({"q": name, "result_type": "popular"})]
        except:
            return []

    urls_array = flatten([try_encode(name) for name in names_array])
    tweet_responses = []
    for url in urls_array:
        try:
            response = urllib2.urlopen(url)
            tweet_responses.append(json.load(response))
            print "correct " + url
        except urllib2.HTTPError, e:
            print "skipping " + url
            pass

    all_tweets = flatten([tweet['results'] for tweet in tweet_responses])
    useful_array = [(t["metadata"]["recent_retweets"], t["text"]) for t in all_tweets]
    sorted_tweets = sorted(useful_array, key=lambda x: x[0])

    if not sorted_tweets:
        return []
    return sorted_tweets[0][1]


@route('/')
def index_page():
    graph = facebook.GraphAPI(ACCESS_TOKEN)
    profile = graph.get_object("me")
    likes = graph.get_connections("me", "likes") 
    formatted = pprint.pformat(likes)

    names_array = [like["name"] for like in likes["data"]]

    chunks=[names_array[x:x+100] for x in xrange(0, len(data), 100)]
    for chunk in chunks:
        tweet_maybe = grab_popular_tweet(chunk)
        if tweet_maybe:
            graph.put_wall_post("test message:" + tweet_maybe)
            return '<br>'.join(chunk)

@route('/callback/')
def callback_page():
    # note: the OAuth spec calls it 'oauth_token', but it's
    # actually just a request_token_key...
    request_token_key = bottle.request.params['code']
    if not request_token_key:
        return "Expected a request token key back!"

    request_token = TOKEN_STORE[request_token_key]
    access_token = sess.obtain_access_token(request_token)
    TOKEN_STORE[access_token.key] = access_token
    cookies['access_token_key'] = access_token.key
    return bottle.redirect('/viewfiles/')
  
@route('/complete_link/')
def complete():
  return 'Link complete'

def get_session():
    return session.FacebookSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
  
def get_client(access_token):
    sess = get_session()
    sess.set_token(access_token.key, access_token.secret)
    return client.DropboxClient(sess)

run(host='localhost', port=80, debug=True)
