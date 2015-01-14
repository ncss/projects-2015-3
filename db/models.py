import sqlite3, time, hashlib, math
from .connection import conn, cursor
  
def get_new_id(table_name):
  # returns next id for the table specified as 'table_name'
  cursor.execute("SELECT MAX(id) FROM " + table_name + ";")
  max_id = cursor.fetchone()
  max_id = max_id[0]
  if max_id is None:
    return 0
  return int(max_id) + 1


class Model:

  @classmethod
  def delete(cls, id):
    cursor.execute("DELETE FROM " + cls.lower() + " WHERE id = ?;", (id,));
    conn.commit()


class Comment(Model):
  def __init__(self, id, user_id, video_id, content, created, timestamp):
    self.id = id
    self.user_id = user_id
    self.video_id = video_id
    self.content = content
    self.created = created
    self.timestamp = timestamp
  
  def update(self): #updates comment contents
    cursor.execute("""UPDATE comment SET content = ? WHERE id = ?;""", (self.content, self.id,))
    conn.commit()
   
  @classmethod
  def create(cls, user_id, video_id, content, timestamp):
    created = time.time()
    id = get_new_id('comment')
    cursor.execute("""INSERT INTO comment VALUES (?, ?, ?, ?, ?, ?);""", (id, user_id, video_id, content, created, timestamp,))
    conn.commit()
    return cls(id, user_id, video_id, content, created, timestamp)
  
  @classmethod
  def find(cls, id):
    cursor.execute("""SELECT * FROM comment WHERE id = ?;""", (id,))
    row = cursor.fetchone()
    if row is not None:
      return cls(id, row[1], row[2], row[3], row[4], row[5])
    return None
  
  @classmethod
  def find_by_video(cls, video_id):
    cursor.execute("""SELECT * FROM comment WHERE video_id = ?;""", (video_id,))
    rows = cursor.fetchall()
    comments = []
    for comment in rows:
      comments.append(cls(*comment[:6]))
    return comments
    
  @classmethod
  def get_comments_list(cls, video_id):
    cursor.execute("""SELECT u.display_name, c.created, c.content, c.timestamp 
                      FROM user u
                      JOIN comment c ON u.id = c.user_id
                      WHERE video_id = ?
                      ORDER BY c.timestamp DESC, c.created DESC;""", (video_id,))
    rows = cursor.fetchall()
    return rows              

class View(Model):
  def __init__(self, id, video_id, user_id, created, elapsed, last_updated):
    self.id = id
    self.video_id = video_id
    self.user_id = user_id
    self.created = created
    self.elapsed = elapsed
    self.last_updated = last_updated
  
  def update(self):
    cursor.execute("""UPDATE view SET video_id = ?, user_id = ?, elapsed = ?, last_updated = ? WHERE id = ?""", (self.video_id, self.user_id, self.elapsed, time.time(), self.id,))
    conn.commit()
  
  @classmethod  
  def create(cls, video_id, user_id):
    id = get_new_id('view')
    created = time.time()
    cursor.execute("""INSERT INTO view VALUES (?, ?, ?, ?, ?, ?)""", (id, video_id, user_id, created, 0, created,))
    conn.commit()
    return cls(id, video_id, user_id, created, 0, created)
    
  @classmethod
  def find(cls, id):
    cursor.execute("""SELECT * FROM view WHERE id = ?""", (id,))
    row = cursor.fetchone()
    if row is not None:
        return cls(id, row[1], row[2], row[3], row[4], row[5])
    return None
	
  @classmethod
  def find_by_video_id(cls, video_id):
    cursor.execute("""SELECT * FROM view WHERE video_id = ?""", (video_id,))
    row = cursor.fetchone()
    if row is not None:
        return cls(id, row[1], row[2], row[3], row[4], row[5])
    return None
  
  @classmethod
  def most_recent(cls, attr=None, value=None):
    # returns most recent view

    # attr : user_id, video_id. 
    # default (None) gets most recent by date created
    if attr and value:
      cursor.execute("SELECT * FROM view WHERE " + attr + " = ? ORDER BY created DESC LIMIT 1;", (value,))
    else:
      cursor.execute("SELECT * FROM view ORDER BY created DESC")
    row = cursor.fetchone()
    if row is not None:
      return cls(row[0], row[1], row[2], row[3], row[4], row[5])
    return None

  @classmethod
  def all_views(cls, attr=None, value=None):
    # returns list of views 

    # attr : user_id, video_id. 
    # default (None) gets most recent by date created
    if attr and value:
      cursor.execute("SELECT * FROM view WHERE " + attr + " = ? ORDER BY created DESC", (value,))
    else:
       cursor.execute("SELECT * FROM view ORDER BY created DESC")
    rows = cursor.fetchall()
    view_list = []
    for row in rows:
       if row is not None:
          view_list.append(cls(row[0], row[1], row[2], row[3], row[4], row[5]))
    return view_list
  
  

