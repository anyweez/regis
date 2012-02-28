from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required

@permission_required('models.view_aggregates')
def index(request):
    
    return render_to_response('admin/index.tpl', {'user' : request.user })