{% comment %}

hint_vote_body.tpl is intended to be injected into a web page.

Requires:
hintid
hintcontent
votetotal

{% endcomment %}
<div class='votepane'>
  <div class='hintvoter'>
    <a onclick="hint_vote_up({{ hintid }}, true)">
      <img title='Upvote this hint' src='/static/img/approve.png' />
    </a>
    <a onclick="hint_vote_down({{ hintid }}, false)">
      <img title="Downvote this hint" src="/static/img/disapprove.png" />
    </a>
  </div>
  <div class="hintscore" id="score_{{ hintid }}">
    {{ votetotal }}
  </div>
</div>
<div style="vertical-align: top; display: inline-block; margin-top: 2px; width: 90%;">
  {{ hintcontent }}
</div>
