from google.appengine.ext import ndb
from myuser import MyUser

class ListUser(ndb.Model):
    list_user = ndb.StructuredProperty(MyUser, repeated=True)
