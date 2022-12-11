"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from portafolios import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('portafolios/', views.portafolios, name="portafolios"),
    path('portafolios_universal/', views.portafolios_universal, name="portafolios_universal"),
    path('portafolios_completed/', views.portafolios_completed, name="portafolios_completed"),
    path('portafolios/create/', views.create_portafolios, name="create_portafolios"),
    path('portafolios/<int:portafolio_id>/', views.portafolio_detail, name="portafolio_detail"),
    path('portafolios/<int:portafolio_id>/complete', views.complete_portafolio, name="complete_portafolio"),
    path('portafolios/<int:portafolio_id>/delete', views.delete_portafolio, name="delete_portafolio"),
    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name="signin"),
]
