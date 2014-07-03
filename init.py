#!/usr/bin/env python
import lastfm

x = lastfm.api('./creds.json')
pm = {}
pm['method'] = 'auth.getToken'
result = x.call(pm)
print(result)
