from google.appengine.ext import ndb
from controllers import helpers as utils
from user import User
from post import Post


class Comment(ndb.Model):
    """Models an like to record with who liked which post,
       prevent user to like his own post or relike same post."""
    content = ndb.StringProperty(required=True)
    postId = ndb.IntegerProperty(required=True)
    userId = ndb.IntegerProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return utils.render_str('comment.html', comment=self,
                                author=User.by_id(self.userId).name
                                )
