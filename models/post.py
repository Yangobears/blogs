from controllers import helpers as utils
from google.appengine.ext import ndb


class Post(ndb.Model):
    """Models an individual post entry with title and content,
       also recording the create time and last modified time."""
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    author = ndb.StringProperty()
    likes = ndb.IntegerProperty(default=0)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        link = "/blog/%s" % str(self.key.id())
        return utils.render_str('post.html', p=self, link=link)
