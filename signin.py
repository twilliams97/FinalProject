from google.appengine.api import users
import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
        template_vars = {"name": "Nicolas"}
        template = jinja_environment.get_template('BeginningTimeline.html')
        self.response.out.write(template.render(template_vars))
class TimelineHandler(webapp2.RequestHandler):
    def get(self):
        template_vars2 = {"SeniorYearSpring": "Senior Year Spring"}
        template = jinja_environment.get_template('SeniorSpring.html')
        self.response.out.write(template.render(template_vars2))
        # self.response.out.write("<html><head><title>Timeline</title><link rel="stylesheet" type="text/css" href="style.css"></head><body><h1>Welcome to your timeline</h1><div id="JYFall">
        #<a href="JuniorYearFall.html">Junior Year - Fall</a></div><div id="JYSpring"><a href="JuniorYearSpring.html">Junior Year - Spring</a></div id="JYSummer"><div><a href="JuniorYearSummer.html">Junior Year - Summer</a></div><div id="SYFall"><a href="SeniorYearFall.html">Senior Year - Fall</a></div id="SYSpring"><div><a href="SeniorYearSpring.html">Senior Year - Spring</a></div></body></html>")
app = webapp2.WSGIApplication([
    ('/', MyHandler),
    ('/SeniorYearSpring.html', TimelineHandler)
], debug=True)
