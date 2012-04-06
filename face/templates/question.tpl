<h2>{{question.status|capfirst}} Question</h2>
<div class="card-close-btn">X</div>
<div style="padding: 3px;">
  <p style="font-size: small;">released on {{ question.time_released }}</p>
  <p>{{question.decoded_text|safe}}</p>

  <div id="answerbox" style="height: 40px;">
    <input type="text" value="" name="answer">
    <input onclick="submit_question({{ question.id }});" type="submit" value="Guess" name="submit">
  </div>
</div>
