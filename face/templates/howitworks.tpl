<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

  {% include 'include/common_header.tpl' %}

  <title>Regis: how it works</title>
</head>
<body>    
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
    <!-- Container for the majority of the page's content. -->
    <div id="middle_container">
      <div id="left_body">
  &nbsp;
      </div>
      <div id="center_body"> 
        <h2>How Regis Works</h2>
        <p>Regis releases one question to you every other day.  A new question will be immediately released
        if you're able to solve one of the problems available to you.</p>
        <p>The question database contains a series of templates that can be personalized for each user.  Each
        question that you receive has a very high probability of being unique among all users, but is similar
        enough that it should be possible to discuss algorithmic approaches to solving it if you'd like to.</p>
        <h3>Fine print for earning questions</h3>
        <p>Regis actually releases new questions when you log in -- this means that waiting for a month before
        signing in will only earn you one new question.  You can unlock a new question every other day if you
        sign in after the 48-hour timer expires; a countdown clock appears under the title of your <a href="/dash">current
        question</a>.</p>
        <h3>How Regis Learns</h3>
        <p>Regis records actions that you make on the site, including correct and incorrect guesses.  We're
        able to get a general feel for the difficulty of particular problem after enough users have attempted
        it, and are also able to get a feel for your conceptual strengths and weaknesses after you've attempted
        enough questions.  In addition, the feedback you provide after correctly answering a question plays
        a significant role in determining your interests and comfort level with particular topics.</p>
        <p>The learning system itself is still in its very early stages and may change fairly drastically in the
        coming months.</p>
      </div>  
{% comment %}      {% include 'include/sidebar.tpl' %} {% endcomment %}
      <div style="clear: both; height: 0px;">&nbsp;</div>
    </div> <!--  end middle_container -->
  
    <!-- Container for the information that appears below the main content (i.e. licensing info). -->
    <div id="footer">
    </div>
  </div> 
</body>
</html>
