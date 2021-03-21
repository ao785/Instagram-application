from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from mypost import MyPost
from google.appengine.api.images import get_serving_url
from listcomment import ListComment


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        my_post = MyPost(
            text_caption=self.request.get('text_caption'),
            image=get_serving_url(upload.key()),
            creator=myuser,
            creation_time=blobinfo.creation)
        my_post.put()
        my_post.post_id = str(my_post.key.id())
        my_post.put()
        list_comment = ListComment(post = my_post, post_id = str(my_post.key.id()))
        list_comment.put()
        self.redirect('/')
