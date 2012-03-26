<p style="font-size: small;">released on {{ time_released }}</p>
<p>{{text}}</p>

<div id="answerbox" style="height: 40px;">
<!--  <form accept-charset="utf-8" method="post" action="/question/check"> -->
  {% csrf_token %}
    <input type="text" value="" name="answer">
    <input onclick="submit_question({{ question_num }});" type="submit" value="Guess" name="submit">
<!--  </form>  -->
</div>