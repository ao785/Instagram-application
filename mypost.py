from google.appengine.ext import ndb
from myuser import MyUser

class MyPost(ndb.Model):
    text_caption = ndb.StringProperty()
    image = ndb.BlobProperty()
    creator = ndb.StructuredProperty(MyUser)
    creation_time = ndb.DateTimeProperty()
    post_id = ndb.StringProperty()
