from django.conf.urls import url
from django.contrib.auth import views as auth_views

from pagina_web.views import (
    AboutView,
    HomePageView,
    ApplicationEnrollmentView,
    redirect_home
)

urlpatterns = [

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'web_page:login'}, name='logout'),
    url(r'^developers/$', AboutView.as_view(), name="developers_details"),
    url(r'^application/$', ApplicationEnrollmentView.as_view(), name="application_enrollment"),
    url(r'^home/$', HomePageView.as_view(), name="home_page"),
    url(r'^$', redirect_home, name="home"),

]
