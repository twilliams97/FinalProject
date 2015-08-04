import jinja2
import os
import webapp2
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class BlogPost(ndb.Model):
    db_title = ndb.StringProperty(required=True)
    db_entry = ndb.StringProperty(required=True)

class BlogPostSaver(webapp2.RequestHandler):
    def post(self):

        title = self.request.get('title_in_request')
        entry = self.request.get('entry_in_request')

        db_blog_post = BlogPost(db_title=title, db_entry=entry)

        db_blog_post.put()

        template = JINJA_ENVIRONMENT.get_template('thanks.html')
        self.response.write(template.render())

class BlogPostViewer(webapp2.RequestHandler):
    def get(self):
        
        blog_query = BlogPost.query()

        blog_data = blog_query.fetch()
        template = JINJA_ENVIRONMENT.get_template('viewer.html')

        self.response.write(template.render({'entries' : blog_data}))

class BlogPostCreator(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('creator.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', BlogPostCreator),
    ('/save', BlogPostSaver),
    ('/view', BlogPostViewer)
], debug=True)
