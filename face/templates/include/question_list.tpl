
      {% for q in questions %}
        {% if q.status != 'pending' %}
        <div class="qbox">
		  {% if q.status == 'ready' %}
		  <div class="q_decoration q_unavailable">
		    <p class="q_status">locked</p>
		  {% endif %}
		  {% if q.status == 'released' %}
		  <div class="q_decoration q_unanswered">
		    <p class="q_status">unsolved</p>
		  {% endif %}
		  {% if q.status == 'solved' %}
		  <div class="q_decoration q_answered">
		    <p class="q_status">solved</p>
		  {% endif %} 
		  
		    <p>solved by 2 of 8</p>
		    <p>( 25% )</p>
		  </div>
          <div>
            {% if q.status == 'ready' %}
              <h2 class="qbox_head">Question #{{ q.template.id }}: {{ q.template.title }}</h2>
              <p class="qbox_preview" style="font-style: italic">This question isn't available yet.</p>
            {% else %}
              <h2 class="qbox_head">Question #{{ q.template.id }}: <a href="{{q.template.id}}/">{{ q.template.title }}</a></h2>
              {% if q.text|length > 60 %}
                <p class="qbox_preview">{{ q.text|slice:":200" }}...</p>
              {% else %}
                <p class="qbox_preview">{{ q.text }}</p>
              {% endif %}
            {% endif %}
            

          </div>
        </div>
        {% endif %}
      {% endfor %}
