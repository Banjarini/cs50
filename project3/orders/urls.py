
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static
from . import views

urlpatterns = [
   	path("", views.index, name="index"),
   	path("<str:menu>", views.menu, name="menu"),
 
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)