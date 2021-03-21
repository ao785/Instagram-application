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

class MyProfil(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user() #boolean
        id = self.request.get('id')
        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()

        my_follow = Follow.query()

        my_post = MyPost.query(MyPost.creator == myuser).order(-MyPost.creation_time)

        list_comment = ListComment.query()

        template_values = {
            'user' : user,
            'my_post' : my_post,
            'my_follow' : my_follow,
            'myuser': myuser,
            'id' : id,
            'list_comment' : list_comment,
        }

        template = JINJA_ENVIRONMENT.get_template('myprofil.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Follow':

            id = self.request.get('id')
            following_user_key = ndb.Key('MyUser', id)
            following_user = following_user_key.get()
            his_follower = Follow.query(Follow.user == following_user)

            user = users.get_current_user()
            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()
            my_following = Follow.query(Follow.user == my_user)

            for i in his_follower:
                for j in i.followers:
                    if j.user_id != my_user.user_id:
                        i.followers.append(my_user)
                        i.put()
            for i in my_following:
                for j in i.following:
                    if j.user_id != following_user:
                        i.following.append(following_user)
                        i.put()

            self.redirect('/')

        if self.request.get('button') == 'Unfollow':

            id = self.request.get('id')
            following_user_key = ndb.Key('MyUser', id)
            following_user = following_user_key.get()
            his_follower = Follow.query(Follow.user == following_user)

            user = users.get_current_user()
            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()
            my_following = Follow.query(Follow.user == my_user)

            for i in his_follower:
                for j in i.followers:
                    if j.email_address == my_user.email_address:
                        i.followers.remove(j)
                i.put()
            for i in my_following:
                for j in i.following:
                    if j.email_address == following_user.email_address:
                        i.following.remove(j)
                i.put()

            self.redirect('/')
        if self.request.get('button') == 'Return to main page':
            self.redirect('/')
