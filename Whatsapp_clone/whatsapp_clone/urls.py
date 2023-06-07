"""whatsapp_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from chats.views import index,LandingPageView ,chatPage,search_users , search, login_request, creator_profile

from payments.views import initiate_payment,payment_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('chat/', index, name='home'),
    path('chat/None/', chatPage, name='chatPage'),
    path('chat/<int:id>/', chatPage, name='chatPage'),
    #path('search_users/', search_users, name='search_users'),
    #path('search/', search, name='search'),
   
    path('search/', search_users, name='search_users'),
    
    path('sea/', search, name = 'search'),

    path('', LandingPageView.as_view(), name = "landingpage"),
    path("chats/", include("chats.urls")),
    path('accounts/', include('allauth.urls')),


    path('login/',login_request, name='login_main'),

    path('Creator_profile/<int:id>/', creator_profile, name='creator_profile'),

    path('paytm/initiate-payment/', initiate_payment, name='paytm-initiate-payment'),
    path('paytm/callback/', payment_callback, name='paytm-callback'),


    
]


from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
