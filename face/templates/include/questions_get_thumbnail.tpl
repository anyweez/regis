{% comment %} 
question_thumbnail.tpl is intended to be injected into a web page.

Requires:
questionstatus
questiontitle
questionnumber (actually template.id)
questioncontent
questionpublished
hintids

Uses (optional):
questionstats
{% endcomment %}
<div id="question{{ questionnumber }}" class="qbox status_{{ questionstatus }}">
  <div class="question_status">
      <div class="q_decoration">
        {% if questionstatus == 'ready' or questionstatus == 'pending' %}
          <p class="q_status">Locked.</p>
        {% endif %}
        {% if questionstatus == 'released' %}
          <p class="q_status">Unsolved.</p>
        {% endif %}
        {% if questionstatus == 'solved' %}
          <p class="q_status">Solved!</p>
        {% endif %} 
        <p>Solved by {{ questionstats.num_solved }} of {{ questionstats.num_available }} students.</p>
        <p>( {{ questionstats.solved_percent }}% )</p>
      </div>
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
