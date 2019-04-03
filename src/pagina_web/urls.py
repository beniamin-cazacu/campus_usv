from django.conf.urls import url
from django.contrib.auth import views as auth_views

from pagina_web.views import (
    AboutView,
    PrincipalPage
)

urlpatterns = [

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,  {'next_page': 'login'}, name='logout'),
    url(r'^prezentare/', AboutView.as_view(), name="pagina_prezentare"),
    url(r'^principal/', PrincipalPage.as_view(), name="principal_page")
]
