'''
Created on Sep 2, 2012

@author: Andrew
'''

import webapp2
import jinja2
import os


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
      def get(self):
        template_values = {
                           'url': self.request.get('url'),
                           'caption': self.request.get('caption')
        }

        template = jinja_environment.get_template('master.html')
        self.response.out.write(template.render(template_values))
       
       



app = webapp2.WSGIApplication([('/', MainPage),
                             ],
                              debug=True)