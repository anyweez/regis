<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

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

  <title>Welcome to Regis!</title>
</head>
<body>
  <div style="margin-top: 7%;" id="logbox">
    <img style="display: block; margin: 0 auto" src="static/img/logo-large.png" />
    <p style="margin-top: 20px;">Regis is a tool for practicing programming skills.  It generates a unique question for
    you each day and customizes its content to give you the best practice possible.</p>

	{% if errors %}
	<div class="error">
      {% for e in errors %}
      <p>{{ e }}</p>
      {% endfor %}
    </div>
    {% endif %}
    
    <div id="login_form" style="margin: 0 auto; width: 550px;">
      <form action="/account/login" method="post" accept-charset="utf-8">    
      {% csrf_token %}
      <label for="username">Username: </label>    
      <input type="text" name="username" value="" id="email" style="width: 12em;"  />    
      
      <span style="margin-left: 1em;">
        <label for="password">Password: </label>
      </span>
      <input type="password" name="password" value="" id="password" style="width: 12em;" />
      <div style="text-align: center; margin: 1em 0em 1em 0em;">
        <input type="submit" name="login" value="Log In" id="login" style="width: 5em;" />
      </div>
    </form>    
    </div>
	<div id="extra_login" style="text-align: center; margin-top: 5px;">
	  <a href="account/create">register</a>
	</div>
    
  </div>
</body>
</html>
