import cherrypy
import sys
import os, os.path
import random
import string
import json
from elasticsearch import Elasticsearch


class StreamMiner(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')
	#return "Hello world!"


@cherrypy.expose
class StreamMiningWebService(object):
        @cherrypy.tools.accept(media='text/plain')
        def GET(self):
            return cherrypy.session['mystring']

        def POST(self, coord_str,dist_str):
            cherrypy.log("coord_str  --> "+coord_str+" -> "+dist_str)
            es = Elasticsearch('search-tweetmine-swvqmlh2ustsro4zkee6xxzh44.us-east-2.es.amazonaws.com',port=80, maxsize=25)
            query = '{' \
                  '"query": {' \
                  ' "bool" : {' \
                  ' "must" : {' \
                  ' "match_all" : {}' \
                  ' },' \
                  '"filter" : {' \
                  '"geo_distance" : {' \
                  ' "distance" : "'+dist_str+'km",' \
                  ' "location" : [ '+coord_str+' ] ' \
                  ' }' \
                  ' }' \
                  ' }' \
                  '}' \
                  '}'
            data = []
            res = es.search(index="mining_index", doc_type="tweet", body=query)
            #print("%d documents found" % res['hits']['total'])
            for doc in res['hits']['hits']:
                #print("%s %s " % (doc['_id'], doc['_source']['location']))
                data.append(doc['_source'])


            #some_string = ''.join(random.sample(string.hexdigits, int(length)))
            cherrypy.session['mystring'] = coord_str
            print (json.dumps(data))
            return json.dumps(data)

        def PUT(self, another_string):
            cherrypy.session['mystring'] = another_string

        def DELETE(self):
            cherrypy.session.pop('mystring', None)



if __name__ == '__main__':
    cherrypy.log("Starting ------>")
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    conf1 = {'global': {'server.socket_host':'0.0.0.0','server.socket_port': 8080}}
    conf2 = {'global': {'server.socket_host': '0.0.0.0', 'server.socket_port': 8080},
             '/': {
                 'tools.sessions.on': True,
                 'tools.staticdir.root': os.path.abspath(os.getcwd())
             },
             '/generator': {
                 'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                 'tools.response_headers.headers': [('Content-Type', 'text/plain')],
             },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
                }
             }
    webapp = StreamMiner()
    webapp.generator  = StreamMiningWebService()
    cherrypy.quickstart(webapp, '/', conf2 )
    cherrypy.log("Stopping ------>")
