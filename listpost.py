from google.appengine.ext import ndb
from mypost import MyPost
from myuser import MyUser

class ListPost(ndb.Model):
    user = ndb.StructuredProperty(MyUser)
    list_post = ndb.StructuredProperty(MyPost, repeated=True)
