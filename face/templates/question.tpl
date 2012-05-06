<h2>{{question.status|capfirst}} Question</h2>
<div class="card-close-btn">X</div>
<div class="question-body" style="padding: 3px;">
  <p style="font-size: small;">released on {{ question.released }}</p>
  <p>{{question.text|safe}}</p>

  <form id="answerbox" style="height: 40px;">
    <input type="text" value="" name="answer">
    <input type="submit" value="Check" name="submit">
  </form>
  <div id="hintbox" style="display:inline;">
  </div>
</div>
