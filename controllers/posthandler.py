from models.post import Post
from models.like import Like

from bloghandler import BlogHandler
from google.appengine.ext import ndb
from controllers import helpers as utils
import time


class AllPosts(BlogHandler):
    def get(self):
        posts = ndb.gql("select * from Post order by created desc limit 10")
        self.render('posts.html', posts=posts)


class ViewPost(BlogHandler):
    def get(self, post_id):
        error = self.request.get('error')
        key = ndb.Key('Post', int(post_id), parent=utils.blog_key())
        postEnt = key.get()
        if not postEnt:
            self.error(404)
            return
        postIdStr = str(postEnt.key.id())
        likeLink = '/blog/%s/like' % postIdStr
        editLink = '/blog/%s/edit' % postIdStr
        deleteLink = '/blog/%s/delete' % postIdStr

        permission = False
        if self.user and self.user.name == postEnt.author:
            permission = True
        comments = ndb.gql("select * from Comment where postId=%s" % postIdStr)
        self.render("specificpost.html",
                    post=postEnt,
                    likeLink=likeLink,
                    editLink=editLink,
                    deleteLink=deleteLink,
                    permission=permission,
                    comments=comments,
                    error=error
                    )


class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blogs')

        title = self.request.get('title')
        content = self.request.get('content')
        author = self.user.name

        if title and content and author:
            p = Post(parent=utils.blog_key(),
                     title=title,
                     content=content,
                     author=author)
            p_key = p.put()
            ident = p_key.id()
            time.sleep(0.1)

            self.redirect('/blog/%s' % str(p_key.id()))
        else:
            error = "title and content, please!"
            self.render("newpost.html", title=title, content=content,
                        author=author, error=error)


class EditPost(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/login')
            return

        key = ndb.Key('Post', int(post_id), parent=utils.blog_key())
        postEnt = key.get()
        if not postEnt:
            self.error(404)
            return
        if postEnt.author != self.user.name:
            error = "You can not edit post of other author"
            self.redirect('/blog/%s?error=%s' % (str(postEnt.key.id()), error))
            return

        self.render("editpost.html", post=postEnt,
                    cancelLink='/blog/%s' % str(key.id()))

    def post(self, post_id):
        title = self.request.get('title')
        content = self.request.get('content')
        key = ndb.Key('Post', int(post_id), parent=utils.blog_key())
        postEnt = key.get()

        if title and content:
            postEnt.title = title
            postEnt.content = content
            postEnt.put()
            time.sleep(0.1)
            self.redirect('/blog/%s' % str(key.id()))
        else:
            error = "title and content, please!"
            self.render("editpost.html", post=postEnt, error=error)


class DeletePost(BlogHandler):
    def post(self, post_id):
        if not self.user:
            self.redirect('/login')

        key = ndb.Key('Post', int(post_id), parent=utils.blog_key())
        postEnt = key.get()
        if not postEnt:
            self.error(404)
            return
        if postEnt.author != self.user.name:
            error = "You can not delete post of other author"
            self.redirect('/blog/%s?error=%s' % (str(postEnt.key.id()), error))
            return

        key.delete()
        time.sleep(0.1)

        self.redirect('/blogs')


class LikePost(BlogHandler):
    def post(self, post_id):
        if not self.user:
            self.redirect('/login')
        key = ndb.Key('Post', int(post_id), parent=utils.blog_key())
        postEnt = key.get()

        if not postEnt:
            self.error(404)
            return
        if self.user:
            if postEnt.author == self.user.name:
                error = "You cannot like your own post"
                url = '/blog/%s?error=%s' % (str(postEnt.key.id()), error)
                self.redirect(url)
                return

            else:
                query = Like.query(Like.userId == self.user.key.id(),
                                   Like.postId == key.id()).get()
                if query:
                    error = "You already like the post"
                    self.redirect('/blog/%s?error=%s' %
                                  (str(postEnt.key.id()), error))
                    return
                else:
                    l = Like(parent=utils.like_key(),
                             userId=self.user.key.id(), postId=key.id())
                    l.put()
                    postEnt.likes += 1
                    postEnt.put()
                    time.sleep(0.1)

                self.redirect('/blog/%s' % str(postEnt.key.id()))
