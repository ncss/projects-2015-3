INSERT INTO user VALUES (0,            'me@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',     'cool_guy', 1420867500,         NULL,  'F',           NULL, '/static/images/profiles/cat1.jpg'); -- 'password'
INSERT INTO user VALUES (1,           'you@example.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',    'ilovecats', 1420866500, "1997-08-28",  'M',          'I l', '/static/images/profiles/cat2.jpg'); -- '1234'
INSERT INTO user VALUES (2,               'foo@bar.com', '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5',    'ihatecats', 1420865500, "1998-04-30", NULL, 'I am so cool',      NULL); -- 'qwerty'
INSERT INTO user VALUES (3,          'okdude@gmail.com', '1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032',    'ilovedogs', 1420857500,         NULL,  'F',     'I o cool', '/static/images/profiles/cat3.jpg'); -- 'letmein'
INSERT INTO user VALUES (4,         'spencer@gmail.com', '1eff0838ca36ddf92554b3b17ed22f72efceac557d7dadd2196d1e3ef84a6a58', 'Marc_is_cool', 1420855500, "1978-01-21",  'O', 'I am so cool',      NULL); -- 'cinemeow'
INSERT INTO user VALUES (5,            'asdf@gmail.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c',     'Specie13', 1420837500, "1990-05-12",  'M',     'I o cool', '/static/images/profiles/cat4.jpg'); -- '1111'
INSERT INTO user VALUES (6, 'ilovecinemeow@outlook.com', '6a158d9847a80e99511b2a7866233e404b305fdb7c953a30deb65300a57a0655',       'Ziiita', 1420861500, "1998-11-02",  'F',       'foobar', '/static/images/profiles/cat5.jpg'); -- 'pa$$word'
INSERT INTO user VALUES (7,         'kitty@outlook.com', '108c1be06d161f8df747fe656a6b157d3500723bc8ec5a153a8e8af2c8d9f301',   'uncool_guy', 1420862500,         NULL, NULL,     'I am so ', '/static/images/profiles/cat1.jpg'); -- 'thisisapass'
INSERT INTO user VALUES (8,             'her@gmail.com', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090',          'LOL', 1420864500, "1955-01-14",  'O',           NULL,      NULL); -- 'abc123'
INSERT INTO user VALUES (9,             'him@gmail.com', '89e01536ac207279409d4de1e5253e01f4a1769e696db0d6062ca9b8f56767c8',     'HAHAROFL', 1420865200, "2000-12-29",  'F',           NULL, '/static/images/profiles/cat3.jpg'); -- 'mypassword'

INSERT INTO video VALUES (0, 'cbP2N1BQdYc');
INSERT INTO video VALUES (1, 'Qrl0E1kwhSg');
INSERT INTO video VALUES (2, '0IvGAvo7nDE');
INSERT INTO video VALUES (3, 'brlaQPXzFTA');
INSERT INTO video VALUES (4, 'gU2ZPcS-bAk');
INSERT INTO video VALUES (5, '4tzhyfWHdLo');
INSERT INTO video VALUES (6, 'L0MK7qz13bU');
INSERT INTO video VALUES (7, '5MgBikgcWnY');
INSERT INTO video VALUES (8, 'ds8chrP62Os');
INSERT INTO video VALUES (9, 'Q8TXgCzxEnw');

INSERT INTO comment VALUES (0, 6, 1,                            'LOL', 1420867595, 21);
INSERT INTO comment VALUES (1, 3, 1,                             ':)', 1420867500, 30);
INSERT INTO comment VALUES (2, 0, 2,                            'omg', 1420867500, 50);
INSERT INTO comment VALUES (3, 2, 4,                     'dramatique', 1420866053, 21);
INSERT INTO comment VALUES (4, 5, 0,            '; DROP TABLE video;', 1420865153, 21);
INSERT INTO comment VALUES (5, 8, 3,              'asdskldjasljdsajl', 1420865123, 21);
INSERT INTO comment VALUES (6, 1, 5, '<script>alert("xss");</script>', 1420856153, 21);
INSERT INTO comment VALUES (7, 4, 9,          'everything is awesome', 1420867153, 21);
INSERT INTO comment VALUES (8, 7, 8,                 'asdasdasdasdas', 1420864130, 21);
INSERT INTO comment VALUES (9, 9, 7,                 'asdasdasdasdas', 1420864130, 21);

INSERT INTO view VALUES (0, 6, 7, 1420864053, 0, 1420864053);
INSERT INTO view VALUES (1, 5, 6, 1420846053, 0, 1420864053);
INSERT INTO view VALUES (2, 7, 8, 1420866043, 0, 1420864053);
INSERT INTO view VALUES (3, 4, 9, 1420866003, 0, 1420864053);
INSERT INTO view VALUES (4, 8, 5, 1420861053, 0, 1420864053);
INSERT INTO view VALUES (5, 3, 3, 1420868053, 0, 1420864053);
INSERT INTO view VALUES (6, 1, 4, 1420863053, 0, 1420864053);
INSERT INTO view VALUES (7, 2, 1, 1420852053, 0, 1420864053);
INSERT INTO view VALUES (8, 1, 2, 1420846053, 0, 1420864053);
INSERT INTO view VALUES (9, 0, 0, 1420867053, 0, 1420864053);

INSERT INTO favourite VALUES (0, 3, 2);
INSERT INTO favourite VALUES (1, 7, 1);
INSERT INTO favourite VALUES (2, 0, 6);
INSERT INTO favourite VALUES (3, 1, 6);
INSERT INTO favourite VALUES (4, 2, 6);

INSERT INTO friend VALUES (0,0,1);
INSERT INTO friend VALUES (1,0,2);
INSERT INTO friend VALUES (2,2,1);
INSERT INTO friend VALUES (3,7,6);
INSERT INTO friend VALUES (4,9,3);
INSERT INTO friend VALUES (5,6,1);
INSERT INTO friend VALUES (6,6,5);
