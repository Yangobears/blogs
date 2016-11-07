import webapp2

from controllers import helpers as utils
from controllers.userhandler import Login, Logout, Register, Signup
from controllers.posthandler import AllPosts, ViewPost, EditPost, DeletePost,\
                                NewPost, LikePost
from controllers.commenthandler import NewComment, DeleteComment, EditComment
from controllers.bloghandler import BlogHandler


class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/blogs', AllPosts),
                               ('/blog/(\d+)', ViewPost),
                               ('/blog/(\d+)/like', LikePost),
                               ('/blog/(\d+)/edit', EditPost),
                               ('/blog/(\d+)/delete', DeletePost),
                               ('/comment/new', NewComment),
                               ('/comment/delete', DeleteComment),
                               ('/comment/edit', EditComment),
                               ('/blog/new', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome)
                               ],
                              debug=True)
