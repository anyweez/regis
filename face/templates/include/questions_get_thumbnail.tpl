{% comment %} 
question_thumbnail.tpl is intended to be injected into a web page.

Requires:
questionstatus
questiontitle
questionnumber (actually template.id)
questioncontent
questionpublished
hintids

{% endcomment %}
<div id="question{{ questionnumber }}" class="qbox status_{{ questionstatus }}">
  <div class="question_status">
    {% if questionstatus == 'ready' or questionstatus == 'pending' %}
      <div class="q_decoration">
        <p class="q_status">Locked.</p>
        <p>Solved by 2 of 8 students.</p>
        <p>( 25% )</p>
      </div>
    {% endif %}
    {% if questionstatus == 'released' %}
      <div class="q_decoration">
        <p class="q_status">Unsolved.</p>
        <p>Solved by 2 of 8 students.</p>
        <p>( 25% )</p>
      </div>
    {% endif %}
    {% if questionstatus == 'solved' %}
      <div class="q_decoration">
        <p class="q_status">Solved!</p>
        <p>Solved by 2 of 8 students.</p>
        <p>( 25% )</p>
      </div>
    {% endif %} 
  </div>
  
  <div class="question_content">
    {% if questionstatus == 'ready' or questionstatus == 'pending' %}
      <h2 class="qbox_head">
        Question #{{ questionnumber }}: {{ questiontitle }}
      </h2>
      <p class="qbox_preview" style="font-style: italic">This question isn't available yet.</p>
    {% else %}
      <h2 class="qbox_head">Question #{{ questionnumber }}: <a href="{{questionnumber}}">{{ questiontitle }}</a></h2>
      {% if questioncontent|length > 60 %}
        <p class="qbox_preview">{{ questioncontent|slice:":200" }}...</p>
      {% else %}
        <p class="qbox_preview">{{ questioncontent }}</p>
      {% endif %}
    {% endif %}
    
  
  </div>
</div>
