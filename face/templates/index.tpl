<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
  <script type="text/javascript" src="/static/js/underscore.js"></script>
  <script type="text/javascript" src="/static/js/jquery.js"></script>
  <script type="text/javascript" src="/static/js/backbone.js"></script>
  <script type="text/javascript" src="/static/js/regis/regis.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      // Initialize Regis and get some decks.
      regis_init();
      deck = regis.Deck('Home', 'home');
      
      // Activate a deck after some time has passed.  This should be
      // converted to an event eventually.
      setTimeout(function() { regis.activateDeck(deck); }, 500);
    });
  </script>

  <title>Welcome to codepath!</title>
  {% include 'include/common_header.tpl' %}
</head>
<body>
  <div id='main-display'>
    <h1 id="codepath-title"><span class="cp_first">code</span><span class="cp_second">path</span></h1>
    <div id="navigation">
<!--         <div id="profile_btn"><img src="/static/img/profile.png" />profile</div> -->
    </div>
    <div id='card-stack'>
    </div>
  </div>

</body>
</html>
