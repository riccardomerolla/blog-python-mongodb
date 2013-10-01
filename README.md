blog-python-mongodb
===================

Simple Blog in Python and MongoDB

# mongo shell
use blog
db.posts.drop()

# terminal
mongoimport -d blog -c posts < posts.json

python blog.py

http://localhost:8082/
