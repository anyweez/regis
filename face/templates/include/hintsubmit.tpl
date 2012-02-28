<form method="post" action="/ajax/hints/submit/{{ question.template.id }}">
  {% csrf_token %}
  <textarea style="width: 90%;" name="hinttext"></textarea>
  <input style="border-radius: 0px; right: 0px; height: 30px;" type='submit' value="Submit your Hint" />
</form>