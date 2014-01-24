import unittest
import os


from google.appengine.ext import testbed, ndb
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import taskqueue_stub
from google.appengine.api import urlfetch_stub

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
ds_stub = datastore_file_stub.DatastoreFileStub('YOUR_APP_HANDLE',
                                                'PATH_TO_YOUR_DATASTORE')
apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', ds_stub)
mc_stub = memcache_stub.MemcacheServiceStub()
apiproxy_stub_map.apiproxy.RegisterStub('memcache', mc_stub)
tq_stub = taskqueue_stub.TaskQueueServiceStub()
apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', tq_stub)
uf_stub = urlfetch_stub.URLFetchServiceStub()
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', uf_stub)
os.environ['APPLICATION_ID'] = 'YOUR_APP_HANDLE'


class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def SimpleTest(self):
        self.assertTrue(1 + 1 == 2)
