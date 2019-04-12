
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include('pagina_web.urls', namespace="web_page"))
]
