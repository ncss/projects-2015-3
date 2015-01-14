CREATE TABLE user (
  id INT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  display_name TEXT NOT NULL,
  created REAL NOT NULL, --unix time
  birthday TEXT, --'YYYY-MM-DD'
  gender TEXT,
  biography TEXT,
  profile_photo TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE video (
  id INT NOT NULL,
  link TEXT NOT NULL, --'K3p0EFtJIn8'
  PRIMARY KEY (id)
);

CREATE TABLE comment (
  id INT NOT NULL,
  user_id INT NOT NULL,
  video_id INT NOT NULL,
  content TEXT NOT NULL,
  created REAL NOT NULL, --unix time
  timestamp REAL NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE view (
  id INT NOT NULL,
  video_id INT NOT NULL,
  user_id INT NOT NULL,
  created REAL NOT NULL, --unix time
  elapsed REAL NOT NULL,
  last_updated REAL NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE favourite (
  id INT NOT NULL,
  video_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE friend (
  id INT NOT NULL,
  user_a INT NOT NULL,
  user_b INT NOT NULL,
  PRIMARY KEY (id)
);
