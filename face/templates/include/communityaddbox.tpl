<div id="suggestbox" style="height: 40px;">
  <form action="/community/add/submit" method="post" accept-charset="utf-8">
    {% csrf_token %}
    <br />
    Question:<br />
    <textarea name="question" id="question" value="" rows="3" cols="50" style="font-size: 15px; margin: 0; border-radius: 5px 0px 0px 5px; height: 90px; width: 90%;"></textarea>
  	<br />
    Answer:<br />
    <textarea name="answer" id="answer" value="" rows="3" cols="50" style="font-size: 15px; margin: 0; border-radius: 5px 0px 0px 5px; height: 60px; width: 90%"/></textarea><br />
    Question Type:<br />
    <input type="radio" name="subjective" id="subj" value="exact" />Exact answer<br />
    <input type="radio" name="subjective" id="subj" value="free" />Free response<br /> 
    <input type="submit" name="submit" value="Submit" style="border-radius: 4px; display: block; right: 0px; margin-top: 8px;" />
  </form>
</div>
