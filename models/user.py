from google.appengine.ext import ndb
from controllers import helpers as utils


class User(ndb.Model):
    """Models a User with email, password hash and email address."""
    name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=utils.users_key())

    @classmethod
    def by_name(cls, name):
        u = User.query(User.name == name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = utils.make_pw_hash(name, pw)
        return User(parent=utils.users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and utils.valid_pw(name, pw, u.pw_hash):
            return u
