"""Web_SA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from hello import views  # from 애플리케이션명 import views 형식으로 hello 앱의 views를 임포트
from index import views as index_views
from balance import views as balance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # hello 애플리케이션의 URL에 대한 뷰 처리를 추가, 첫 글자가 대문자이면 hello 애플리케이션의 views.py에 존재하는 sayHello()함수를 호출(정규 표현식)
    re_path(r'^(?P<name>[A-Z][a-z]*)$', views.sayHello),
    # index/ -> 인덱스 애플리케이션 뷰의 main_view()함수로 매핑하라는 의미
    path('index/', index_views.main_view),
    path('balance/', balance_views.main_view)
]
