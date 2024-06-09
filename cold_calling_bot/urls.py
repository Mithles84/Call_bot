"""cold_calling_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
# ]

from django.contrib import admin
from django.urls import include, path
from coldcalling.views import index 
from django.contrib.auth import views as auth_views
from coldcalling.views import register_view, login_view,cold_calling,train_model_view,predict_view
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [ 
     path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('train/', train_model_view, name='train_model'),
    path('predict/', predict_view, name='predict'),
    path('coldcalling/', cold_calling, name='cold_calling'), 
]

