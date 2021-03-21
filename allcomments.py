import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from google.appengine.ext import blobstore
from uploadhandler import UploadHandler

from myuser import MyUser
from follow import Follow
from mypost import MyPost
from listcomment import ListComment

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AllComments(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        post_id = self.request.get('post_id')
        my_post = MyPost.get_by_id(int(post_id))

        list_comment = ListComment.query()

        template_values = {
            'my_post' : my_post,
            'list_comment' : list_comment,
        }

        template = JINJA_ENVIRONMENT.get_template('allcomments.html')
        self.response.write(template.render(template_values))
