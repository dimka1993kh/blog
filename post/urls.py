from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:name>/addpost/', views.add_post, name='post'),
    path('<str:name>/', views.blog, name='blog'),
    path('<str:name>/delete/<int:id>/', views.delete),
    path('<str:name>/subscribe', views.subscribe, name='subscribe'),
    path('<str:name>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('<str:name>/newsfeed', views.newsfeed, name='newsfeed'),    
]


