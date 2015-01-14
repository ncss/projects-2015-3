from tornado.ncss import Server
from template import render

class person:
	gender = 0
	friends = []

	def __init__(self, name, gender=1):
		self.name = name
		self.gender = gender
	
	def friend(self, friend):
		self.friends.append(friend)

jim = person("Jim & bob")
bob = person("Bob")
jill = person("Jill",0)
tom = person("Tom")
james = person("James",0)
bob_derp = person("Bob Derp",2)

jim.friend(bob)
jim.friend(jill)
jim.friend(tom)
jim.friend(james)
jim.friend(bob_derp)

def index_handler(context):
	context.write(render("example.html", {"jim": jim, "site_title": "CineMeow", "unsafe": "<a href=#>login</a>", "safe": "<a href=#>login</a>"}))

server = Server()
server.register("/", index_handler)
server.run()
