<div id="suggestbox">
  <form action="/suggest/submit" method="post" accept-charset="utf-8">
    {% csrf_token %}
    <br />
    Question:<br />
    <textarea name="question" id="question_suggestion" value="" rows="3" cols="50"></textarea>
  	<br />
    Sample Solution (optional):<br />
    <textarea name="answer" value="" rows="3" cols="40" /></textarea>
    <input type="submit" name="submit" value="Submit" />
  </form>
</div>
