from models.comment import Comment
from bloghandler import BlogHandler
from controllers import helpers as utils
from google.appengine.ext import ndb

import time
import logging


class NewComment(BlogHandler):

    def post(self):
        if not self.user:
            self.redirect('/login')
            return
        postId = int(self.request.get('postId'))
        content = self.request.get('content')
        comment = Comment(parent=utils.comment_key(),
                          userId=self.user.key.id(),
                          postId=postId,
                          content=content)
        comment.put()
        # For redirect to show new result
        time.sleep(0.1)
        self.redirect('/blog/%s' % str(postId))


class DeleteComment(BlogHandler):
    def post(self):
        if not self.user:
            self.redirect('/login')
            return

        commentId = int(self.request.get('commentId'))
        key = ndb.Key('Comment', int(commentId), parent=utils.comment_key())
        commentEnt = key.get()
        if not commentEnt:
            self.error(404)
            return
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
            self.redirect('/login')
            return

        commentId = int(self.request.get('commentId'))
        content = self.request.get('content')
        key = ndb.Key('Comment', int(commentId), parent=utils.comment_key())
        commentEnt = key.get()
        if not commentEnt:
            self.error(404)
            return
        if commentEnt.userId != self.user.key.id():
            error = "You can not edit comment of other author"
            self.redirect('/blog/%s?error=%s' %
                          (str(commentEnt.postId), error))
            return

        commentEnt.content = content
        commentEnt.put()
        time.sleep(0.1)
        self.redirect('/blog/%s' % str(commentEnt.postId))
