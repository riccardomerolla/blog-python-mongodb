import sys
import re
import datetime



# The Event Post Data Access Object handles interactions with the Events collection
class EventsDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.events = database.events

    # inserts the event entry and returns a permalink for the entry
    def insert_event(self, title, description, start_date, end_date, personalized_url, venue_id, organizer_id, capacity, confirmation_email, tags_array):
        print "inserting event entry", title, organizer_id

        # fix up the permalink to not include whitespace

        exp = re.compile('\W') # match anything not alphanumeric
        whitespace = re.compile('\s')
        temp_title = whitespace.sub("_",title)
        permalink = exp.sub('', temp_title)

        # Build a new event
        event = {"title": title,
                "permalink": permalink,
                "description": description,
                "start_date": datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f"),
                "end_date": datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S.%f"),
                "timezone": "",
                "privacy": 1,
                "personalized_url": personalized_url,
                "venue_id": venue_id,
                "organizer_id": organizer_id,
                "capacity": capacity,
                "currency": "",
                "locale": "",
                "status": "draft",
                "custom_header": "",
                "custom_footer": "",
                "confirmation_page": "",
                "confirmation_email": confirmation_email,
                "background_color": "",    
                "text_color": "",    
                "link_color": "",    
                "title_text_color": "",    
                "box_background_color": "",    
                "box_text_color": "",    
                "box_border_color": "",    
                "box_header_background_color": "",    
                "box_header_text_color": "",
                "creation_date": datetime.datetime.utcnow(),
                "last_mod_date": datetime.datetime.utcnow(),
                "comments": [],
                "tags": tags_array}

        # now insert the event
        try:
            self.events.insert(event)
            print "Inserting the event"
        except:
            print "Error inserting event"
            print "Unexpected error:", sys.exc_info()[0]

        return permalink

    # returns an array of num_events events, reverse ordered
    def get_events(self, num_posts):

        cursor = self.events.find().sort('creation_date', direction=-1).limit(num_posts)
        l = []

        for event in cursor:
            if event['start_date'] is not None:
                event['start_date'] = event['start_date'].strftime("%A, %B %d %Y at %I:%M%p")
            if event['end_date'] is not None:
                event['end_date'] = event['end_date'].strftime("%A, %B %d %Y at %I:%M%p")
            if 'tags' not in event:
                event['tags'] = [] # fill it in if its not there already
            if 'comments' not in event:
                event['comments'] = []

            l.append(event)

        return l

    # find a event corresponding to a particular permalink
    def get_event_by_permalink(self, permalink):

        event = self.events.find_one({'permalink': permalink})

        if event is not None:
            # fix up date
            if event['start_date'] is not None:
                event['start_date'] = event['start_date'].strftime("%A, %B %d %Y at %I:%M%p")
            if event['end_date'] is not None:
                event['end_date'] = event['end_date'].strftime("%A, %B %d %Y at %I:%M%p")

        return event









