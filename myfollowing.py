import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from google.appengine.ext import blobstore
from uploadhandler import UploadHandler

from myuser import MyUser
from follow import Follow

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MyFollowing(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user() #boolean
        id = self.request.get('id')
        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()

        my_follow = Follow.query(Follow.user == myuser)

        template_values = {
            'user' : user,
            'my_follow' : my_follow,
            'myuser': myuser,
            'id' : id,
        }

        template = JINJA_ENVIRONMENT.get_template('myfollowing.html')
        self.response.write(template.render(template_values))
