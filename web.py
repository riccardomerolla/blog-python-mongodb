import pymongo
import eventsDAO
import blogPostDAO
import sessionDAO
import userDAO
import bottle
import cgi
import re
import os

# This route is the main page of the blog
@bottle.route('/')
def blog_index():

    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)

    # even if there is no logged in user, we can show the blog
    #l = posts.get_posts(10)
    l = events.get_events(10)

    #return bottle.template('blog_template', dict(myposts=l, username=username))
    return bottle.template('event_template', dict(myevents=l, username=username))

# Displays a particular event
@bottle.get("/event/<permalink>")
def show_event(permalink="notfound"):

    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)
    permalink = cgi.escape(permalink)

    print "about to query on permalink = ", permalink
    event = events.get_event_by_permalink(permalink)

    if event is None:
        bottle.redirect("/event_not_found")

    # init comment form fields for additional comment
    comment = {'name': "", 'body': "", 'email': ""}

    return bottle.template("entry_event_template", dict(event=event, username=username, errors="", comment=comment))

@bottle.get("/event_not_found")
def event_not_found():
    return "Sorry, event not found"


# Displays the form allowing a user to add a new post. Only works for logged in users
@bottle.get('/newevent')
def get_newevent():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect("/login")

    return bottle.template("newevent_template", dict(title="", description="", start_date="", end_date="", personalized_url="", venue_id="",
     organizer_id="", capacity="", confirmation_email="", errors="", tags="", username=username))

#
# Post handler for setting up a new post.
# Only works for logged in user.
@bottle.post('/newevent')
def post_newevent():
    title = bottle.request.forms.get("title")
    description = bottle.request.forms.get("description")
    start_date = bottle.request.forms.get("start_date")
    end_date = bottle.request.forms.get("end_date")
    personalized_url = bottle.request.forms.get("personalized_url")
    venue_id = bottle.request.forms.get("venue_id")
    organizer_id = bottle.request.forms.get("organizer_id")
    capacity = bottle.request.forms.get("capacity")
    confirmation_email = bottle.request.forms.get("confirmation_email")
    tags = bottle.request.forms.get("tags")

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect("/login")

    if title == "" or post == "":
        errors = "Post must contain a title and description entry"
        return bottle.template("newevent_template", dict(title=cgi.escape(title, quote=True), username=username,
                                                        description=cgi.escape(description, quote=True), start_date="", end_date="", 
                                                        personalized_url="", venue_id="", organizer_id="", capacity="", confirmation_email="", 
                                                        tags=tags, errors=errors))

    # extract tags
    tags = cgi.escape(tags)
    tags_array = extract_tags(tags)

    # looks like a good entry, insert it escaped
    escaped_description = cgi.escape(description, quote=True)

    # substitute some <p> for the paragraph breaks
    newline = re.compile('\r?\n')
    formatted_description = newline.sub("<p>", escaped_description)

    permalink = events.insert_entry(title, description, start_date, end_date, personalized_url, venue_id, organizer_id, capacity, confirmation_email, tags_array)

    # now bottle.redirect to the blog permalink
    bottle.redirect("/post/" + permalink)



# The main page of the blog, filtered by tag
@bottle.route('/tag/<tag>')
def posts_by_tag(tag="notfound"):

    cookie = bottle.request.get_cookie("session")
    tag = cgi.escape(tag)

    username = sessions.get_username(cookie)

    # even if there is no logged in user, we can show the blog
    l = posts.get_posts_by_tag(tag, 10)

    return bottle.template('blog_template', dict(myposts=l, username=username))


# Displays a particular blog post
@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):

    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)
    permalink = cgi.escape(permalink)

    print "about to query on permalink = ", permalink
    post = posts.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")

    # init comment form fields for additional comment
    comment = {'name': "", 'body': "", 'email': ""}

    return bottle.template("entry_template", dict(post=post, username=username, errors="", comment=comment))


