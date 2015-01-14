from tornado.ncss import Server
from db.models import User
from db.models import View
from db.models import Comment
from db.models import Video
from db.models import Favourite
from db.models import Friend
from template import render
from tornado import websocket
import time
import datetime
import json
import re


USER_ID_COOKIE = "userid"

def login_required(fn):
    def newfn(response, *args):
        user = is_logged_in(response)
        if not user:
            response.redirect('/login')
        else:
            response.user = user
            fn(response, *args)
    return newfn

def grab_user(fn):
    def newfn(response, *args):
        user = is_logged_in(response)
        response.user = user 
        fn(response, *args)
    return newfn

@grab_user
def index_handler(response):
    recent_views = View.all_views()

    popular_views = Favourite.find_popular(6) # call function to get vids with most favs
    # friend_views = [] # get vids from friends

    def video_link(views):
        video_id_li = []
        links = []
        if views is not None:
            #Only display 6 videos on the main page
            if len(views) > 6:
                views = views[:6]
            for i in views:
                video_id = i.video_id
                video_id_li.append(video_id)
                links.append(Video.get_link(video_id))
        return (links, video_id_li)

    recent_view_tup = video_link(recent_views)
    popular_view_tup = video_link(popular_views)
    # friend_view_tup = video_link(friend_views)

    recent_links, recent_id = recent_view_tup[0], recent_view_tup[1]
    popular_links, popular_id = popular_view_tup[0], popular_view_tup[1]
    # friend_links, friend_id = friend_view_tup[0], friend_view_tup[1]

    response.write(render('templates/index.html',{
        'popular_links': popular_links, 'popular_id': popular_id, 
        #'friend_links': friend_links, 'friend_id' : friend_id, 
        'links' : recent_links, 'video_id_li' : recent_id }, response))

@login_required
def video_handler(response, view_id):
    view = View.find_by_video_id(view_id)
    print(view_id)
    if view is not None:
        comments_list = Comment.get_comments_list(view.video_id)
        comments = []
        for i, comment in enumerate(comments_list):
            d = {"display_name": comment[0],
                 "created": datetime.datetime.fromtimestamp(comment[1]).strftime('%Y-%m-%d %H:%M:%S'),
                 "content": comment[2],
                 "timestamp": comment[3],
                 "counter": i}
            comments.append(d)

        video = Video.find(view.video_id)
        if video is not None:
            response.write(render('templates/video.html',{'youtube_link':video.link, 'comments' : comments, 'video_id': video.id, 'favourited':Favourite.check_existing(video.id, response.user.id)}, response))

@login_required
def favourites_handler(response):
    video_id = response.get_field("video_id")
    profile_id = response.get_field("profile_id")
    if not Favourite.check_existing(video_id, profile_id):
        Favourite.create(video_id, profile_id)

@login_required
def edit_profile_handler(response, profile_id=None):
    print(profile_id)
    user = User.find(profile_id)
    friends = [User.find(x) for x in Friend.find_by_id(profile_id).friends]
    #print(friends.friends)
    if user != None:
        views = View.all_views('user_id', profile_id)
        links = []
        ids = []
        for i in views:
            links.append(Video.get_link(i.video_id))
            ids.append(i.video_id)
        biography = user.bio
        favourite_ids = user.get_favourites()
        favourite_links = [Video.get_link(i) for i in favourite_ids]
        response.write(render("templates/edit_profile.html", {'links': links, 'user': user, 'ids': ids, 'biography': biography, "friends": friends,  'favourite_links': favourite_links, 'favourite_ids': favourite_ids}, response))
    else:
        response.redirect('/profile/' + str(response.user.id))

@grab_user
def view_profile_handler(response, profile_id=None):
    user = User.find(profile_id)
    friends = [User.find(x) for x in Friend.find_by_id(profile_id).friends]
    #print(friends.friends)
    if user != None:
        views = View.all_views('user_id', profile_id)
        links = []
        ids = []
        for i in views:
            links.append(Video.get_link(i.video_id))
            ids.append(i.video_id)
        biography = user.bio
        favourite_ids = user.get_favourites()
        favourite_links = [Video.get_link(i) for i in favourite_ids]
        response.write(render("templates/profile.html", {'links': links, 'user': user, 'ids': ids, 'biography': biography, "friends": friends,  'favourite_links': favourite_links, 'favourite_ids': favourite_ids}, response))
    else:
        if response.user:
            if response.user.id != None:
                response.redirect("/profile/"+str(response.user.id))
        response.redirect("error")

@login_required
def add_friend_handler(response, profile_id):
	try:
		if int(profile_id) not in Friend.find_by_id(response.user.id).friends:
			Friend.create(response.user.id, profile_id)
			response.redirect("/profile/"+str(response.user.id))
		else:
			response.redirect("/profile/"+str(response.user.id))
	except:
		response.redirect("error")

def search_handler(response):
    response.write(render('templates/search.html',{}, response))

@grab_user
def login_handler(response):
  if response.user:
        response.redirect('/')
  email = response.get_field("email")
  password = response.get_field("password")
  message = ""
  if email is not None and password is not None:
    u = User.authenticate(email, password)
    if u is None:
      #Login Failed
      message = "Invalid credentials."
      response.write(render('templates/login.html', {"message" : message}, response))
    else:
      #Login Successful
      response.set_secure_cookie(USER_ID_COOKIE,str(u.id))
      #Redirect the user to index
      response.redirect('/')
  else:
    response.write(render('templates/login.html', {"message" : message}, response))

