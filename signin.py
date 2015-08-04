# from google.appengine.api import users
# import jinja2
# import os
# import webapp2
#
# jinja_environment = jinja2.Environment(loader=
#     jinja2.FileSystemLoader(os.path.dirname(__file__)))
#
# class MyHandler(webapp2.RequestHandler):
#     def get(self):
#         user = users.get_current_user()
#         if user:
#             greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
#                         (user.nickname(), users.create_logout_url('/')))
#         else:
#             greeting = ('<a href="%s">Sign in or register</a>.' %
#                         users.create_login_url('/'))
#         template_vars = {"name": "Nicolas"}
#         template = jinja_environment.get_template('BeginningTimeline.html')
#         self.response.out.write(template.render(template_vars))
# class TimelineHandler(webapp2.RequestHandler):
#     def get(self):
#         template_vars2 = {"SeniorYearSpring": "Senior Year Spring "}
#         template = jinja_environment.get_template('SeniorSpring.html')
#         self.response.out.write(template.render(template_vars2))
#         # self.response.out.write("<html><head><title>Timeline</title><link rel="stylesheet" type="text/css" href="style.css"></head><body><h1>Welcome to your timeline</h1><div id="JYFall">
#         #<a href="JuniorYearFall.html">Junior Year - Fall</a></div><div id="JYSpring"><a href="JuniorYearSpring.html">Junior Year - Spring</a></div id="JYSummer"><div><a href="JuniorYearSummer.html">Junior Year - Summer</a></div><div id="SYFall"><a href="SeniorYearFall.html">Senior Year - Fall</a></div id="SYSpring"><div><a href="SeniorYearSpring.html">Senior Year - Spring</a></div></body></html>")
# app = webapp2.WSGIApplication([
#     ('/', MyHandler),
#     ('/SeniorYearSpring.html', TimelineHandler)
# ], debug=True)
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Make sure to run app like so:
# dev_appserver.py --datastore_consistency_policy=consistent [path_to_app_name]
# in order to see changes reflected in the redirect immediately

# To clear the datastore:
# /usr/local/google_appengine/dev_appserver.py --clear_datastore=1 [path_to_app_name]

import os
import webapp2
import jinja2
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Define a Post model for the Datastore
class Topic(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    comment_keys = ndb.KeyProperty(kind='Comment', repeated=True)

class Comment(ndb.Model):
    author = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    # Your code goes here

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Get all of the student data from the datastore
        query = Topic.query()
        topic_data = query.fetch()
        # Pass the data to the template
        template_values = {
            'topics' : topic_data
        }
        template = JINJA_ENVIRONMENT.get_template('blogposts.html')
        self.response.write(template.render(template_values))

    def post(self):
        # Get the post title and content from the form
        title = self.request.get('title')
        content = self.request.get('content')
        # Create a new Student and put it in the datastore
        topic = Topic(title=title, content=content)
        topic.put()
        # Redirect to the main handler that will render the template
        self.redirect('/')

class CommentHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        comment = self.request.get('comment')
        db_comment = Comment(
            name=name,
            comment=comment
        )
        comment_key = db_comment.put()

        # Create the comment in the Database
        # !!!! YOUR CODE HERE

        # Find the post that was commented on using the hidden post_url_key
        topic_url_key = self.request.get('topic_url_key')
        topic_key = ndb.Key(urlsafe=topic_url_key)
        topic = topic_key.get()

        # Attach the comment to that post
        # !!!! YOUR CODE HERE
        topic.comment_keys.append(comment_key)
        topic.put()

        self.redirect('/')

#         template_vars2 = {"SeniorYearSpring": "Senior Year Spring"}
#         template = jinja_environment.get_template('SeniorSpring.html')
#         self.response.out.write(template.render(template_vars2))
        # self.response.out.write("<html><head><title>Timeline</title><link rel="stylesheet" type="text/css" href="style.css"></head><body><h1>Welcome to your timeline</h1><div id="JYFall">
        #<a href="JuniorYearFall.html">Junior Year - Fall</a></div><div id="JYSpring"><a href="JuniorYearSpring.html">Junior Year - Spring</a></div id="JYSummer"><div><a href="JuniorYearSummer.html">Junior Year - Summer</a></div><div id="SYFall"><a href="SeniorYearFall.html">Senior Year - Fall</a></div id="SYSpring"><div><a href="SeniorYearSpring.html">Senior Year - Spring</a></div></body></html>")

class ScholarshipHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('scholarships.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    # ('/', MyHandler),
    ('/forum', MainHandler),
    ('/comment', CommentHandler),
    # ('/SeniorYearSpring.html', TimelineHandler),
    ('/scholarships', ScholarshipHandler)
], debug=True)
