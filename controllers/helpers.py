import jinja2
import os
import hmac
from google.appengine.ext import ndb
import random
import hashlib
from string import letters

secret = 'a2h3d'

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

# Keys for nbd entities


def users_key(name='default'):
    return ndb.Key('users', name)


def blog_key(name='default'):
    return ndb.Key('blogs', name)


def comment_key(name='default'):
    return ndb.Key('comments', name)


def like_key(name='default'):
    return ndb.Key('likes', name)
