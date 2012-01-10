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

  <title>Regis: Dashboard for {{ user.username }}</title>
</head>
<body>
	{% if errors %}
	<div class="error">
      {% for e in errors %}
      <p>{{ e }}</p>
      {% endfor %}
    </div>
    {% endif %}
    
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="main_body">
    <div id="question_body">
              <h2 style="margin-bottom: 5px;">Challenge: <span style="font-weight: normal">Credit is Due</span></h2>
        <p style="font-size: small; margin-top: 0px; color: #666666;">New question released in 5 hours, 26 minutes, 8 seconds.</p>
        	    <p id="main_q">Modern credit card numbers (as well as many other ID numbers) are computed to be valid according to a function called the Luhn algorithm.  The purpose of this function is to give banks, retailers, and others who deal with credit cards the ability to quickly distinguish between potentially legitimate credit card numbers and random collections of digits.

If you want the following credit card number to be valid according to the Luhn algorithm, what would the last digit have to be?

<div class="q_text">604336569426524x</div></p>
        <div id="answerbox" style="height: 40px;">
<form action="http://temple.lukesegars.com/regis/check" method="post" accept-charset="utf-8">
<input type="text" name="answer" value="" disabled="disabled" style="font-size: 20px; margin: 0; border-radius: 5px 0px 0px 5px; height: 30px;"  />
<input type="hidden" name="qid" value="19" />

<input type="hidden" name="on_correct" value="today" />

<input type="hidden" name="on_incorrect" value="today" />
<input type="submit" name="submit" value="Solved" disabled="disabled" style="position: relative; right: 4px; bottom: 1px; font-size: 1em; border-radius: 0px 5px 5px 0px; height: 42px; border-left-width: 0px;"  /></form></div>          </div>  
    <div id="right_col">
      <div id="small_right">
        <h3>{{ user.get_full_name }}</h3>
        <p style="margin: 20px 0 6px 0; padding: 0;"><b>1360.88</b> points <span style="color: green;"> (+### yesterday)</span></p>

        <p style="margin: 2px 0 20px 0; padding: 0;"><b>1360.88</b> team points <span style="color: green;"> (+### yesterday)</span></p>
        <div style="width: 95%; height: 120px;" id="chart_div">[snazzy point chart]</div>
        <div style="width: 100%; height: 20px;" id="legend_div">[snazzy point chart]</div>
      </div>
      <div id="large_right">

        <h3>Key Stats</h3>
        <table class="stat_display" style="width: 100%">
          <tr>
            <td style="width: 45%; text-align: right; padding-right: 5%"><p class="factoid">Current ranking:</p></td>
            <td style="width: 15%;"><img title="Personal ranking" src="images/person.gif" /><span style="font-size: small; margin: 4px;">1 / 2</span></td>
            <td style="width: 15%;"><img title="Your team's ranking" src="images/comment_left.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
          </tr>

          <tr>
            <td style="width: 45%; text-align: right; padding-right: 5%"><p class="factoid">Yesterday's gain:</p></td>
            <td style="width: 15%;"><img title="Personal ranking" src="images/person.gif" /><span style="font-size: small; margin: 4px;">1 / 2</span></td>
            <td style="width: 15%;"><img title="Your team's ranking" src="images/comment_left.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%"><img src="images/globe.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
          </tr>
          <tr>

            <td style="width: 45%; text-align: right; padding-right: 5%"><p class="factoid">% answered:</p></td>
            <td style="width: 15%;"><img src="images/person.gif" /><span style="font-size: small; margin: 4px;">50%</span></td>
            <td style="width: 15%"><img src="images/comment_left.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%"><img src="images/globe.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            </td>
          </tr>
          <tr>

            <td style="width: 45%; text-align: right; padding-right: 5%"><p class="factoid">First-day answers:</p></td>
            <td style="width: 15%;"><img src="images/person.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%;"><img src="images/comment_left.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%;"><img src="images/globe.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
          </tr>
          <tr>
            <td style="width: 45%; text-align: right; padding-right: 5%"><p class="factoid">Avg. points per question:</p></td>

            <td style="width: 15%;"><img src="images/person.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%;"><img src="images/comment_left.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%;"><img src="images/globe.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
          </tr>
          <tr>
            <td style="width: 45%; text-align: right; padding-right: 5%"><p class="factoid">Team completion rate:</p></td>
            <td style="width: 15%;"><img src="images/person.gif" /><span style="font-size: small; margin: 4px;">?</span></td>

            <td style="width: 15%;"><img src="images/comment_left.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
            <td style="width: 15%;"><img src="images/globe.gif" /><span style="font-size: small; margin: 4px;">?</span></td>
          </tr>
        </table>
      </div>
    </div> 
  <div style="clear: both; height: 0px;">&nbsp;</div>
  </div> <!--  end main_body -->

  <!-- Container for the information that appears below the main content (i.e. licensing info). -->
    <div id="footer">
    <p>Page rendered in 0.0328 seconds</p>
  </div>
</div> 
  </div>
</body>
</html>
