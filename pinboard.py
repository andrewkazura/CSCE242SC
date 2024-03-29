'''
Created on Sep 2, 2012

@author: Andrew
'''

import webapp2
import jinja2
import os
import logging #for debugging.
import json
from google.appengine.api import users
from google.appengine.ext import db
import urllib2
from google.appengine.api import urlfetch
from google.appengine.api import images

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class Pin(db.Model):
    imgUrl = db.StringProperty(multiline=True)
    caption = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    owner = db.UserProperty()
    pinprivate = db.StringProperty()
    picture = db.BlobProperty(default=None)
    width = db.StringProperty()
    height = db.StringProperty()
    comments = db.StringListProperty(default=[])
    

class Board(db.Model):
    name = db.StringProperty()
    owner = db.UserProperty()
    boardprivate = db.StringProperty()
    tags = db.StringListProperty()
    xCoor = db.ListProperty(int)
    yCoor = db.ListProperty(int)
    


    

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
        imgUrl = self.request.get('imgUrl')
        
        self.pin = Pin(imgUrl=self.request.get('imgUrl'),
                       caption=self.request.get('caption'),
                       owner=user,
                       picture = db.Blob(urlfetch.Fetch(imgUrl).content))
        img = images.Image(self.pin.picture)
        self.pin.height = str(img.height)
        self.pin.width = str(img.width)
        
        self.pin.put()
        
        
        self.redirect('/pin/'+ str(self.pin.key().id()))
        
        
  
        
class PinHandler(webapp2.RequestHandler):
    def get(self,id):
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)  
        
        templateValues = {'imgUrl': self.pin.imgUrl,
                          'caption': self.pin.caption,
                          'owner': self.pin.owner,
                          'date': self.pin.date,
                          'id': str(self.pin.key().id()),
                          'pinprivate': self.pin.pinprivate,
                          'delete': True,
                          'comments': self.pin.comments
                          }
        templateValues['title'] = 'Pin ' + str(self.pin.key().id())
        templateValues['date'] = str(templateValues['date'])[0:16]
        
        user = users.get_current_user()
        if user:
            templateValues['logout'] = users.create_logout_url('/')
            templateValues['username'] = user.nickname()
        else:
            templateValues['login'] = users.create_login_url('/')
            
        templateValues['boards'] = Board.all()
        
        if self.request.get('fmt') == 'json':
            self.response.out.headers['Content-Type'] = 'text/json'
            data = {'key': self.pin.key().id(), 'imgUrl': self.pin.imgUrl, 'caption': self.pin.caption}
            self.response.out.write(json.dumps(data))
            return
          
            template = jinja_environment.get_template('jsonmainpics.html')
            self.response.out.write(template.render(templateValues))  
            return        
       
        template = jinja_environment.get_template('mainpics.html')
        self.response.out.write(template.render(templateValues))
        
 
        
    def post(self, id):
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)
        if self.request.get('caption') != "":
            self.pin.caption=self.request.get('caption')
        if self.request.get('addcomment') != "":
            self.pin.comments.append(self.request.get('addcomment'))
        self.pin.pinprivate = self.request.get('pinprivate')
        self.pin.save()
       


            
            
class AllPinHandler(webapp2.RequestHandler):
    def get(self):
        templateValues = {}
        templateValues['title'] = 'Your Pins'
        templateValues['pins'] = Pin.all()
        
        user = users.get_current_user()
        if user:
            templateValues['logout'] = users.create_logout_url('/')
            templateValues['username'] = user
        else:
            templateValues['login'] = users.create_login_url('/')
            
        template = jinja_environment.get_template('mainallpics.html')                         
        
        if self.request.get('fmt') == 'json':
            self.response.out.headers['Content-Type'] = 'text/json'
            jdata = []
            for pin in Pin.all():
                data = {'key': pin.key().id(), 'imgUrl': pin.imgUrl, 'caption': pin.caption}
                jdata.append(data)
            self.response.out.write(json.dumps(jdata))
            
            return
            template = jinja_environment.get_template('mainjsonallpics.html')
            self.response.out.write(template.render(templateValues))
            return
 
           
 
        self.response.out.write(template.render(templateValues))


class DeletePin(webapp2.RequestHandler):
    def get(self, id):
        pass
    
    def post(self, id):
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)
        self.pin.delete()
        self.redirect('/')
        
class DeleteBoard(webapp2.RequestHandler):
    def get(self, id):
        pass
    
    def post(self, id):
        self.key = db.Key.from_path('Board', long(id))
        self.board = db.get(self.key)
        self.board.delete()
        self.redirect('/')
        
        
