from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import Subscribers

# Create your views here.

def index(request):
    data = {
        'data': User.objects.all(),
        'subscribers_profile' : request.user.username,
        'subscribers' : Subscribers.objects.filter(profile=request.user.id),
    }
    return render(request, 'main/index.html', data)
