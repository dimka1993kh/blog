from django.shortcuts import render, redirect
from django.views.generic import DetailView, DeleteView
from .models import Post, Subscribers
from django.contrib.auth.models import User
from .forms import PostForm
import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from pprint import pprint
from django.core import serializers
from django.http import JsonResponse



def blog(request, name):
    posts = Post.objects.filter(author=User.objects.filter(username=name)[0].id)
    sub = Subscribers.objects.filter(profile=request.user.id)

    def create_subscribers_list(subscribers_objects):
        result = []
        for sub in subscribers_objects:
            result.append(sub.subscribe.id)
            # print(result)
        return result
    
    def create_users_list(users_objects):
        result = []
        for user in users_objects:
            result.append(user.id)
        return result


    def find_subscribe_info(subscriber=-1):
        if User.objects.filter(id=subscriber):
                btn_title = 'Отписаться'
                btn_class = 'btn btn-secondary'       
        else:
                btn_title = 'Подписаться'
                btn_class = 'btn btn-danger'
        return {'subscribe': subscriber, 'btn_title' : btn_title, 'btn_class' : btn_class}

    sub_info = [find_subscribe_info() for i in range(User.objects.all().count() - 1)]
    for i in range(User.objects.all().count() - 1):   
        if create_users_list(User.objects.exclude(username=name))[i] in create_subscribers_list(sub):      
            sub_info[i] = find_subscribe_info(create_users_list(User.objects.exclude(username=name))[i])
        else:
            sub_info[i] = find_subscribe_info()


    users = list(User.objects.exclude(username=name).values())
    for index, i in enumerate(users):
        i.update(sub_info[index])           
        

    data = {
        'posts' : posts,
        'name' : name,
        'data': users,
        'subscribers' : sub_info,
        'subscribers_list' : create_subscribers_list(sub),
        'subscribers_profile' : request.user.username,
    }
    return render(request, 'post/blog.html', data)


def add_post(request, name):
    error = ''
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/blog/{request.user.username}')
        else:
            error = 'Форма была не верной'
    form = PostForm(initial={
        'author' : request.user.id,
        'datetime' : datetime.datetime.now
    })
    data = {
        'form' : form,
        'error' : error,
        'data': User.objects.all(),
    }
    return render(request, 'post/add_post.html', data)


def delete(request, id, name):
    try:
        person = Post.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect(f'/blog/{request.user.username}')
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Пост не найден</h2>")

def subscribe(request, name):
    sub = User.objects.get(username=name)
    Subscribers.objects.create(profile=request.user, subscribe=sub)
    posts = Post.objects.filter(author=User.objects.filter(username=name)[0].id)
    data = {
        'posts' : posts,
        'data': User.objects.all(),
        'subscribers' : Subscribers.objects.all()
    }
    return redirect(f'/blog/{request.user.username}/newsfeed')

def unsubscribe(request, name):
    for subscribe in Subscribers.objects.all():
        print(subscribe.profile)
        print(User.objects.get(username=request.user.username).id)
        if subscribe.subscribe.id == User.objects.get(username=name).id and subscribe.profile.id == User.objects.get(username=request.user.username).id:
            print(subscribe)
            subscribe.delete()
        else:
            print('Не удалилось=((((')
    return redirect(f'/blog/{request.user.username}/newsfeed')

def newsfeed(request, name):
    subscribers = Subscribers.objects.filter(profile=request.user.id)
    posts = []
    print(subscribers)
    for subscriber in subscribers:
        posts.append(Post.objects.filter(author=subscriber.subscribe))

    sub = Subscribers.objects.filter(profile=request.user.id)   

    def create_users_list(users_objects):
        result = []
        for user in users_objects:
            result.append(user.id)
        return result
    
    def create_subscribers_list(subscribers_objects):
        result = []
        for sub in subscribers_objects:
            result.append(sub.subscribe.id)
            # print(result)
        return result
    
    def find_subscribe_info(subscriber=-1):
        if User.objects.filter(id=subscriber):
                btn_title = 'Отписаться'
                btn_class = 'btn btn-secondary'       
        else:
                btn_title = 'Подписаться'
                btn_class = 'btn btn-danger'
        return {'subscribe': subscriber, 'btn_title' : btn_title, 'btn_class' : btn_class}

    sub_info = [find_subscribe_info() for i in range(User.objects.all().count() - 1)]
    for i in range(User.objects.all().count() - 1):   
        if create_users_list(User.objects.exclude(username=name))[i] in create_subscribers_list(sub):      
            sub_info[i] = find_subscribe_info(create_users_list(User.objects.exclude(username=name))[i])
        else:
            sub_info[i] = find_subscribe_info()


    users = list(User.objects.exclude(username=name).values())
    for index, i in enumerate(users):
        i.update(sub_info[index])  

    data = {
        'posts' : posts,
        'name' : name,
        'data': users,
        'subscribers' : sub_info,
        'subscribers_list' : create_subscribers_list(sub),
        'subscribers_profile' : request.user.username,
    }
    print(posts)

    return render(request, 'newsfeed/newsfeed.html', data)

