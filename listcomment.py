from google.appengine.ext import ndb
from mypost import MyPost
from mycomment import MyComment

class ListComment(ndb.Model):
    post = ndb.StructuredProperty(MyPost)
    list_comment = ndb.StructuredProperty(MyComment, repeated=True)
    post_id = ndb.StringProperty()
