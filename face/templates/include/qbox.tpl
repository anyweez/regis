<div id="answerbox" style="height: 40px;">
  <form action="/question/check" method="post" accept-charset="utf-8">
    {% csrf_token %}
    <input type="text" name="answer" value="" style="font-size: 20px; margin: 0; border-radius: 5px 0px 0px 5px; height: 30px;"  />
    <input type="hidden" name="qid" value="{{ question.id }}" />

    <input type="hidden" name="on_correct" value="/dash" />
    <input type="hidden" name="on_incorrect" value="/dash" />

    <input style="font-size: 15px; text-shadow: 1px 1px 1px #AAA;" type="submit" name="submit" value="Submit"  />
  </form>
</div>
