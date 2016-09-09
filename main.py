
import webapp2
import jinja2
import os
import cgi
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


class Post(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Index(webapp2.RequestHandler):


    def get(self):
        test= db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 1")
        latest = self.request.get("latest")
        article = self.request.get("article")
        link = self.request.get("link")
        t = jinja_env.get_template("Index.html")
        response = t.render(latest = test, article = article)
        self.response.write(response)



class NewPost(webapp2.RequestHandler):

    def renderForm(self, title="", post="", error=""):
        t = jinja_env.get_template("newpostform.html")
        response = t.render(title = title, post = post, error = error)
        self.response.write(response)
    def get(self):
        self.renderForm()

    def post(self):
        blogTitle = self.request.get("title")
        blogPost = self.request.get("post")
        if blogTitle and blogPost:
            newPost = Post(title = blogTitle, blog = blogPost)
            #self.redirect("/?latest="+ newPost.title + "&article=" + newPost.blog + "&link=" + link)
            newPost.put()
            link = newPost.key().id()
            self.redirect("/blog/"+ str(link))
        else:
            error = "Please enter a title and post"
            self.renderForm(error = error, title= blogTitle, post = blogPost)

class Blog(webapp2.RequestHandler):
    def get(self):
        latestEntries = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("blog.html")
        response = t.render(latestEntries = latestEntries)
        self.response.write(response)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        singleEntry = Post.get_by_id(int(id))
        t = jinja_env.get_template("singlepost.html")
        response = t.render(title=singleEntry.title, body=singleEntry.blog)
        self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', Index),
    ("/newpost", NewPost),
    ("/blog", Blog),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
