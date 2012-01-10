<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="static/css/main.css" />

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
    <div style="display: inline;">
    <img style="float: left; width: 237px; margin-right: 10px;" src="images/title_big_bl.png" />
    <span style="float: left; width: 350px; margin-top: 20px;">Regis is a tool for practicing programming skills.  It generates a unique question for
    you each day and gives you points based on how quickly you can answer it.</span>
    </div>
    <div style="clear: both;">&nbsp;</div>
    
    <div id="login_form" style="margin: 0 auto; width: 550px;">
      <form action="http://temple.lukesegars.com/regis/account/login" method="post" accept-charset="utf-8">    
      <label for="email">Email: </label>    
      <input type="text" name="email" value="" id="email" style="width: 12em;"  />    
      
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
