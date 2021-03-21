from google.appengine.ext import ndb
from myuser import MyUser

class MyComment(ndb.Model):
    comment = ndb.StringProperty()
    user = ndb.StructuredProperty(MyUser)
    creation_time = ndb.DateTimeProperty()