class Video(Model):
  def __init__(self, id, link):
    self.id = id # unique ID for each video
    self.link = link # youtube id of video

  @classmethod
  def create(cls, link):
    id = get_new_id('video')
    cursor.execute("INSERT INTO video VALUES (?, ?);", (id, link))
    conn.commit()
    return cls(id, link)
  
  

  @classmethod
  def get_link(cls, ID):
    cursor.execute("SELECT link FROM video WHERE id = ?;", (ID,))
    #Returning a tuple with (link,None)
    #Requires [0] to prevent javascript errors
    row = cursor.fetchone()
    if row is not None:
      return row[0]
    return None
  
  @classmethod
  def find(cls, id):
    cursor.execute("""SELECT * FROM video WHERE id = ?""", (id,))
    row = cursor.fetchone()
    if row is not None:
        return cls(id, row[1])
    return None
    
  @classmethod
  def find_by_link(cls, link):
    cursor.execute("""SELECT * FROM video WHERE link = ?""", (link,))
    row = cursor.fetchone()
    if row is not None:
        return cls(row[0], row[1])
    return None
  

    


class User(Model):
  def __init__(self, id, email, password, name, created, birthday=None, gender=None, bio=None, pic=None):
    self.id = id
    self.name = name
    self.email = email
    self.birthday = birthday # format should be YYYY-MM-DD
    self.gender = gender
    self.password = password
    self.pic = pic
    self.created = created
    self.bio = bio

  def update():
    cursor.execute("UPDATE user SET user.email = ?, user.password = ?, user.display_name = ?, user.birthday = ?, user.gender = ?, user.profile_photo = ? WHERE user.id = ?;", (self.email, self.password, self.name, self.birthday, self.gender, self.pic, self.id))
    conn.commit()

  def get_age(self): # returns formatted birthday
    birthday = self.birthday
    now = time.time()
    birthday_time_object = time.strptime(birthday, "%Y-%m-%d")
    dif_secs = now - time.mktime(birthday_time_object)
    age = int(dif_secs/3600/24/365)
    return age

  @classmethod
  def create(cls, email, password, name, birthday=None, gender=None):
    id = get_new_id('user')
    # hash password sha256
    hash = User.get_hash(password)
    created = time.time()
    cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (id, email, hash, name, created, birthday, gender, None, None))
    # User table has variables: id email password display_name created birthday gender biography profile_photo
    conn.commit()
    return cls(id, email, hash, name, created, birthday, gender)

  @classmethod
  def find_by_email(cls, email):
    cursor.execute("SELECT * FROM user WHERE user.email = ?;", (email,))
    row = cursor.fetchone()
    if row is None:
      return None
    return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

  @classmethod
  def find(cls, id):
    cursor.execute("SELECT * FROM user WHERE user.id = ?;", (id,))
    row = cursor.fetchone()
    if row is None:
      return None      
    return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

  @classmethod
  def user_by_attribute(cls, attribute, var):
    ### change to return a list?
    cursor.execute("SELECT * FROM user WHERE " + attribute + " = ?;", (var,))
    row = cursor.fetchone()
    if row is None:
      return None
    return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
  
  @classmethod
  def authenticate(cls, email, password):
    cursor.execute("SELECT * FROM user WHERE email = ?;", (email,))
    row = cursor.fetchone()
    if row is None:
      return None
    if User.get_hash(password) == row[2]:
      return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    return None

  @classmethod
  def get_hash(cls, password):
     return hashlib.sha256(password.encode('utf-8')).hexdigest()
     
  def get_favourites(self):
    cursor.execute("""SELECT video_id FROM favourite WHERE user_id = ?""", (self.id,))
    rows = cursor.fetchall()
    fav_list = []
    for row in rows:
       if row is not None:
          fav_list.append(row[0])
    return fav_list

  
class Favourite(Model):
  def __init__(self, id, video_id, user_id):
    self.id = id
    self.video_id = video_id 
    self.user_id = user_id
  
  @classmethod
  def check_existing(cls, video_id, user_id):
    cursor.execute("""SELECT video_id FROM favourite WHERE user_id = ? AND video_id = ?;""", (user_id, video_id))
    if cursor.fetchone():
      return True
    return False

  @classmethod
  def find_popular(cls, limit):
    cursor.execute("""SELECT id, video_id, user_id, COUNT(video_id) AS count 
                      FROM favourite 
                      GROUP BY video_id
                      ORDER BY count DESC 
                      LIMIT ?;""", (limit,) )
    rows = cursor.fetchall()
    if len(rows) > 0:
      favourites = [cls(i[0], i[1], i[2]) for i in rows]
      return favourites
      # returns favourites tuple with attributes id, video_id, user_id NOT a Favourites object
    return None
  
  @classmethod  
  def create(cls, video_id, user_id):
    id = get_new_id('favourite')
    cursor.execute("""INSERT INTO favourite VALUES (?, ?, ?);""", (id, video_id, user_id))
    conn.commit()
    return cls(id, video_id, user_id)


class Friend(Model):
  def __init__(self, id, friends):
    self.id = id
    #self.user = user
    self.friends = friends

  @classmethod
  def create(cls,user_a,user_b):
    id = get_new_id("friend")
    cursor.execute("INSERT INTO friend VALUES (?, ?, ?);", (id, user_a, user_b))
    conn.commit()

  def update(self,id,user_a,user_b):
    cursor.execute("UPDATE friend SET friend.user_a = ?, friend.user_b = ? WHERE friend.id = ?;", (self.id, self.user_a, self.user_b))
    conn.commit()

  @classmethod
  def find_by_id(cls,id):
    cursor.execute("SELECT user_a, user_b FROM friend WHERE user_a = ? OR user_b = ?", (id,id))
    row = cursor.fetchall()
    temp = []
    for friend in row:
        if friend[0] == id:
          temp.append(friend[0])
        else:
          temp.append(friend[1])
    return cls(id,temp)
