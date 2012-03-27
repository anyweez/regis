<h2>{{question.status|capfirst}} Question</h2>
<p style="font-size: small;">released on {{ question.time_released }}</p>
<p>{{question.decoded_text|safe}}</p>

<div id="answerbox" style="height: 40px;">
<!--  <form accept-charset="utf-8" method="post" action="/question/check"> -->
  {% csrf_token %}
    <input type="text" value="" name="answer">
    <input onclick="submit_question({{ question.template.id }});" type="submit" value="Guess" name="submit">
<!--  </form>  -->
</div>