from django.conf.urls import url

from pagina_web.views import AboutView

urlpatterns = [

    url(r'^prezentare/', AboutView.as_view(), name="pagina_prezentare")
]
