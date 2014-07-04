import json
import time
import urllib.request
import urllib.parse


class api:

    def __init__(self, credfile):
        self.creds = self.getcreds(credfile)
        self.api_key = self.creds['apikey']
        self.token = None
        self.tokentime = 1

    def getcreds(self, credfile):
        fh = open(credfile, 'r')
        creds = json.load(fh)
        fh.close()
        return creds

    def auth_getToken(self):
        # get lastfm token
        # Must use call, and set things up manually
        # doCall may call getToken causing massive recursion
        pm = {}
        pm['method'] = 'auth.getToken'
        pm['api_key'] = self.api_key
        pm['format'] = 'json'
        self.token = self.call(pm)
        self.tokentime = time.time()

    def tokenExpire(self):
        # Tokens expire after an hour.
        if time.time()-self.tokentime < 3600:
            return False
        return True

    def call(self, parameters):
        # raw call method
        domain = 'http://ws.audioscrobbler.com'
        apiversion = '2.0'
        querystring = urllib.parse.urlencode(parameters)
        requrl = "%s/%s/?%s" % (domain, apiversion, querystring)
        response = urllib.request.urlopen(requrl)
        str_response = response.readall().decode('utf-8')
        obj = json.loads(str_response)
        return obj

    def doCall(self, parameters):
        # helper call method
        # if you don't have a token, get one
        if self.tokentime is None:
            self.auth_getToken()
        # if token is stale, replace it
        if self.tokenExpire():
            self.auth_getToken()
        # xml, you've been good to us, but it's time to die.
        if 'format' not in parameters:
            parameters['format'] = 'json'
        if 'api_key' not in parameters:
            parameters['api_key'] = self.api_key
        return self.call(parameters)
