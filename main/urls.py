from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('account/', include('accounts.urls')),
    path('blog/', include('post.urls')),
]
