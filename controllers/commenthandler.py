from models.comment import Comment
from bloghandler import BlogHandler
from controllers import helpers as utils
from google.appengine.ext import ndb

import time
import logging


class NewComment(BlogHandler):

    def post(self):
        if not self.user:
            return self.redirect('/login')

        postId = int(self.request.get('postId'))
        content = self.request.get('content')
        comment = Comment(parent=utils.comment_key(),
                          userId=self.user.key.id(),
                          postId=postId,
                          content=content)
        comment.put()
        # Dealing with eventual consistency
        time.sleep(0.1)
        return self.redirect('/blog/%s' % str(postId))


class DeleteComment(BlogHandler):
    def post(self):
        if not self.user:
            return self.redirect('/login')

        commentId = int(self.request.get('commentId'))
        key = ndb.Key('Comment', int(commentId), parent=utils.comment_key())
        commentEnt = key.get()
        if not commentEnt:
            self.error(404)
            return self.render('404.html')
        if commentEnt.userId != self.user.key.id():
            error = "You can not delete comment of other author"
            self.redirect('/blog/%s?error=%s' %
                          (str(commentEnt.postId), error))
            return

        commentEnt.key.delete()
        time.sleep(0.1)
        self.redirect('/blog/%s' % str(commentEnt.postId))


class EditComment(BlogHandler):
    def post(self):
        if not self.user:
            return self.redirect('/login')

        commentId = int(self.request.get('commentId'))
        content = self.request.get('content')
        key = ndb.Key('Comment', int(commentId), parent=utils.comment_key())
        commentEnt = key.get()
        if not commentEnt:
            self.error(404)
            return self.render('404.html')
        if commentEnt.userId != self.user.key.id():
            error = "You can not edit comment of other author"
            self.redirect('/blog/%s?error=%s' %
                          (str(commentEnt.postId), error))
            return

        commentEnt.content = content
        commentEnt.put()
        time.sleep(0.1)
        return self.redirect('/blog/%s' % str(commentEnt.postId))
