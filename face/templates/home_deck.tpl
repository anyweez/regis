<p style="margin-top: 20px;">
  {{text}}
  Codepath is here for one reason: to help you practice your algorithmic thinking skills.  We provide
  you with a single programming problem to focus on at a time and learn your strengths and weaknesses as you work.
</p>
<p>
  Codepath is language-agnostic.  Use it to practice a language you already know or even to learn one
  that you've never used before.
</p>

<div id="extra_login" style="text-align: center; margin-top: 5px;">
  {% for name in social_auth.backends.openid %}
	<p>Here: {{ name }}</p>
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
	<p>There: {{ name }}</p>
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
