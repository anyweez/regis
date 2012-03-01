<div id="heading">
    <a href="/dash" style="display: inline-block; margin: 5px 15px 0px 15px;">
      <img src="/static/img/logo-white-small.png" />
    </a>
    
    <div id="navigation">
      <ul>
        <li><a href="/dash">current question</a></li>
        <li><a href="/question/view/all">question list</a></li>
        <!--<li><a href="/team/challenge">team challenge</a></li>-->
        <li><a href="/how">how it works</a></li>
        <li><a href="/about">about</a></li>
        <!--<li><a href ="/suggest">suggest a question</a></li>-->
        
        {% comment %}
        The item below only appears for users that have permissions to "view aggregates." This
        is a standard Django permission and can currently be set through the database.
        
        This should probably be implemented using {% if perm.models.view_aggregates %} but
        I can't figure out how to make it work.
        {% endcomment %}
        
        {% if 'models.view_aggregates' in user.get_all_permissions %}
        <li style="font-weight: bold; text-decoration: underline;"><a href ="/summary">administer</a></li>
        {% endif %}
        <li><a href ="/community">community</a></li>
        <li><a href="/account/logout">log out</a></li>
      </ul>
    </div>
    <div style="clear: both; height: 0px;">&nbsp;</div>
</div>