class AllBoardHandler(webapp2.RequestHandler):
    def get(self):
        templateValues = {}
        user = users.get_current_user()
        templateValues['username'] = user
        templateValues['boards'] = Board.all()
        templateValues['title'] = "All Boards"

           
        template = jinja_environment.get_template('allboards.html')
        self.response.out.write(template.render(templateValues))

    def post(self):
        user = users.get_current_user()
        self.board = Board(name = self.request.get('name'), owner = user)
        self.board.put()
        
        
        self.redirect('/board')       


class BoardHandler(webapp2.RequestHandler):
    def get(self,id):
        self.templateValues = {}
        self.user = users.get_current_user()
        
        self.templateValues['pins'] = Pin.all()
        
        self.key = db.Key.from_path('Board', long(id))
        self.board = db.get(self.key)
        
        self.templateValues['title'] = self.board.name
        self.templateValues['owner'] = self.board.owner
        self.templateValues['boardprivate'] = self.board.boardprivate
        self.templateValues['id'] = self.board.key().id()
        self.templateValues['tags'] = self.board.tags
        self.templateValues['xCoor'] = self.board.xCoor
        self.templateValues['yCoor'] = self.board.yCoor
        
        
        if self.request.get('fmt') == 'json':
            data = {}
            data['pinboard'] = self.templateValues['tags']
            for pin in Pin.all():
                data[pin.key().id()] = (pin.imgUrl, pin.caption, pin.key().id())
            data['boardID'] = self.board.key().id()
            data['boardprivate'] = self.board.boardprivate
            
            self.response.out.headers['Content-Type']='text/json'
            self.response.out.write(json.dumps(data))
            return
            
        template = jinja_environment.get_template('board.html')
        
        if self.request.get('fmt') != 'json':
            self.response.out.write(template.render(self.templateValues))

    
    def post(self,id):
        self.key = db.Key.from_path('Board', long(id))
        self.board = db.get(self.key)
        if self.request.get('name') != "":
            self.board.name = self.request.get('name')
        self.board.boardprivate = self.request.get('boardprivate') 
        
        if self.request.get('addpin') != "":
            self.board.tags.append(self.request.get('addpin'))
            
        if self.request.get('deletepin') != "":
            self.board.tags.remove(str(self.request.get('deletepin')))
            
        self.request.xCoor.append(['addpin'])
        self.request.yCoor.append(['addpin'])
        
        self.board.save()

        
        
class CanvasHandler(webapp2.RequestHandler):
    def get(self,id):
        self.templateValues = {}
        self.user = users.get_current_user()
        
        self.templateValues['pins'] = Pin.all()
        
        self.key = db.Key.from_path('Board', long(id))
        self.board = db.get(self.key)
        
        self.templateValues['title'] = self.board.name
        self.templateValues['owner'] = self.board.owner
        self.templateValues['boardprivate'] = self.board.boardprivate
        self.templateValues['id'] = self.board.key().id()
        self.templateValues['tags'] = self.board.tags
        self.templateValues['xCoor'] = self.board.xCoor
        self.templateValues['yCoor'] = self.board.yCoor
        
        
        
        if self.request.get('fmt') == 'json':
            data = {}
            data['pinboard'] = self.templateValues['tags']
            for pin in Pin.all():
                data[pin.key().id()] = (pin.imgUrl, pin.caption, pin.key().id(), 0, 0)
            data['boardID'] = self.board.key().id()
            data['boardprivate'] = self.board.boardprivate
            
            self.response.out.headers['Content-Type']='text/json'
            self.response.out.write(json.dumps(data))
            return
            
        template = jinja_environment.get_template('canvas.html')
        
        if self.request.get('fmt') != 'json':
            self.response.out.write(template.render(self.templateValues))

    
    def post(self,id):
        self.key = db.Key.from_path('Board', long(id))
        self.board = db.get(self.key)
        if self.request.get('name') != "":
            self.board.name = self.request.get('name')
        self.board.boardprivate = self.request.get('boardprivate')
        x = self.request.get('x')
        y = self.request.get('y')
        logging.info("=%s=" % x)
        self.board.xCoor[int(self.request.get('editPinId'))] = int(x)
        self.board.yCoor[int(self.request.get('editPinId'))] = int(y)

        self.board.save()

class ImgHandler(webapp2.RequestHandler):
    def get(self,id):
        self.templateValues = {}
        self.user = users.get_current_user()
        self.key = db.Key.from_path('Pin', long(id))
        self.pin = db.get(self.key)
        self.response.headers['Content-Type'] = 'image/jpg'
        self.response.out.write(self.pin.picture)
        return


app = webapp2.WSGIApplication([('/', MainPage),('/pin/(.*).jpg', ImgHandler),('/pin/(.*)', PinHandler),
                               ('/hell/(.*)',DeletePin),('/board/(.*)',BoardHandler),
                               ('/board', AllBoardHandler),('/hell2/(.*)',DeleteBoard),
                               ('/canvas/(.*)', CanvasHandler), ('/pin', AllPinHandler)],
                              debug=True)