@login_required 
def logout_handler(response):
	login_check = is_logged_in(response)
	if login_check is not None:
		response.clear_cookie(USER_ID_COOKIE)
	response.redirect('/')

def style_guide_handler(response):
    template = open("templates/style_guide.html")
    response.write(template.read())

@grab_user
def register_handler(response):
    if response.user:
        response.redirect('/')
    if response.get_field('email') is None:
        return response.write(render('templates/register.html',{'valid': True, 'message': ''}, response))
    else:
        reqfields = ['email', 'password', 'display_name']
        opfields = ['birthday', 'gender']
        fields = {}
        valid = True
        for field in (reqfields + opfields):
            fields[field] = response.get_field(field)
            
        for field in opfields:
            if fields[field] == '':
                fields[field] = None

        for field in reqfields: # check for empty required fields
            if fields[field] == '':
                valid = False
                message = 'Required field \'' + field + '\' is empty.'
                break

        if fields['birthday'] is not None:
            if not re.match(r'\d\d\d\d-\d\d-\d\d', fields['birthday']):
                valid = False
                message = 'Invalid date in birthday field'
            else:
                now = time.time()
                birthday_time_object = time.strptime(fields['birthday'], "%Y-%m-%d")
                if time.mktime(birthday_time_object) > now:
                    valid = False
                    message = 'Birthday may not be in future'
        
        if User.user_by_attribute('display_name', fields['display_name']): # checks for intersecting display names
            valid = False
            message = 'Display name already taken'
        if User.find_by_email(fields['email']) is not None: # checks for intersecting emails
            valid = False
            message = 'This email is already linked to an account, <a href="/login">login</a>?'

        if fields['display_name'] == 'James': fields['display_name'] = 'Jimmy Murran'

        if not valid:
            response.write(render('templates/register.html',{'valid': False, 'message': message, 'email': fields['email'], 'display_name': fields['display_name'], 'birthday': fields['birthday']}, response))
        else:
            u = User.create(
                fields['email'],
                fields['password'],
                fields['display_name'],
                fields['birthday'],
                fields['gender']
                )
            response.set_secure_cookie(USER_ID_COOKIE,str(u.id))
            response.redirect('/profile/' + str(u.id))
	
def is_logged_in(response):
	user_id = response.get_secure_cookie(USER_ID_COOKIE)
	try:
		user_id = int(user_id)
	except (TypeError, ValueError):
		return None
	else:
		u = User.find(user_id)
		if u is None:
			return None
		else:
			return u
	
def start_view(response, youtube_link):
    u = is_logged_in(response)
    if u is not None:
        youtube_video = Video.find_by_link(youtube_link)
        if youtube_video is None:
            youtube_video = Video.create(youtube_link)
        view = View.create(youtube_video.id,u.id)
        response.redirect('/video/'+str(view.id))
    
def pulse(response,view_id,time):
    u = is_logged_in(response)
    if u is not None:
        v = View.find(int(view_id))
        if u.id == v.user_id:
            v.elapsed = float(time)
            v.update()
            response.write('{"status" : "ok"}')
        else:
            response.write('{{"last_updated" : {0}, "elapsed" : {1}, "status" : "client"}}'.format(v.last_updated, v.elapsed))

class CommentWebSocket(websocket.WebSocketHandler):
    connections = set()
    
    def open(self):
        self.connections.add(self)
        u = is_logged_in(self)
        print("WebSocket opened for: " + str(u.id))

    def on_message(self, message):
        u = is_logged_in(self)
        extra_information = {'time' : time.time(), 'user_name' : u.name}
        j = json.loads(message)
        j.update(extra_information)
        if u is not None:
            Comment.create(u.id, j['video_id'], str(j['comment']),j['timestamp'])
            for client in self.connections:
                client.write_message(j)

    def on_close(self):
        print("WebSocket closed")
            
@login_required    
def search_video_handler(response):
    q = response.get_field("q")
    if q is None:
        q = ""
    response.write(render("templates/search_videos.html", {"q":q}, response))
                

def not_found_handler(response):
  response.set_status(404)
  response.write(render('templates/404_page.html',{}, response))

@grab_user
def about_handler(response):
  response.write(render('templates/about.html',{}, response))
  

server = Server()
server.register("/", index_handler)
server.register(r"/video/(\d+)", video_handler)
server.register("/style_guide", style_guide_handler)
server.register("/profile", view_profile_handler)
server.register(r"/profile/(\d+)", view_profile_handler)
server.register(r"/profile/add/(\d+)", add_friend_handler)
server.register("/profile/edit/(\d+)", edit_profile_handler)
server.register("/search", search_handler)
server.register("/search_video", search_video_handler)
server.register("/login", login_handler)
server.register("/logout", logout_handler)
server.register("/register", register_handler)
server.register(r"/pulse/(.*)/(.*)", pulse)
server.register(r"/view/(.*)", start_view)
server.register(r"/comment/new", CommentWebSocket)
server.register(r"/about", about_handler)
server.register(r"/favourites", favourites_handler)
server.register("/.*", not_found_handler)


server.run()
