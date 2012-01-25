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
  {% include 'include/common_header.tpl' %}
</head>
<body>
  <div style="margin-top: 7%;" id="logbox">
    <img style="display: block; margin: 0 auto" src="static/img/logo-large.png" />
    <p style="margin-top: 20px;">Regis is a tool for practicing programming skills.  It generates a unique question for
    you every other day and customizes its content to give you the best practice possible.</p>

	{% if errors %}
	<div class="error">
      {% for e in errors %}
      <p>{{ e }}</p>
      {% endfor %}
    </div>
    {% endif %}

	<div id="extra_login" style="text-align: center; margin-top: 5px;">
	  {% for name in social_auth.backends.oauth %}
	    <p><a rel="nofollow" href="{% url socialauth_begin name %}">{{ name }}</a></p>
	  {% endfor %}
	  {% for name in social_auth.backends.openid %}
	    {% if name == 'google' %}
	    <a rel="nofollow" href="{% url socialauth_begin name %}">
	      <div class="login_btn">
	        <img src="/static/img/google.png" />
	        <span>Log in with Google</span>
	      </div>
	    </a>	  
	    {% endif %}
	  {% endfor %}
	  {% for name in social_auth.backends.oauth2 %}
	    {% if name == 'facebook' %}
	    <a rel="nofollow" href="{% url socialauth_begin name %}">
	      <div class="login_btn">
	        <img src="/static/img/facebook.png" />
	        <span>Log in with Facebook</span>
	      </div>
	    </a>
	    {% endif %}
	  {% endfor %}
	</div>
  </div>
</body>
</html>
