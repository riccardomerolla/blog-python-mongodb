<!doctype HTML>
<html
<head>
<title>
Event
</title>
</head>
<body>
%if (username != None):
Welcome {{username}}        <a href="/logout">Logout</a> | 
%end
<a href="/">Eventsito</a><br><br>

<h2>{{event['title']}}</h2>
Event date: {{event['start_date']}} to {{event['end_date']}}<br>
<hr>
{{!event['description']}}
<p>
<em>Filed Under</em>: 
%if ('tags' in event):
%for tag in event['tags'][0:1]:
<a href="/tag/{{tag}}">{{tag}}</a>
%for tag in event['tags'][1:]:
, <a href="/tag/{{tag}}">{{tag}}</a>
%end
%end
%end
<p>
Comments: 
<ul>
%if ('comments' in event):
%numComments = len(event['comments'])
%else:
%numComments = 0
%end
%for i in range(0, numComments):
Author: {{event['comments'][i]['author']}}<br>
{{event['comments'][i]['body']}}<br>
<hr>
%end
<h3>Add a comment</h3>
<form action="/newcomment" method="event">
<input type="hidden" name="permalink", value="{{event['permalink']}}">
{{errors}}
<b>Name</b> (required)<br>
<input type="text" name="commentName" size="60" value="{{comment['name']}}"><br>
<b>Email</b> (optional)<br>
<input type="text" name="commentEmail" size="60" value="{{comment['email']}}"><br>
<b>Comment</b><br>
<textarea name="commentBody" cols="60" rows="10">{{comment['body']}}</textarea><br>
<input type="submit" value="Submit">
</ul>
</body>
</html>


