"""liuche URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from helpers.director import login_url 
from hello.engin_menu import PcMenu,F7Engine
from helpers.director import views as director_views
from helpers.case.organize import urls as organize_urls
from django.views.generic import RedirectView 
from helpers.face import urls as face_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include(login_url)),
    url(r'^pc/([\w\.]+)/?$',PcMenu.as_view(),name=PcMenu.url_name),
    url(r'f7/([\w\.]+)/?$',F7Engine.as_view(),name=F7Engine.url_name),
        
    url(r'^_ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^_ajax/?$',director_views.ajax_views), 
    url(r'^_face/', include(face_urls)),
    url(r'^_download/(?P<app>\w+)?/?$',director_views.donwload_views,name='download_url'),
    
    url(r'^orgnize/',include(organize_urls)),
    
    url(r'^mb/?$',RedirectView.as_view(url='/f7/home.f7')),
    url(r'^$',RedirectView.as_view(url='/pc/press?_name=home'))
]



from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)