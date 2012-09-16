'''
Created on Sep 2, 2012

@author: Andrew
'''

import webapp2
import jinja2
import os


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
      
      def get(self):
        template_values = {
                           'user': users.get_current_user(),
                           'url': self.request.get('url'),
                           'caption': self.request.get('caption')  
        }
        
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/"))

        self.response.out.write("<html><header>%s</header></html>" % greeting)
  
        template = jinja_environment.get_template('master.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage),
                             ],
                              debug=True)