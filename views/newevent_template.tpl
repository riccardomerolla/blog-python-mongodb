<!doctype HTML>
<html>
<head>
<title>Create a new event</title>
</head>
<body>
%if (username != None):
Welcome {{username}}        <a href="/logout">Logout</a> | <a href="/">Eventsito</a><p>
%end
<form action="/newevent" method="POST">
{{errors}}
<h2>Title</h2>
<input type="text" name="title" size="120" value="{{title}}"><br>
<h2>Description<h2>
<textarea name="description" cols="120" rows="20">{{description}}</textarea><br>
<h2>Start date</h2>
<input type="date" name="start_date" value="{{start_date}}"><br>
<h2>End date</h2>
<input type="date" name="end_date" value="{{end_date}}"><br>
<h2>Personalize url</h2>
<input type="text" name="personalized_url" size="120" value="{{personalized_url}}"><br>
<h2>Confirmation email</h2>
<input type="text" name="confirmation_email" size="120" value="{{confirmation_email}}"><br>
<h2>Venue id</h2>
<input type="text" name="venue_id" size="30" value="{{venue_id}}"><br>
<h2>Organizer id</h2>
<input type="text" name="organizer_id" size="30" value="{{organizer_id}}"><br>
<h2>Capacity</h2>
<input type="text" name="capacity" size="30" value="{{capacity}}"><br>
<h2>Tags</h2>
Comma separated, please<br>
<input type="text" name="tags" size="120" value="{{tags}}"><br>
<p>
<input type="submit" value="Submit">

</body>
</html>

