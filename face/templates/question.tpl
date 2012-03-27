<h2>{{question.status|capfirst}} Question [{{question.template.id}}]</h2>
<div style="padding: 3px;">
  <p style="font-size: small;">released on {{ question.time_released }}</p>
  <p>{{question.decoded_text|safe}}</p>

  <div id="answerbox" style="height: 40px;">
    <input type="text" value="" name="answer">
    <input onclick="submit_question({{ question.template.id }});" type="submit" value="Guess" name="submit">
  </div>
</div>