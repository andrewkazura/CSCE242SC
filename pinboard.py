'''
Created on Sep 2, 2012

@author: Andrew
'''

import webapp2
import jinja2
import os
import logging #for debugging.
from google.appengine.api import users
from google.appengine.ext import db

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class Pin(db.Model):
    imgUrl = db.StringProperty()
    caption = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    owner = db.UserProperty()
    tags = db.StringListProperty()

class Board(db.Model):
    name = db.StringProperty()
    

class MainPage(webapp2.RequestHandler):
    def get(self):
        templateValues = {}
        if self.request.get('imgUrl') != None:
            templateValues['imgUrl'] = self.request.get('imgUrl')
        if self.request.get('caption') != None:
            templateValues['caption'] = self.request.get('caption')
        templateValues['title'] = 'Pinboard'
        user = users.get_current_user()
        if user:
            templateValues['logout'] = users.create_logout_url('/')
            templateValues['username'] = user.nickname()
        else:
            templateValues['login'] = users.create_login_url('/')


           
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(templateValues))
        

    def post(self):

        user = users.get_current_user()
        self.pin = Pin(imgURL=self.request.get('imgUrl'),
                       caption=self.request.get('caption'),
                       owner=user.nickname())
        self.pin.put()
        
        
        self.redirect('/pin/'+ str(self.pin.key().id()))
        
        
  
        
class PinHandler(webapp2.RequestHandler):
    def get(self,id):
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)  
        
        templateValues = {'imgURL': self.pin.imgURL,
                          'caption': self.pin.caption,
                          'owner': self.pin.owner,
                          'date': self.pin.date,
                          'id': str(self.pin.key().id()),
                          'delete': True
                          }
        templateValues['title'] = 'Pin ' + str(self.pin.key().id())
        templateValues['date'] = str(templateValues['date'])[0:16]
        
        user = users.get_current_user()
        if user:
            templateValues['logout'] = users.create_logout_url('/')
            templateValues['username'] = user.nickname()
        else:
            templateValues['login'] = users.create_login_url('/')
       
        template = jinja_environment.get_template('mainpics.html')
        self.response.out.write(template.render(templateValues))
        
 
        
    def post(self, id):
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)
        self.pin.imgURL=self.request.get('imgURL')
        self.pin.caption=self.request.get('caption')
        self.pin.save()
        self.redirect('/pin/'+ str(self.pin.key().id())) 


            
            
class AllPinHandler(webapp2.RequestHandler):
    def get(self):
        templateValues = {}
        templateValues['title'] = 'Your Pins'
        templateValues['pins'] = Pin.all()
        
#        templateValues['owner'] = 'test'
        user = users.get_current_user()
        if user:
            templateValues['logout'] = users.create_logout_url('/')
            templateValues['username'] = user.nickname()
        else:
            templateValues['login'] = users.create_login_url('/')
            

           
        template = jinja_environment.get_template('mainallpics.html')
        self.response.out.write(template.render(templateValues))


class DeletePin(webapp2.RequestHandler):
    def get(self, id):
        pass
    
    def post(self, id):
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)
        self.pin.delete()
        self.redirect('/')
        
        
class AllBoardHandler(webapp2.RequestHandler):
    def get(self):
        templateValues = {}
        self.user = users.get_current_user()
        self.templateValues['boards'] = Board.all()
        self.templateValues['title'] = "All Boards"

           
        template = jinja_environment.get_template('mainallpics.html')
        self.response.out.write(template.render(templateValues))

      


class BoardHandler(webapp2.RequestHandler):
    def get(self,id):
        templateValues = {}
        self.user = users.get_current_user()
        query = Board.all()
        self.templateValues['boards'] = query
        if self.user:
            self.templateValues['title'] = 'My Boards'
            self.render('/board')
        else:
            self.render('/')
            
        template = jinja_environment.get_template('mainpics.html')
        self.response.out.write(template.render(templateValues))

    
    def post(self,id):
        #get the pin
        
        pass


app = webapp2.WSGIApplication([('/', MainPage),('/pin/(.*)', PinHandler),('/pin', AllPinHandler),
                               ('/hell/(.*)',DeletePin),('/board/(.*)',BoardHandler),
                               ('/board', AllBoardHandler),],
                              debug=True)
