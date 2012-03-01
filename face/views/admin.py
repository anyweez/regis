from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

import face.models.models as models
import datetime, math, json

@permission_required('models.view_aggregates')
def index(request):
    return render_to_response('admin/index.tpl', {'user' : request.user })

def request_chart(request, chart_type):
    result = None
    if chart_type == 'engagement':
        result = _chart_engagement()

    if result is None:
        raise Exception('Unknown chart type: %s' % chart_type)    
    return HttpResponse(json.dumps(result),
        mimetype='application/json')

def get_chart(request, chart_type):
    return render_to_response('admin/chart_view.tpl', 
        { 'user' : request.user, 'chart_type' : chart_type })

# Generates data for the "New Joins" chart in the summary menu.
def chart_new_joins(request):
    joins = [user.date_joined for user in models.User.objects.all()]
    
    num_buckets = 20
    earliest = min(joins)
    latest = max(joins)

    # Get the number of members that were registered in each of 20 chronological "buckets"
    # spanning from the first member's join date until the most recent's.    
    delta = ((latest - earliest).total_seconds() + 1) / num_buckets
    buckets = [len(filter(lambda t: t < earliest + datetime.timedelta(x * delta), joins)) for x in xrange(num_buckets)]

    chart = {
        'title' : 'New joins since %s' % joins[0],
        'description' : 'The cumulative number of members that have existed at a particular point in time.',
        'type' : 'line',
        'xdata' : [x+1 for x in xrange(num_buckets)],
        'ydata' : buckets
    }
    
    return render_to_response('admin/chart_view.tpl', 
        { 'user' : request.user, 'chart' : chart })

def _chart_engagement(request):
    # Unique user logins per day.
    event_qry = models.RegisEvent.objects.filter(event_type="login")
    events = [event for event in event_qry]
    login_time = [event.when for event in events]
    
    num_days = int(math.ceil((max(login_time) - min(login_time)).total_seconds() / 86400))
    lpd = [0 for d in xrange(num_days)]
    for d in xrange(num_days):
        current_day = min(login_time) + d * ((max(login_time) - min(login_time)) / num_days)
        valid_events = filter(lambda e: (e.when - current_day).total_seconds() < 86400 and (e.when - current_day).total_seconds() > 0, events)
        lpd[d] = len(list(set([event.who.id for even in valid_events])))

    chart = {
        'title' : 'User engagement',
        'description' : 'Several metrics for measuring user engagement over time.',
        'type' : 'line',
        'xdata' : [x+1 for x in xrange(num_days)],
        'ydata' : {
            'Unique logins per day' : lpd,
            'Logins per week (per user)' : lpd * 2
        }
    }
    return chart

@permission_required('models.view_aggregates')
def chart_view(request, plugin_id):
    return render_to_response('admin/chart_view.tpl', {'user' : request.user })