# used to process a comment on a blog post
@bottle.post('/newcomment')
def post_new_comment():
    name = bottle.request.forms.get("commentName")
    email = bottle.request.forms.get("commentEmail")
    body = bottle.request.forms.get("commentBody")
    permalink = bottle.request.forms.get("permalink")

    post = posts.get_post_by_permalink(permalink)
    cookie = bottle.request.get_cookie("session")

    username = sessions.get_username(cookie)

    # if post not found, redirect to post not found error
    if post is None:
        bottle.redirect("/post_not_found")
        return

    # if values not good, redirect to view with errors

    if name == "" or body == "":
        # user did not fill in enough information

        # init comment for web form
        comment = {'name': name, 'email': email, 'body': body}

        errors = "Post must contain your name and an actual comment."
        return bottle.template("entry_template", dict(post=post, username=username, errors=errors, comment=comment))

    else:

        # it all looks good, insert the comment into the blog post and redirect back to the post viewer
        posts.add_comment(permalink, name, email, body)

        bottle.redirect("/post/" + permalink)

@bottle.get("/post_not_found")
def post_not_found():
    return "Sorry, post not found"


# Displays the form allowing a user to add a new post. Only works for logged in users
@bottle.get('/newpost')
def get_newpost():

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect("/login")

    return bottle.template("newpost_template", dict(subject="", body = "", errors="", tags="", username=username))

#
# Post handler for setting up a new post.
# Only works for logged in user.
@bottle.post('/newpost')
def post_newpost():
    title = bottle.request.forms.get("subject")
    post = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        bottle.redirect("/login")

    if title == "" or post == "":
        errors = "Post must contain a title and blog entry"
        return bottle.template("newpost_template", dict(subject=cgi.escape(title, quote=True), username=username,
                                                        body=cgi.escape(post, quote=True), tags=tags, errors=errors))

    # extract tags
    tags = cgi.escape(tags)
    tags_array = extract_tags(tags)

    # looks like a good entry, insert it escaped
    escaped_post = cgi.escape(post, quote=True)

    # substitute some <p> for the paragraph breaks
    newline = re.compile('\r?\n')
    formatted_post = newline.sub("<p>", escaped_post)

    permalink = posts.insert_entry(title, formatted_post, tags_array, username)

    # now bottle.redirect to the blog permalink
    bottle.redirect("/post/" + permalink)


# displays the initial blog signup form
@bottle.get('/signup')
def present_signup():
    return bottle.template("signup",
                           dict(username="", password="",
                                password_error="",
                                email="", username_error="", email_error="",
                                verify_error =""))

# displays the initial blog login form
@bottle.get('/login')
def present_login():
    return bottle.template("login",
                           dict(username="", password="",
                                login_error=""))

# handles a login request
@bottle.post('/login')
def process_login():

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    print "user submitted ", username, "pass ", password

    user_record = users.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session_id = sessions.start_session(user_record['_id'])

        if session_id is None:
            bottle.redirect("/internal_error")

        cookie = session_id

        # Warning, if you are running into a problem whereby the cookie being set here is
        # not getting set on the redirect, you are probably using the experimental version of bottle (.12).
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)

        bottle.redirect("/welcome")

    else:
        return bottle.template("login",
                               dict(username=cgi.escape(username), password="",
                                    login_error="Invalid Login"))


@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return {'error':"System has encountered a DB error"}


@bottle.get('/logout')
def process_logout():

    cookie = bottle.request.get_cookie("session")

    sessions.end_session(cookie)

    bottle.response.set_cookie("session", "")


    bottle.redirect("/signup")


@bottle.post('/signup')
def process_signup():

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")

    # set these up in case we have an error case
    errors = {'username': cgi.escape(username), 'email': cgi.escape(email)}
    if validate_signup(username, password, verify, email, errors):

        if not users.add_user(username, password, email):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return bottle.template("signup", errors)

        session_id = sessions.start_session(username)
        print session_id
        bottle.response.set_cookie("session", session_id)
        bottle.redirect("/welcome")
    else:
        print "user did not validate"
        return bottle.template("signup", errors)



@bottle.get("/welcome")
def present_welcome():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        print "welcome: can't identify user...redirecting to signup"
        bottle.redirect("/signup")

    return bottle.template("welcome", {'username': username})



# Helper Functions

#extracts the tag from the tags form element. an experience python programmer could do this in  fewer lines, no doubt
def extract_tags(tags):

    whitespace = re.compile('\s')

    nowhite = whitespace.sub("",tags)
    tags_array = nowhite.split(',')

    # let's clean it up
    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)

    return cleaned


# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True

connection_string = "mongodb://heroku:heroku@paulo.mongohq.com:10000/app18514552"
connection = pymongo.MongoClient(connection_string)
database = connection.app18514552

events = eventsDAO.EventsDAO(database)
posts = blogPostDAO.BlogPostDAO(database)
users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)


bottle.debug(True)
bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

