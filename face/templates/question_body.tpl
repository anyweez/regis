{% comment %} 
question_box.tpl is intended to be injected into a web page.

Requires:
questionstatus
questiontitle
questionnumber (actually template.id)
questioncontent
questionpublished
numberhints

{% endcomment %}
{% if questionstatus == "released" %}
  <h2 style="margin-bottom: 5px;">
    Question #{{ questionnumber }}:
    <span style="font-weight: normal">{{ questiontitle }}</span>
  </h2>
  <p style="color: #555; margin: 0px 0px 10px 3px; padding: 0;">
  released on {{ questionpublished }}
  </p>
  <p id="main_q">{{ questioncontent }}</p>
  <div id="answerbox" style="height: 40px;">
    <form accept-charset="utf-8" method="post" action="/question/check">
      <div style="display:none">
        <input type="hidden" value="f4d76ce04b9550de5aee68dc690efb5c" name="csrfmiddlewaretoken">
      </div>
      <input type="text" style="font-size: 20px; margin: 0; border-radius: 5px 0px 0px 5px; height: 30px;" value="" name="answer">
      {% comment %} questionnumber is actually the templateid {% endcomment %}
      <input type="hidden" value="{{ questionnumber }}" name="qid">
      <input type="hidden" value="/dash" name="on_correct">
      <input type="hidden" value="/dash" name="on_incorrect">
      <input type="submit" value="Guess" name="submit">
    </form>
  </div>
  <div id="hintzone" class="hintbox">
    <img src="/static/img/hint.png">
    <span id="hintdrop">
      {% if numhints == 0 %}
        No hints are currently available.
      {% else %}{% if numhints == 1 %}
        1 hint is currently available for this question.
      {% else %}{% if numhints > 1 %}
        {{ numhints }} hints are currently available for this question.
      {% endif %}{% endif %}{% endif %}
    </span>
    <div id="hintdisplay" style="display: none;"></div>
  </div>
{% else %}{% if questionstatus == "doesnotexist" %}
  <h2 style="margin-bottom: 5px;">
    Question does not exist
  </h2>
  <p style="color: #555; margin: 0px 0px 10px 3px; padding: 0;">
  </p>
  <p id="main_q">{{ questioncontent }}</p>
  <div id="answerbox" style="height: 40px;">
    <form accept-charset="utf-8" method="post" action="/question/check">
      <div style="display:none">
        <input type="hidden" value="f4d76ce04b9550de5aee68dc690efb5c" name="csrfmiddlewaretoken">
      </div>
      <input type="text" style="font-size: 20px; margin: 0; border-radius: 5px 0px 0px 5px; height: 30px;" value="" name="answer">
      {% comment %} questionnumber is actually the templateid {% endcomment %}
      <input type="hidden" value="/dash" name="on_correct">
      <input type="hidden" value="/dash" name="on_incorrect">
      <input type="submit" value="Guess" name="submit">
    </form>
  </div>
  <div id="hintzone" class="hintbox">
    <img src="/static/img/hint.png">
    <span id="hintdrop">
      {% if numhints == 0 %}
        No hints are currently available.
      {% else %}{% if numhints == 1 %}
        1 hint is currently available for this question.
      {% else %}{% if numhints > 1 %}
        {{ numhints }} hints are currently available for this question.
      {% endif %}{% endif %}{% endif %}
    </span>
    <div id="hintdisplay" style="display: none;"></div>
  </div>
{% else %}
  <h2 style="margin-bottom: 5px;">
    Question #{{ questionnumber }}:
    <span style="font-weight: normal">{{ questiontitle }}</span>
  </h2>
  <p style="color: #555; margin: 0px 0px 10px 3px; padding: 0;">
  </p>
  <p id="main_q">{{ questioncontent }}</p>
  <div id="answerbox" style="height: 40px;">
    <form accept-charset="utf-8" method="post" action="/question/check">
      <div style="display:none">
        <input type="hidden" value="f4d76ce04b9550de5aee68dc690efb5c" name="csrfmiddlewaretoken">
      </div>
      <input type="text" style="font-size: 20px; margin: 0; border-radius: 5px 0px 0px 5px; height: 30px;" value="" name="answer">
      {% comment %} questionnumber is actually the templateid {% endcomment %}
      <input type="hidden" value="{{ questionnumber }}" name="qid">
      <input type="hidden" value="/dash" name="on_correct">
      <input type="hidden" value="/dash" name="on_incorrect">
      <input type="submit" value="Guess" name="submit">
    </form>
  </div>
  <div id="hintzone" class="hintbox">
    <img src="/static/img/hint.png">
    <span id="hintdrop">
      {% if numhints == 0 %}
        No hints are currently available.
      {% else %}{% if numhints == 1 %}
        1 hint is currently available for this question.
      {% else %}{% if numhints > 1 %}
        {{ numhints }} hints are currently available for this question.
      {% endif %}{% endif %}{% endif %}
    </span>
    <div id="hintdisplay" style="display: none;"></div>
  </div>
{% endif %}{% endif %}


