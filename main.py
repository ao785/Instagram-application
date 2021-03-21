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
from myprofil import MyProfil
from listuser import ListUser
from listpost import ListPost
from myfollower import MyFollower
from myfollowing import MyFollowing
from mycomment import MyComment
from listcomment import ListComment
from datetime import datetime
from allcomments import AllComments

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''

        user = users.get_current_user() #boolean

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser_key = ndb.Key('MyUser', user.user_id()) #generate a key for MyUser type
            myuser = myuser_key.get()
            my_follow = Follow.query(Follow.user == myuser)
            if myuser == None: # if we find the key or not here not
                myuser = MyUser(id=user.user_id(), email_address = user.email(), user_id = user.user_id())
                myfollow = Follow(user=myuser)
                myuser.put() #commit myuser in datastore
                myfollow.put()

            key = ndb.Key('ListUser', 'default')
            list_user = key.get()
            if list_user == None:
                list_user = ListUser(id='default')
                list_user.put()

            my_following_post = MyPost.query()
            my_post = MyPost.query(MyPost.creator == myuser)
            list_comment = ListComment.query()

            list_post = ListPost.query(ListPost.user == myuser)
            if list_post.count() == 0:
                my_list_post = ListPost(user=myuser)
                for i in my_following_post:
                    for j in my_follow:
                        for k in j.following:
                            if i.creator == k:
                                my_list_post.list_post.append(i)
                for i in my_post:
                    my_list_post.list_post.append(i)
                my_list_post.list_post = sorted(my_list_post.list_post, key=lambda post: post.creation_time, reverse=True)
                if len(my_list_post.list_post) > 50:
                    my_list_post.list_post = my_list_post.list_post[0:50]
                my_list_post.put()
            else:
                for i in list_post:
                    i.key.delete()
                my_list_post = ListPost(user=myuser)
                for i in my_following_post:
                    for j in my_follow:
                        for k in j.following:
                            if i.creator == k:
                                my_list_post.list_post.append(i)
                for i in my_post:
                    my_list_post.list_post.append(i)
                my_list_post.list_post = sorted(my_list_post.list_post, key=lambda post: post.creation_time, reverse=True)
                if len(my_list_post.list_post) > 50:
                    my_list_post.list_post = my_list_post.list_post[0:50]
                my_list_post.put()


            template_values = {
                'url' : url,
                'url_string' : url_string,
                'user' : user,
                'upload_url' : blobstore.create_upload_url('/upload'),
                'list_user' : list_user,
                'my_following_post': my_following_post,
                'my_follow': my_follow,
                'list_post': list_post,
                'list_comment': list_comment,
            }


        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

            template_values = {
                'url' : url,
                'url_string' : url_string,
            }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Research':
            key = ndb.Key('ListUser', 'default')
            list_user = key.get()
            del list_user.list_user
            research = self.request.get('email_address')
            research_user = MyUser.query(MyUser.email_address == research)
            for i in research_user:
                list_user.list_user.append(i)
            list_user.put()
            self.redirect('/')

        if self.request.get('button') == 'Add comment':
            post_id = self.request.get('post_id')
            comment = self.request.get('comment')

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            my_comment = MyComment(user=myuser, comment=comment, creation_time=datetime.now())
            my_comment.put()
            list_comment = ListComment.query(ListComment.post_id == post_id)
            for i in list_comment:
                i.list_comment.append(my_comment)
                i.list_comment = sorted(i.list_comment, key=lambda comment: comment.creation_time)
                i.put()
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadHandler),
    ('/profil', MyProfil),
    ('/profil/follower',MyFollower),
    ('/profil/following', MyFollowing),
    ('/allcomments', AllComments),
], debug=True)
