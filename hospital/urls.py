from django.views.generic.base import TemplateView, RedirectView
from . import models, views
from django.urls import path,include
from django.conf.urls import url
app_name = 'hospital'

urlpatterns = [
    path("",RedirectView.as_view(url="authentica"),name="auth_manager"),
    path("authentica", views.authentication_manager,name="auth_manager"),
    path("home", views.home_view,name="home"),
    path("logout",views.logout_view,name='logout'),
    path("hospital", views.hospital_auth,name="hospital_login"),
    path("scan", TemplateView.as_view(template_name="scan.html"),name = "scan_manager"),
    path("views/<str:username>", views.profile_view,name="profile_view"),
    path("filter_hosp", views.filter_hospital,name="filter hospital"),
    path("_search",views.search_hosp,name="search_hosp"),
    path("_search/<str:license>", views.hosp_profile, name="hosp_profile"),
    path('find', views.search_hosp, name='find'),
    path('home/page', views.loadspec, name='page'),
    path('home/ans', views.specialfunc, name='ans'),
]
