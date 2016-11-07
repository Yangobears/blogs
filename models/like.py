from google.appengine.ext import ndb


class Like(ndb.Model):
    """Models an like to record with who liked which post,
       prevent user to like his own post or relike same post."""
    userId = ndb.IntegerProperty(required=True)
    postId = ndb.IntegerProperty(required=True)
