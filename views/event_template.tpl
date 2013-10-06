<!DOCTYPE html>
<html>
<head>
<title>Eventsito</title>
</head>
<body>

%if (username != None):
Welcome {{username}}        <a href="/logout">Logout</a> | <a href="/newevent">New Event</a><p>
%end

<h1>Events</h1>

%for event in myevents:
<h2><a href="/event/{{event['permalink']}}">{{event['title']}}</a></h2>
Event date: {{event['start_date']}} to {{event['end_date']}}<br>
Comments: 
%if ('comments' in event):
%numComments = len(event['comments'])
%else:
%numComments = 0
%end
<a href="/event/{{event['permalink']}}">{{numComments}}</a>
<hr>
{{!event['description']}}
<p>
<p>
<em>Filed Under</em>: 
%if ('tags' in event):
%for tag in event['tags'][0:1]:
<a href="/tag/{{tag}}">{{tag}}</a>
%for tag in event['tags'][1:]:
, <a href="/tag/{{tag}}">{{tag}}</a>
%end
%end

<p>
%end
</body>
</html>


