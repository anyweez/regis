<form method="post" action="/ajax/hints/submit/{{ question.tid.id }}">
  {% csrf_token %}
  <textarea style="width: 90%;" name="hinttext"></textarea>
  <input type='submit' value="Submit your Hint" />
</form>