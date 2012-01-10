<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="../static/css/main.css" />

  <style type="text/css">
    #logbox {
      background-color: white;
      width: 38em;
      padding: 1%;
      margin: 0 auto;

      border: 3px solid black;
      border-radius: 3px;
    }
  </style>

  <title>Regis: register</title>
</head>
<body>
  <div style="margin-top: 7%;" id="logbox">
    <p>Registration for Regis is quick and free.  Just fill out the form below and you'll be good to go.</p>
    <form action="http://localhost:8000/account/store" method="post" accept-charset="utf-8">  
      {% csrf_token %}
      <div>
        <label for="id_league">League:</label> 
        {{ form.league }}
      </div>
      <div>
        <label for="id_username">Username:</label>
        {{ form.username }}
      </div>
      <div>
        <label for="id_password">Password:</label>
        {{ form.password }}
      </div>
      <div>
        <label for="id_password">Email:</label>
        {{ form.email }}
      </div>
	  <div style="margin-top: 10px;">
	    <input onclick="window.location='http://localhost:8000/'" type="button" value="Cancel" />
	    <input type="submit" name="login" value="Create account"  />        
	  </div>
	</form>
  </div>
</body>
</html>
