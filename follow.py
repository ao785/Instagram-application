from google.appengine.ext import ndb
from myuser import MyUser

class Follow(ndb.Model):
    user = ndb.StructuredProperty(MyUser)
    followers = ndb.StructuredProperty(MyUser, repeated=True)
    following = ndb.StructuredProperty(MyUser, repeated=True)
