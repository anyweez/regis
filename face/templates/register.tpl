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
    <form action="http://localhost:8000/account/create" method="post" accept-charset="utf-8">  
      {% csrf_token %}
      <div>
		{% for m in messages %}
		<p>{{ m.0 }}</p>
		{% endfor %}
		
		{% for e in errors %}
		<p>{{ e }}</p>
		{% endfor %}
		
        <label for="league_id">League:</label> 
        <select name="league_id">
          {% for league in form.leagues %}
          <option value="{{ league.0 }}">{{ league.1 }}</option>
          {% endfor %}
        </select>
      </div>
      <div>
        <label for="username">Username:</label>
        <input type="text" name="username" />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="text" name="email" />
      </div>
      <div>
        <label for="id_password">Password:</label>
        <input type="password" name="password" />
      </div>
      <div>
        <label for="id_password">Repeat password:</label>
        <input type="password" name="password2" />
      </div>
	  <div style="margin-top: 10px;">
	    <input onclick="window.location='http://localhost:8000/'" type="button" value="Cancel" />
	    <input type="submit" name="login" value="Create account"  />        
	  </div>
	</form>
  </div>
</body>
</html>
